# WhisperTranscriber
# src: https://github.com/VimWei/WhisperTranscriber
# 实现 Whisper 的基本参数配置
# 实现对srt输出的参数控制，从而可以实现逐字srt
    # max_line_width，max_line_count，max_words_per_line
# 实现对srt断行控制的自由切换：人工还是自动

import whisper
import os
import json

def transcribe_audio(
    audio_files,
    model="turbo",
    model_dir=None,
    device="cpu",
    output_dir=".",
    output_format="all",
    verbose=True,
    task="transcribe",
    language=None,
    temperature=0,
    best_of=5,
    beam_size=5,
    patience=None,
    length_penalty=None,
    suppress_tokens="-1",
    initial_prompt=None,
    condition_on_previous_text=True,
    fp16=True,
    word_timestamps=False,
    max_line_width=None,
    max_line_count=None,
    max_words_per_line=None,
    use_default_line_breaks=False,
):
    # 加载模型
    model = whisper.load_model(model, device=device)

    for audio in audio_files:
        # 获取文件名（去掉扩展名）
        base_name = os.path.splitext(os.path.basename(audio))[0]

        # 使用 transcribe 函数
        result = model.transcribe(
            audio,
            language=language,
            task=task,
            temperature=temperature,
            best_of=best_of,
            beam_size=beam_size,
            patience=patience,
            length_penalty=length_penalty,
            suppress_tokens=suppress_tokens,
            initial_prompt=initial_prompt,
            condition_on_previous_text=condition_on_previous_text,
            fp16=fp16,
            word_timestamps=word_timestamps,
            verbose=verbose,
        )

        # 处理输出
        formats = output_format if output_format != 'all' else ["txt", "vtt", "srt", "json"]

        for fmt in formats:
            output_file = os.path.join(output_dir, f"{base_name}.{fmt}")
            if fmt == "txt":
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result["text"])
            elif fmt == "srt":
                # 手动处理 SRT 输出
                with open(output_file, "w", encoding="utf-8") as f:
                    if use_default_line_breaks:
                        write_srt_with_default_line_breaks(result, f)
                    else:
                        write_srt_with_word_timestamps(result, f, max_line_width, max_line_count, max_words_per_line)
            elif fmt == "vtt":
                with open(output_file, "w", encoding="utf-8") as f:
                    writer = whisper.utils.WriteVTT(output_dir)
                    writer.write_result(result, f)
            elif fmt == "json":
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

        if verbose:
            print(f"Transcription complete for {audio}. Output saved to {output_dir}")

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
    transcribe_audio(
        audio_files=["beekeeping is most difficult.mp4"],
        model="turbo",
        language="en",
        initial_prompt="This topic is about beekeeping:",
        fp16=False,
        word_timestamps=True,
        # 断行人工控制
        max_line_width=42,
        max_words_per_line=5,
        max_line_count=None,
        # 断行自动控制
        use_default_line_breaks=False,
        output_format="all",
        verbose=True
    )
