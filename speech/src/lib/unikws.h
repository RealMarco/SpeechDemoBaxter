/**
@file       unikws.h
@date       2023/7/27
@author     yzs
@version    v1.0.0
@brief      提供离线语音识别的接口，包括初始化离线语音识别引擎，开始识别，停止识别，释放资源
@details    完整的识别包括四个过程，init - start - stop - deinit，在init和deinit之间，可以重复调用start和stop，
            一次start和stop支持多次语音识别，因此可根据具体业务需求，调用一次start和stop，或者多次。
            1）需要成对调用；2）如果通过一次start和stop可以满足要求，建议使用一次，因为两个接口都有相应的开销
@history    2023/9 增加对跨语言（python）和跨平台linux Windows的支持
            2023/11 剥离录音和Windows库的依赖，完全移植到linux平台
*/
#ifndef UNIKWS_H
#define UNIKWS_H

extern "C"
{
    /*!
     * @brief    初始化录音和识别引擎，根据需求，暂不提供各种参数的设置接口，高度封装
     * @param    [in]const char * strModelPath vad模型和kws模型的路径
     * @return   int    0 成功；1 失败，暂不分类失败code，如需了解，参考strMsg
     */
    int InitApi(const char *strModelPath);

    // 定义回调函数，该回调函数用于语音识别过程中返回确定的结果。在跨语言集成经验中，字符串有长度错误的情况，
    // 因此使用了指针和长度，如调用者开发语言为C++，则可以直接使用指针
    // 返回结果的编码为utf-8
    typedef void (*KwsResultCallback)(const char *strResult, int nLen);

    // 注意：上述两个函数的实现中，千万不要有耗时的处理或者阻塞的动作，如需要请开辟线程
    /*!
     * @brief    开始识别
     * @param    [in]KwsResultCallback pfResult 处理语音识别结果的方法
     * @return   int    0 成功；1 失败，因为初始化成功后开始识别失败，问题只能发生在引擎内部，
                        因此不返回具体的错误内容，需要提交开发者解决
     */
    int StartApi(KwsResultCallback pfResult);

    /*!
     * @brief    识别语音，如有识别结果在回调函数中处理
     * @param    [in]char * pBuffer 语音数据指针
     * @param    [in]int nLen       语音数据长度
     * @return   int    0 成功；1 失败
     */
    int RecognizeApi(char *pBuffer, int nLen);

    /*!
     * @brief    停止识别
     * @return   int    0 成功；1 失败
     */
    int StopApi();

    /*!
     * @brief    去初始化
     * @return   int    0 成功；1 失败
     */
    int DeinitApi();
}

#endif // UNIKWS_H
