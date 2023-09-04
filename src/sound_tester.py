#!/usr/bin/env python3

import os

# Get the parent directory of the script (where your script is located)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to reach the project root directory
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Construct the path to the WAV file in the sounds folder
wav_file_path = os.path.join(project_root, "sounds", "bell_sound.wav")

# Define the audio device you want to use (replace "hw:0,0" with the appropriate device identifier)
audio_device = "hw:0,0"

# Create the aplay command with the specified audio device
aplay_command = f"aplay -D {audio_device} {wav_file_path}"

# Play the WAV file using aplay
os.system(aplay_command)
