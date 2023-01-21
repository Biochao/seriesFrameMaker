# Series Frame Maker
Checks a folder for all video files and uses FFMPEG to convert them to frames, separating each episode into its own folder.

## Features:
Creates frames with and without subtitles at the same time

Configurable framerate

Reads season an episode numbers from filenames using regex. By default it's looking for an x inbetween numbers. ie 1x02

Checks for a coresponding subtitle file. If it can't find one it just creates frames without burning in subs

Customizable font and font size for subtitles

Creates a progress.txt file in source folder in case encoding gets interupted. The next time the script is opened it will skip the number of files in progress.txt

## How to Use:

1. set the sources folder

2. Set the output_folder
This is where folders for each episode will be created

3. Configure the output_names
This is the frames naming convention. FFMPEG will name frames based on timestamp in milliseconds. "%08d.jpg" is up to 8 leading zeros.

4. Set your subtitle file format

5. Set the fps

6. Set the font_name and font_size. Use the font family name. This is different from the font file name.

7. Run the script. A progress.txt file will be created in the sources folder incase of crashes.
