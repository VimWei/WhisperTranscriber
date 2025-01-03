# WhisperTranscriber
# src: https://github.com/VimWei/WhisperTranscriber
# 实现 Whisper 的基本参数配置
# 实现对srt输出的参数控制，从而可以实现逐字srt
    # max_line_width，max_line_count，max_words_per_line
# 实现对srt断行控制的自由切换：人工还是自动

import whisper
import os
import json
import yaml
from pathlib import Path

def load_config(config_file='config.yaml'):
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_media_files(config):
    """获取要处理的媒体文件列表"""
    input_dir = config['input']['directory']
    formats = config['input']['formats']
    specific_files = config['input']['specific_files']

    # 确保输入目录存在
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created input directory: {input_dir}")
        return []

    # 如果指定了具体文件，则只处理这些文件
    if specific_files:
        return [os.path.join(input_dir, f) for f in specific_files 
                if os.path.exists(os.path.join(input_dir, f))]

    # 否则处理目录下所有支持的格式
    media_files = []
    for format in formats:
        media_files.extend(
            str(p) for p in Path(input_dir).glob(f"*{format}")
        )
    
    return sorted(media_files)

def transcribe_audio(config_file='config.yaml'):
    """使用配置文件的转写函数"""
    # 加载配置
    config = load_config(config_file)
    
    # 获取要处理的媒体文件
    media_files = get_media_files(config)
    
    if not media_files:
        print(f"No media files found in {config['input']['directory']}")
        print(f"Supported formats: {', '.join(config['input']['formats'])}")
        return

    print(f"Found {len(media_files)} files to process:")
    for file in media_files:
        print(f"  - {os.path.basename(file)}")
    print()

    # 加载模型
    model = whisper.load_model(
        config['model']['name'],
        device=config['model']['device']
    )

    for audio in media_files:
        print(f"Processing: {os.path.basename(audio)}")
        # 获取文件名（去掉扩展名）
        base_name = os.path.splitext(os.path.basename(audio))[0]

        # 使用 transcribe 函数
        result = model.transcribe(
            audio,
            language=config['transcription']['language'],
            task=config['transcription']['task'],
            temperature=config['transcription']['temperature'],
            best_of=config['transcription']['best_of'],
            beam_size=config['transcription']['beam_size'],
            patience=config['transcription']['patience'],
            length_penalty=config['transcription']['length_penalty'],
            suppress_tokens=config['transcription']['suppress_tokens'],
            initial_prompt=config['transcription']['initial_prompt'],
            condition_on_previous_text=config['transcription']['condition_on_previous_text'],
            fp16=config['model']['fp16'],
            word_timestamps=config['transcription']['word_timestamps'],
            verbose=config['output']['verbose'],
        )

        # 处理输出
        formats = config['output']['format'] if config['output']['format'] != 'all' else ["txt", "vtt", "srt", "json"]

        for fmt in formats:
            output_file = os.path.join(config['output']['directory'], f"{base_name}.{fmt}")
            if fmt == "txt":
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result["text"])
            elif fmt == "srt":
                # 手动处理 SRT 输出
                with open(output_file, "w", encoding="utf-8") as f:
                    if config['srt']['use_default_line_breaks']:
                        write_srt_with_default_line_breaks(result, f)
                    else:
                        write_srt_with_word_timestamps(
                            result, 
                            f,
                            config['srt']['max_line_width'],
                            config['srt']['max_line_count'],
                            config['srt']['max_words_per_line']
                        )
            elif fmt == "vtt":
                with open(output_file, "w", encoding="utf-8") as f:
                    writer = whisper.utils.WriteVTT(config['output']['directory'])
                    writer.write_result(result, f)
            elif fmt == "json":
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

        if config['output']['verbose']:
            print(f"Transcription complete for {audio}. Output saved to {config['output']['directory']}")

def write_srt_with_word_timestamps(result, file, max_line_width=None, max_line_count=None, max_words_per_line=None):
    # 初始化变量
    line_index = 1
    current_line = ""
    current_line_start = None
    current_line_end = None
    words_in_line = 0

    for segment in result["segments"]:
        for word in segment["words"]:
            # 检查是否需要换行
            if (max_line_width and len(current_line) + len(word["word"]) + 1 > max_line_width) or \
               (max_words_per_line and words_in_line >= max_words_per_line) or \
               (max_line_count and line_index >= max_line_count):
                # 写入当前行
                if current_line_start is not None and current_line_end is not None:
                    print(f"{line_index}\n{format_timestamp(current_line_start)} --> {format_timestamp(current_line_end)}\n{current_line.strip()}\n", file=file)
                # 重置当前行
                line_index += 1
                current_line = ""
                current_line_start = None
                current_line_end = None
                words_in_line = 0

            # 更新行的开始和结束时间
            if current_line_start is None:
                current_line_start = word["start"]
            current_line_end = word["end"]

            # 追加单词
            current_line += word["word"] + " "
            words_in_line += 1

    # 写入最后一行
    if current_line:
        if current_line_start is not None and current_line_end is not None:
            print(f"{line_index}\n{format_timestamp(current_line_start)} --> {format_timestamp(current_line_end)}\n{current_line.strip()}\n", file=file)

def write_srt_with_default_line_breaks(result, file):
    for segment in result["segments"]:
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip().replace("-->", "->")
        print(f"{segment['id']}\n{start} --> {end}\n{text}\n", file=file)

def format_timestamp(seconds: float):
    milliseconds = int(seconds * 1000)
    hours = milliseconds // 3600000
    minutes = (milliseconds % 3600000) // 60000
    seconds = (milliseconds % 60000) // 1000
    milliseconds = milliseconds % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

if __name__ == "__main__":
    transcribe_audio()
