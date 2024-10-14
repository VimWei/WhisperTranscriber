import json
import re

def generate_srt(json_data, text):
    # 分割纯文本成行列表
    lines = text.split('\n')

    # 初始化 SRT 内容
    srt_content = ""
    line_id = 1

    # 将所有单词及其时间信息放入一个列表中
    all_words = []
    for segment in json_data['segments']:
        all_words.extend(segment['words'])

    word_index = 0

    # 遍历每行
    for line in lines:
        # 使用正则表达式分割单词，保留标点符号
        words = re.findall(r'\w+|[^\w\s]', line.strip())

        if not words:
            continue

        start_time = None
        end_time = None

        # 找到对应的词时间信息
        line_start_index = word_index
        matched_words = []

        while word_index < len(all_words) and words:
            word_info = all_words[word_index]
            word = word_info['word'].strip()

            # 移除标点符号进行比较
            clean_word = re.sub(r'[^\w\s]', '', word)
            clean_expected_word = re.sub(r'[^\w\s]', '', words[0])

            if clean_word.lower() == clean_expected_word.lower():
                if start_time is None:
                    start_time = word_info['start']
                end_time = word_info['end']
                matched_words.append(words.pop(0))

                # 检查并移除最后一个可能的标点符号
                if words and re.match(r'^[^\w\s]+$', words[0]):
                    matched_words.append(words.pop(0))  # 移除标点符号

            word_index += 1

            if not words:  # 如果所有单词都匹配完了，就结束循环
                break

        # 如果没有找到匹配的单词，回退到这一行开始的地方
        if words:
            word_index = line_start_index
            print(f"Warning: Could not find complete timing for line: {line}")
            print(f"Matched words: {matched_words}")
            print(f"Remaining words: {words}")

        # 生成 SRT 内容
        if start_time is not None and end_time is not None:
            srt_content += f"{line_id}\n{format_time(start_time)} --> {format_time(end_time)}\n{line}\n\n"
            line_id += 1
        else:
            print(f"Warning: Could not find timing for line: {line}")

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
