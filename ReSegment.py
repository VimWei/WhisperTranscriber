# ReSegment.py
# https://github.com/VimWei/WhisperTranscriber
# Synchronize SRT with Whisper's Word-Level Timestamps JSON
    # 实现断句的完全自由
# 提升文本匹配的兼容性
    # 无视标点符号
    # 适应简单的文本增删改情形

import json
import re

def generate_srt(json_data, text):
    lines = text.strip().split('\n')
    srt_content = ""
    line_id = 1

    # 提取JSON中的单词
    json_all_words = []
    for segment in json_data['segments']:
        json_all_words.extend(segment['words'])

    json_word_index = 0
    matched_words_index = 0
    previous_end_time = 0  # 存储上一行的结束时间

    for line in lines:
        # 提取TXT中的单词：只要单词，不要标点符号
        txt_words = re.findall(r'\b\w+\b', line.strip())
        # print(f"txt_words: {txt_words}")

        if not txt_words:
            continue

        start_time = None
        end_time = None
        matched_words = []

        # 遍历TXT中的每个单词以查找匹配
        for txt_word in txt_words:
            # print(f"开始匹配: {txt_word} ...")
            matched = False  # 标记是否找到匹配

            while json_word_index < len(json_all_words):
                json_word_info = json_all_words[json_word_index]
                clean_json_word = re.sub(r'[^\w\s]', '', json_word_info['word']).strip()

                if clean_json_word.lower() == txt_word.lower():
                    if start_time is None:
                        start_time = json_word_info['start']
                    end_time = json_word_info['end']
                    matched_words.append(txt_word)
                    # print(f"matched_words_index: {matched_words_index}")
                    matched = True
                    matched_words_index = json_word_index + 1
                    break  # 找到匹配后退出循环
                else:
                    json_word_index += 1

            if matched:
                json_word_index = matched_words_index
            else:
                json_word_index = matched_words_index-1
                print(f"Warning: Could not match word '{txt_word}' in line {line_id}")

        # 设置时间戳
        if start_time is None:
            start_time = previous_end_time

        if end_time is None:
            end_time = previous_end_time

        srt_content += f"{line_id}\n{format_time(start_time)} --> {format_time(end_time)}\n{line}\n\n"
        previous_end_time = end_time  # 更新上一行结束时间
        line_id += 1

    return srt_content

def format_time(time_in_seconds):
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def main():
    # 设置路径
    json_file_path = 'path/to/whisper_output.json'
    text_file_path = 'path/to/text_file.txt'
    output_srt_path = 'path/to/output.srt'

    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # 读取文本文件
    with open(text_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 生成 SRT 内容
    srt_content = generate_srt(json_data, text)

    # 写入 SRT 文件
    with open(output_srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    print(f"SRT file has been generated: {output_srt_path}")

if __name__ == "__main__":
    main()
