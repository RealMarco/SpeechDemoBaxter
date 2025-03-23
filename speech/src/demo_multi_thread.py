#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   demo_multi_thread.py
@Time    :   2023/12/26 23:28:10
@Author  :   by 204 
'''
# -*- coding: utf-8 -*-
import os
import sys
import threading
import pyaudio
import wave
from ctypes import *
import rospy
from speech.msg import voicemsg


# 录音类
class AudioRecorder:
    def __init__(self):
        dir = os.getcwd()
        # 根据实际工程设置目录
        libPath = dir + r"/lib/libunikws.so"
        # print(libPath)
        if os.path.exists(libPath) == False:
            self.is_valid = False
            return
        self.is_valid = True
        # 加载动态库
        self.clibinstance = cdll.LoadLibrary(libPath)
        # 线程相关
        self.is_recording = False
        self.audio_thread = threading.Thread(target=self.record_audio)

        rospy.init_node("speech_command",anonymous=True)
        self.pub = rospy.Publisher("voice_msg",voicemsg,queue_size=1)
    
        
        self.rate = rospy.Rate(20)

    # 开始识别
    def start_recording(self):
        if self.is_valid == False:
            return
        # 启动线程
        self.is_recording = True
        self.audio_thread.start()

    # 停止识别
    def stop_recording(self):
        if self.is_valid == False:
            return
        # 停止线程
        self.is_recording = False
        self.audio_thread.join()  # 等待录音线程结束

    # 识别线程
    def record_audio(self):
        dir = os.getcwd()
        modelPath = dir + r"/data/grammar.dat"
        byPath = modelPath.encode("utf-8")
        self.clibinstance.InitApi.argtypes = [c_char_p]
        self.clibinstance.InitApi.rettype = c_int
        ret = self.clibinstance.InitApi(c_char_p(byPath))
        # print(f"dll.InitApi() return {ret}")
        cfkws = CFUNCTYPE(None, c_char_p, c_int)
        

        def dealKwsResult(reuslt, length):
            print(reuslt)
            command = str(reuslt, "utf-8")
            print("speech command:", command)
            order = 0
            if '向前' in command:
                order = 1
            elif '向后' in command:
                order = 2
            elif '向左' in command:
                order = 3   
            elif '向右' in command:
                order = 4
            elif '开' in command:
                order = 5
            elif '关' in command:
                order = 6
            elif '翻转' in command:
                order = 7                         

            msg = voicemsg()
            msg.order = order
            self.pub.publish(msg)
            rospy.loginfo("Published speech command: %d", msg.order)
            self.rate.sleep()

        c_callback = cfkws(dealKwsResult)
        ret = self.clibinstance.StartApi(c_callback)
        # print(f"dll.StartApi() return {ret}")
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=320,
        )

        while self.is_recording:
            data = stream.read(320)
            ret = self.clibinstance.RecognizeApi(data, 640)

        # 结束识别，释放资源
        ret = self.clibinstance.StopApi()
        # print("dll.StopApi() return: ", ret)
        ret = self.clibinstance.DeinitApi()
        # print("dll.DeinitApi() return: ", ret)

        # 停止录音
        stream.stop_stream()
        stream.close()
        p.terminate()

# 这里用户输入stop可以停止识别
def get_user_input(recorder):
    while True:
        user_input = input("Enter 'stop' to stop recording: ")

        if user_input.lower() == "stop":
            recorder.stop_recording()
            break


if __name__ == "__main__":
    # 识别线程
    recorder = AudioRecorder()
    recorder.start_recording()
    

    # 等待停止，需要根据需求调用语音识别停止方法
    user_thread = threading.Thread(target=get_user_input, args=(recorder,))
    user_thread.start()
