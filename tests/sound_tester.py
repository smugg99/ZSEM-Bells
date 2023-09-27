#!/usr/bin/env python3

import os

script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, ".."))
wav_file_path = os.path.join(project_root, "sounds", "bell_sound.wav")

audio_device = "hw:0,0"

aplay_command = f"aplay -D {audio_device} {wav_file_path}"

os.system(aplay_command)