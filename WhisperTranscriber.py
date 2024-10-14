# 实现了Whisper的基本参数配置

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
):
    # 加载模型
    model = whisper.load_model(model, device=device)

    for audio in audio_files:
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
        base_name = os.path.splitext(os.path.basename(audio))[0]
        formats = output_format if output_format != 'all' else ["txt", "vtt", "srt", "json"]

        for fmt in formats:
            output_file = os.path.join(output_dir, f"{base_name}.{fmt}")
            if fmt == "txt":
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result["text"])
            elif fmt == "srt":
                with open(output_file, "w", encoding="utf-8") as f:
                    writer = whisper.utils.WriteSRT(output_dir)
                    writer.write_result(result, f)
            elif fmt == "vtt":
                with open(output_file, "w", encoding="utf-8") as f:
                    writer = whisper.utils.WriteVTT(output_dir)
                    writer.write_result(result, f)
            elif fmt == "json":
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

        if verbose:
            print(f"Transcription complete for {audio}. Output saved to {output_dir}")

# 脚本既作为可执行程序，又作为可导入的模块
if __name__ == "__main__":
    transcribe_audio(
        audio_files=["beekeeping is most difficult.mp4"],
        model="turbo",
        language="en",
        initial_prompt="This topic is about beekeeping:",
        word_timestamps=True,
        output_format="all",
        fp16=False,
        verbose=True
    )
