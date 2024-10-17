import pandas as pd
import re

class VTTLine:
    def __init__(self, start, end, text):
        self.start = start
        self.end = end
        self.text = text

def clean_vtt(vtt_lines):
    lines = []
    starts = []
    ends = []

    for line in vtt_lines:
        extend_text = line.text.strip().splitlines()
        repeat = len(extend_text)
        lines.extend(extend_text)
        starts.extend([line.start] * repeat)
        ends.extend([line.end] * repeat)

    previous = None
    new_lines = []
    new_starts = []
    new_ends = []

    for l, s, e in zip(lines, starts, ends):
        if l == previous:
            continue
        else:
            new_lines.append(l)
            new_starts.append(s)
            new_ends.append(e)
            previous = l

    df = {"start": new_starts, "end": new_ends, "text": new_lines}
    df = pd.DataFrame(df)
    return df

def parse_vtt(file_path):
    vtt_lines = []

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

        for i in range(len(content)):
            line = content[i].strip()
            if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line):
                start_end = line.split(' --> ')
                start_time = start_end[0]
                end_time = start_end[1]
                text_lines = []

                # Read the subsequent lines for text until an empty line or next timestamp
                i += 1
                while i < len(content) and content[i].strip() != '':
                    text_lines.append(content[i].strip())
                    i += 1

                # Create a VTTLine object and add it to the list
                vtt_lines.append(VTTLine(start_time, end_time, '\n'.join(text_lines)))

    return vtt_lines

def save_to_vtt(df, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        # Write VTT header
        f.write("WEBVTT\n\n")

        for index, row in df.iterrows():
            start_time = row['start']
            end_time = row['end']
            text = row['text']

            # Write each subtitle entry
            f.write(f"{start_time} --> {end_time}\n{text}\n\n")

def main():
    # Path to your VTT file
    # vtt_file_path = 'path/to/your/file.vtt'  # Update this path
    vtt_file_path = 'input.vtt'

    # Parse the VTT file
    vtt_lines = parse_vtt(vtt_file_path)

    # Clean the VTT lines and get the DataFrame
    cleaned_df = clean_vtt(vtt_lines)

    # Print the cleaned DataFrame to console
    print(cleaned_df)

    # Save the cleaned DataFrame to a new VTT file
    output_file_path = 'cleaned_subtitles.vtt'  # Specify your desired output file name
    save_to_vtt(cleaned_df, output_file_path)

    print(f"Cleaned subtitles saved to {output_file_path}")

if __name__ == "__main__":
    main()
