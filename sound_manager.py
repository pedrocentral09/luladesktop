"""
Sound Manager for Desktop Lula using native Windows winsound.
Plays audio asynchronously without blocking the UI.
"""
import os
import random
import winsound

class SoundManager:
    def __init__(self, sounds_dir="assets/sounds", enabled=True):
        self.sounds_dir = sounds_dir
        self.enabled = enabled

    def play(self, sound_name):
        if not self.enabled:
            return
        
        path = os.path.join(self.sounds_dir, f"{sound_name}.wav")
        if os.path.exists(path):
            try:
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")

    def play_random(self):
        if not self.enabled or not os.path.exists(self.sounds_dir):
            return
        files = [f for f in os.listdir(self.sounds_dir) if f.endswith('.wav')]
        if files:
            chosen = random.choice(files)
            sound_name = os.path.splitext(chosen)[0]
            self.play(sound_name)
