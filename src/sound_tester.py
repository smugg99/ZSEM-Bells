#!/usr/bin/env python3

import os
import tempfile
import time
from pydub import AudioSegment
from pydub.playback import play

# Set the audio player command (use 'aplay' or another player if preferred)
pydub_audio_player = 'aplay'

# Get the parent directory of the script (where your script is located)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to reach the project root directory
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Construct the path to the WAV file in the sounds folder
wav_file_path = os.path.join(project_root, "sounds", "bell_sound.wav")

# Define the duration of the fade-in and fade-out (in milliseconds)
fade_duration = 1000  # 1 second

# Load the WAV file
sound = AudioSegment.from_file(wav_file_path)

# Create a temporary directory for the faded audio
temp_dir = tempfile.mkdtemp()

# Define the path to the temporary audio file
temp_file_path = os.path.join(temp_dir, "temp.wav")

# Create a silent segment of the same duration as the audio
silence = AudioSegment.silent(duration=len(sound))

# Combine the silence (fade-out) with the audio (fade-in)
faded_audio = silence.fade_in(fade_duration) + sound + silence.fade_out(fade_duration)

# Export the faded audio to the temporary file
faded_audio.export(temp_file_path, format="wav")

# Play the faded audio
play(AudioSegment.from_file(temp_file_path))

# Delete the temporary file and directory
os.remove(temp_file_path)
os.rmdir(temp_dir)

print("deezx")
