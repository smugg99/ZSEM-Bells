#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.playback import play
import os

# Set the audio player command (use 'aplay' or another player if preferred)
pydub_audio_player = 'aplay'

# Get the parent directory of the script (where your script is located)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to reach the project root directory
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Construct the path to the WAV file in the sounds folder
wav_file_path = os.path.join(project_root, "sounds", "bell_sound.wav")

# Load the WAV file
sound = AudioSegment.from_file(wav_file_path)

# Set the volume (0.0 to 1.0, adjust as needed)
volume = 0.5
sound = sound - 30 * (1 - volume)  # Adjust volume level

# Play the modified audio using 'aplay' or the chosen player
sound.export(os.path.join(script_dir, "temp.wav"), format="wav")  # Export the audio to a temporary file
os.system(f"{pydub_audio_player} {os.path.join(script_dir, 'temp.wav')}")  # Play the temporary file

print("deezx")
