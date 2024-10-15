# WhisperTranscriber

## 简介

原生的 [OpenAI Whisper](https://github.com/openai/whisper) 是一个简易的命令行程序，为方便配置各种参数，并增强部分功能，从而实现：

1. 或让Whisper自动断句：
   * use_default_line_breaks=True
2. 或自由定义断句的参数：
   * use_default_line_breaks=False
   * max_line_width=78,
   * max_words_per_line=5,
   * max_line_count=None,
3. 甚至生成逐字的精准字幕：
   * use_default_line_breaks=False
   * max_line_width=78,
   * max_words_per_line=1,
   * max_line_count=None,
4. 甚至实现断句的完全自由调整：
   * 先：（自由）借助AI批量断句，也可人工任意断句
   * 后：（快速）使用 ReSegment.py 一键同步精准时间戳
   * ReSegment.py 可独立使用，百搭各种 Whisper 衍生品
5. 支持同时处理多个文件
6. 支持同时输出不同格式: SRT/JSON/VTT/TXT

## 安装与使用

1. (建议) 新建一个独立的 python 环境，并激活:
    * 创建：conda create -n whisper python=3.11
    * 激活：conda activate whisper
2. 安装 OpenAI Whisper:
    * pip install -U openai-whisper
3. 运行程序:
    * python WhisperTranscriber.py
    * python ReSegment.py
