# Whisper Transcribe 及 Subtitle 相关小工具

## Whisper Transcribe

方便配置 [OpenAI Whisper](https://github.com/openai/whisper) 各种参数，并增强部分功能：

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
   * 首先，（自动）让Whisper自动断句
   * 然后，（自由）借助AI批量断句，也可应用txt-resegment-by-rules.vim，在人工任意断句
   * 最后，（快速）使用 srt-resegment-by-json.py 一键同步精准时间戳
5. 支持同时处理多个多媒体文件
   * 自动读取目录下所有支持的文件
   * 也可以只处理指定的文件
6. 支持同时输出不同格式: SRT/JSON/VTT/TXT

## 推荐使用: WhisperX Transcribe

* srt: https://github.com/VimWei/WhisperXTranscriber
    - Batched inference for 70x realtime transcription using whisper large-v2
    - faster-whisper backend, requires <8GB gpu memory for large-v2 with beam_size=5
    - Accurate word-level timestamps using wav2vec2 alignment
    - Multispeaker ASR using speaker diarization from pyannote-audio (speaker ID labels)
    - VAD preprocessing, reduces hallucination & batching with no WER degradation

## Subtitle 相关小工具

1. clean-vtt.py
   * 清理VTT格式字幕文件中的重复字幕内容，常见于youtube下载的vtt文件

2. txt-resegment-by-rules.vim
   * vim script: 基于常见规则给纯文本字幕文件批量断句，减轻手工断句处理工作量

3. srt-resegment-by-json.py
   * Synchronize SRT with Whisper's Word-Level Timestamps JSON
   * 推荐使用 [无缝集成到mpv的lua版本](https://github.com/VimWei/mpv-config)

4. FixTranslation.vim
   * vim script: 批量修正字幕文件中的常见翻译错误

## 安装与使用

1. (建议) 新建一个独立的 python 环境，并激活:
    * 创建：conda create -n whisper python=3.11
    * 激活：conda activate whisper
2. 安装依赖包:
    * pip install -r requirements.txt
3. 配置并运行程序:
   * 配置 config.yaml
   * 运行: python WhisperTranscriber.py
