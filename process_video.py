# Converts the videos to mp3 
import os 
import subprocess

files = os.listdir("videos") 
import os

# Assuming your files list looks like this based on your input
files = ['brand.mp4', 'money.mp4'] 

# We use 'enumerate' to get a counter (index) along with the file
# start=1 makes the counting start at 1 instead of 0
for index, file in enumerate(files, start=1):
    
    # 1. Get the Tutorial Number (using the loop counter)
    tutorial_number = index
    
    # 2. Get the File Name (by splitting off the .mp4 extension)
    # This splits "brand.mp4" into ["brand", "mp4"] and takes the first part
    file_name = file.split(".")[0] 
    
    # print(tutorial_number,file_name)
    
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{tutorial_number}_{file_name}.mp3"])