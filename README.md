# WhisperTranscriber

原生的 OpenAI Whisper 是一个简易的命令行程序，其参数比较多，为方便配置各种参数，并增强部分功能，从而实现：

1. 可以生成逐字的精准字幕。
2. 或让Whisper自动断句：
   * use_default_line_breaks=True
3. 或自由定义断句的参数：
   * use_default_line_breaks=False
   * max_line_width=42,
   * max_words_per_line=5,
   * max_line_count=None,

缺点及建议：https://github.com/SubtitleEdit/subtitleedit/issues/8908
