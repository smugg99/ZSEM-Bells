#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.playback import play

# Load the WAV file
sound = AudioSegment.from_file("/ZSEM-Bells/sounds/bell_sound.wav")

# Set the volume (0.0 to 1.0, adjust as needed)
volume = 0.5
sound = sound - 30 * (1 - volume)  # Adjust volume level

# Play the modified audio
play(sound)

print("deezx")