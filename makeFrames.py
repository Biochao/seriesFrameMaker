import os
import re
import subprocess

# Set the path to the folder containing the videos
sources = "C:/Users/framebot/bots/sources/Season 01/"
# Set the path to the folder where you want to save the frames
# folders for each source will be created here
output_folder = "C:/Users/framebot/bots/pokemonFrames"
# Output file naming # this sets 0 padding to up to 8
output_names = "%08d.jpg"
# subtitle format
sub = ".srt"
fps = 2.1
# Font family name. This is different from the font file name.
font_name = "Arial"
font_size = 12

# Set the starting index if partially completed and no progress file was made. This is the amount of files in the source folder you want to skip. Set to 0 to do everything.
start_index = 0

# Change the working directory to the sources folder
os.chdir(sources)
# Load the index from a file (or initialize it to 0 if the file doesn't exist)
index_file = "progress.txt"
if os.path.exists(index_file):
    with open(index_file) as f:
        index = int(f.read())
    print("Progress file found. Resuming.")
else:
    index = start_index
    print("No index file found. Starting from the beginning")

#list of video file extensions to look for
extensions = [".mkv", ".mp4", ".m4v"]

# Use the os.listdir() function to get a list of all files in the folder
file_list = os.listdir(sources)
for i, file in enumerate(file_list[index:], start=index):
    if file.endswith(tuple(extensions)):
        print(index+1)
        # Get the file name and extension
        file_name, file_ext = os.path.splitext(file)
        # Set seasonNum, episodeNum, episodeName, and subs variables
        match = re.search(r'(\d+)x(\d+)', file_name)
        if match:
            seasonNum = match.group(1)
            print(f"Season {seasonNum}")
            episodeNum = match.group(2)
            print(f"Season {episodeNum}")
        else:
            print("No episode number match found. Filenames should have an x separating the season number from the episode number.")
        video = file_name + file_ext
        subs = file_name + sub
        episode_folder = f"s{seasonNum}e{episodeNum}"
        episode_folder_subs = episode_folder + "sub"
        os.makedirs(os.path.join(output_folder, episode_folder), exist_ok=True)
        if os.path.isfile(subs) and sub == ".ass" :
            os.makedirs(os.path.join(output_folder, episode_folder_subs), exist_ok=True)
            print(f"Processing {video} with .ass subs")
            subprocess.run(["ffmpeg", "-loglevel", "quiet", "-copyts", "-i", video, "-r", "1000", "-vf", f"fps=fps={fps},ass={subs}", "-frame_pts", "true", "-vsync", "vfr", "-q:v", "1", os.path.join(output_folder, episode_folder_subs, output_names), "-r", "1000", "-vf", f"fps=fps={fps}", "-frame_pts", "true", "-vsync", "vfr", "-q:v", "1", os.path.join(output_folder, episode_folder, output_names)])
        elif os.path.isfile(subs):
            os.makedirs(os.path.join(output_folder, episode_folder_subs), exist_ok=True)
            print(f"Processing {video} with subs")
            subprocess.run(["ffmpeg", "-loglevel", "quiet", "-copyts", "-i", video, "-r", "1000", "-vf", f"fps=fps={fps},subtitles={subs}:force_style='Fontsize={font_size},Fontname={font_name}'", "-frame_pts", "true", "-vsync", "vfr", "-q:v", "1", os.path.join(output_folder, episode_folder_subs, output_names), "-r", "1000", "-vf", f"fps=fps={fps}", "-frame_pts", "true", "-vsync", "vfr", "-q:v", "1", os.path.join(output_folder, episode_folder, output_names)])
        else:
            print(f"Processing {video} no subs")
            subprocess.run(["ffmpeg", "-loglevel", "quiet", "-copyts", "-i", video, "-r", "1000", "-vf", f"fps=fps={fps}", "-frame_pts", "true", "-vsync", "vfr", "-q:v", "1", os.path.join(output_folder, episode_folder, output_names)])
        
        # Increment the index
        index += 1
        # Save progress to text file
        with open("progress.txt", "w") as f:
            f.write(str(index))
os.remove("progress.txt")
