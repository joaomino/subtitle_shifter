import re
import argparse
from datetime import timedelta
import os

# Function to convert SRT timestamp to timedelta
def parse_srt_timestamp(timestamp):
    # Split the timestamp into hours, minutes, seconds, and milliseconds
    hours, minutes, seconds, milliseconds = map(int, re.split('[:.,]', timestamp))
    # Return the corresponding timedelta object
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

# Function to convert timedelta back to SRT timestamp
def format_srt_timestamp(td):
    # Get the total number of seconds as an integer
    total_seconds = int(td.total_seconds())
    # Extract the milliseconds from the timedelta
    milliseconds = td.microseconds // 1000
    # Calculate hours, minutes, and seconds from total seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Return the formatted timestamp string in SRT format
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Function to shift subtitles
def shift_subtitles(input_file, shift_seconds):
    # Regular expression to match SRT timestamp lines
    pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")

    # Determine the output file name by appending '_shifted' to the input file's name
    input_filename, input_extension = os.path.splitext(input_file)
    output_file = f"{input_filename}_shifted{input_extension}"

    # Open the input file for reading and the output file for writing
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Check if the line matches the timestamp pattern
            match = pattern.match(line)
            if match:
                # Parse the start and end times from the match groups
                start_time = parse_srt_timestamp(match.group(1))
                end_time = parse_srt_timestamp(match.group(2))

                # Shift the timestamps by the specified number of seconds
                start_time += timedelta(seconds=shift_seconds)
                end_time += timedelta(seconds=shift_seconds)

                # Ensure timestamps do not become negative
                start_time = max(start_time, timedelta(0))
                end_time = max(end_time, timedelta(0))

                # Write the adjusted timestamps to the output file
                outfile.write(f"{format_srt_timestamp(start_time)} --> {format_srt_timestamp(end_time)}\n")
            else:
                # Write lines that are not timestamp lines unchanged
                outfile.write(line)

if __name__ == "__main__":
    # Create an argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="Shift subtitles in an SRT file by adding or removing seconds.")
    # Define the input file argument
    parser.add_argument("input_file", help="Path to the input SRT file.")
    # Define the shift seconds argument (can be positive or negative)
    parser.add_argument("shift_seconds", type=float, help="Number of seconds to shift (positive or negative).")

    # Parse the command-line arguments
    args = parser.parse_args()
    # Call the shift_subtitles function with the provided arguments
    shift_subtitles(args.input_file, args.shift_seconds)
