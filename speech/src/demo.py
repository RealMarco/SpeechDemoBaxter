#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   demo_multi_thread.py
@Time    :   2023/12/26 23:28:10
@Author  :   by 204 
'''
import os
import sys
import pyaudio
import wave
from ctypes import *
import rospy
from speech.msg import voicemsg

"""_summary_
该demo实现了加载动态库，加载识别模型，初始化-识别-停止-释放的过程
"""



if __name__ == "__main__":
    rospy.init_node("speech_command",anonymous=True)
    pub = rospy.Publisher("voice_msg", voicemsg, queue_size=1)
    rate = rospy.Rate(20)

    # 加载动态库so文件
    dir = os.getcwd()
    # 根据实际工程设置目录
    libPath = dir + r"/lib/libunikws.so"
    # print(libPath)
    if os.path.exists(libPath) == False:
        print(f"库文件{libPath}不存在!")
        sys.exit()

    # 加载动态库
    clibinstance = cdll.LoadLibrary(libPath)

    # 识别模型的路径，需要改为用户实际使用的模型
    modelPath = dir + r"/data/grammar.dat"
    # print(modelPath)

    # 调用初始化接口，传入模型路径，在该接口中完成加载模型，开辟相应的内存等操作
    byPath = modelPath.encode("utf-8")
    clibinstance.InitApi.argtypes = [c_char_p]
    clibinstance.InitApi.rettype = c_int
    ret = clibinstance.InitApi(c_char_p(byPath))
    # print(f"dll.InitApi() return {ret}")

    # 定义C++使用的回调函数
    cfkws = CFUNCTYPE(None, c_char_p, c_int)
    spe_order = 0
    def dealKwsResult(reuslt, length):
        print(str(reuslt, "utf-8"))
        command = str(reuslt, "utf-8")
        global spe_order
        print("speech command:", command)
        if '向前' in command:
            spe_order = 1
        elif '向后' in command:
            spe_order = 2
        elif '向左' in command:
            spe_order = 3   
        elif '向右' in command:
            spe_order = 4
        elif '开' in command:
            spe_order = 5
        elif '关' in command:
            spe_order = 6
        elif '翻转' in command:
            spe_order = 7



    c_callback = cfkws(dealKwsResult)

    # msg = voicemsg()
    # msg.order = 1
    # pub.publish(msg)

    # 调用开始识别接口，在该接口中完成识别所需的准备工作，等待输入语音数据
    ret = clibinstance.StartApi(c_callback)
    # print(f"dll.StartApi() return {ret}")

    # 使用pyaudio进行录音，设置参数
    FORMAT = pyaudio.paInt16  # 16位采样
    CHANNELS = 1  # 单通道
    RATE = 16000  # 16k samples/s
    CHUNK = 320  # 20ms
    # 在该例子中使用一段时间来进行录音，需要根据实际需求进行调整，如不间断录音
    RECORD_SECONDS = 10  # 10秒
    # 额外工作，保存录音，可以回听来分析录音内容和质量，该部分不是必须的
    WAVE_OUTPUT_FILENAME = "output.wav"

    # 录音
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    # print("start recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # 读取CHUNK大小的录音数据，调用识别接口上传数据，通过回调函数输出结果
        data = stream.read(CHUNK)
        ret = clibinstance.RecognizeApi(data, 640)
        frames.append(data)

        msg = voicemsg()
        msg.order = spe_order
        print(msg)
        pub.publish(msg)
        rospy.loginfo("Published speech command: %d", msg.order)
    # print("stop recording...")

    # 结束识别，释放资源
    ret = clibinstance.StopApi()
    # print("dll.StopApi() return: ", ret)
    ret = clibinstance.DeinitApi()
    # print("dll.DeinitApi() return: ", ret)

    # 停止录音
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 保存录音结果为WAV文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    # rospy.spin()
