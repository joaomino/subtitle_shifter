import re
import argparse
from datetime import timedelta
import os

# Função para converter timestamp SRT para timedelta
def parse_srt_timestamp(timestamp):
    hours, minutes, seconds, milliseconds = map(int, re.split('[:.,]', timestamp))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

# Função para converter timedelta para timestamp SRT
def format_srt_timestamp(td):
    total_seconds = int(td.total_seconds())
    milliseconds = td.microseconds // 1000
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Função para ajustar as legendas
def shift_subtitles(input_file, shift_seconds):
    pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")

    # Parte do nome indicando o deslocamento
    variation = f"{'plus' if shift_seconds >= 0 else 'minus'}{abs(int(shift_seconds))}s"

    input_filename, input_extension = os.path.splitext(input_file)
    output_file = f"{input_filename}_{variation}{input_extension}"

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            match = pattern.match(line)
            if match:
                start_time = parse_srt_timestamp(match.group(1))
                end_time = parse_srt_timestamp(match.group(2))

                start_time += timedelta(seconds=shift_seconds)
                end_time += timedelta(seconds=shift_seconds)

                start_time = max(start_time, timedelta(0))
                end_time = max(end_time, timedelta(0))

                outfile.write(f"{format_srt_timestamp(start_time)} --> {format_srt_timestamp(end_time)}\n")
            else:
                outfile.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shift all SRT files in the 'files' directory.")
    parser.add_argument("shift_seconds", type=float, help="Number of seconds to shift (positive or negative).")
    args = parser.parse_args()

    input_dir = "files"
    for filename in os.listdir(input_dir):
        if filename.endswith(".srt"):
            full_path = os.path.join(input_dir, filename)
            print(f"Processing: {filename}")
            shift_subtitles(full_path, args.shift_seconds)