# subtitle_shifter: A Command-Line Tool for Shifting SRT Timecodes

## Requirements
- Python 3.x (Ensure it's installed on your system)

## How to Use

1. Open your terminal.
2. Run the following command:

   ```bash
   python main.py <filename> <nn>
  
Where:
- `main.py` is the script name.
- `<filename>` is the name of the SRT file you want to modify.
- `<nn>` is the number of seconds to shift the timecodes:
  - Use `-nn` to subtract `nn` seconds.
  - Use `nn` to add `nn` seconds.

## Example

### Add Seconds to Timecodes
To add 5 seconds to the timecodes in `subtitles.srt`, run:

  ```bash
  python main.py subtitles.srt 5
  ```

### Subtract Seconds from Timecodes
To subtract 5 seconds from the timecodes, run:
  ```bash
  python main.py subtitles.srt -5
  ```

## Notes
- Ensure that the SRT file is in the same directory as the script or provide the full path to the file.
- The tool modifies the original SRT file. Consider making a backup before using it.
