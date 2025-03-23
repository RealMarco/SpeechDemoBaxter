# Speech Demonstration for Baxter Robot
## Env
ubuntu 18, ros melodic, baxter pkg

## Speech Recognition
```
#Speech Recognition and Pub to voice_msg to ROS
baxter/src/speech/src/demo_multi_thread.py, or demo.py
```
1）lib文件夹下有libais-lite-Ual.so和libunikws.so，其中libais-lite-Ual.so是识别引擎基础库，被libunikws.so调用，libais-lite-Ual.so需要放在可检索到的系统目录 (e.g. **in the shared 3090 /home/znfs/anaconda3/lib/libais-lite-Ual.so for anaconda base env; and /usr/lib/libais-lite-Ual.so for system python**)，libunikws.so不需要，libunikws.so在python代码中动态调用
2）data文件夹下是语法文件，是开发过程中使用的，需要根据实际项目进行替换，目前是保留了测试用的语法文件
3）上述路径在代码中都是可配置的
4）demo_multi_thread.py是使用线程调用语音识别的例子

## Speech to Baxter Actions
```
baxter/src/baxter_project/scripts/speech_baxter.py
```
