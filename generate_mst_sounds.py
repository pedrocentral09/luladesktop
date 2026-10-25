"""
Generate audio effects for MST/CUT Occupation:
- mst_invasion.wav: Wooden mallet stakes hammering (THOK! THOK!) + upbeat militant brass chant
- eviction_alert.wav: Urgent warning siren and 5-second countdown alert beeps
"""
import wave
import struct
import math
import os

os.makedirs('assets/sounds', exist_ok=True)

# 1. MST INVASION (Stakes Hammering + Militant March)
def generate_mst_invasion_sound():
    path = "assets/sounds/mst_invasion.wav"
    sample_rate = 22050
    duration = 3.2
    total_samples = int(sample_rate * duration)

    with wave.open(path, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = bytearray()
        hammer_times = [0.3, 0.9, 1.5, 2.1, 2.7]

        # Brass fanfare notes ("Reforma Agrária Já!")
        # Notes: C4 (261Hz), E4 (329Hz), G4 (392Hz), C5 (523Hz)
        fanfare = [
            (0.1, 0.4, 261.6),
            (0.4, 0.7, 329.6),
            (0.7, 1.1, 392.0),
            (1.1, 1.4, 329.6),
            (1.4, 1.8, 392.0),
            (1.8, 2.4, 523.2),
            (2.4, 3.0, 392.0)
        ]

        for i in range(total_samples):
            t = i / sample_rate
            sample = 0.0

            # 1. Wooden mallet strike on tent stake (THOK!)
            for ht in hammer_times:
                if 0 <= t - ht < 0.22:
                    dt = t - ht
                    # Low punchy wood impact (80-140Hz decaying fast)
                    wood_freq = 110.0 * math.exp(-dt * 35)
                    wood_env = math.exp(-dt * 28)
                    sample += math.sin(2 * math.pi * wood_freq * dt) * wood_env * 0.75
                    # Wood crack click
                    if dt < 0.015:
                        sample += math.sin(2 * math.pi * 850 * dt) * 0.45

            # 2. Brass militant melody
            for n_start, n_end, n_freq in fanfare:
                if n_start <= t < n_end:
                    dt = t - n_start
                    dur = n_end - n_start
                    env = math.sin(math.pi * (dt / dur))
                    tone = (math.sin(2 * math.pi * n_freq * t) +
                            0.45 * math.sin(2 * math.pi * n_freq * 2 * t) +
                            0.20 * math.sin(2 * math.pi * n_freq * 3 * t)) * env
                    sample += tone * 0.35

            # Master envelope
            master_env = 1.0
            if t < 0.05:
                master_env = t / 0.05
            elif t > duration - 0.2:
                master_env = max(0.0, (duration - t) / 0.2)

            val = int(sample * 16000 * master_env)
            val = max(-32767, min(32767, val))
            frames.extend(struct.pack('<h', val))

        wav.writeframes(frames)
    print(f"Generated {path}")

# 2. EVICTION ALERT (5-second countdown alarm)
def generate_eviction_alert_sound():
    path = "assets/sounds/eviction_alert.wav"
    sample_rate = 22050
    duration = 1.8
    total_samples = int(sample_rate * duration)

    with wave.open(path, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = bytearray()
        beeps = [0.1, 0.5, 0.9, 1.3]

        for i in range(total_samples):
            t = i / sample_rate
            sample = 0.0

            # Warning beeps
            for bt in beeps:
                if 0 <= t - bt < 0.25:
                    dt = t - bt
                    freq = 880.0 if bt < 1.0 else 1174.0 # Higher on last
                    env = math.exp(-dt * 12)
                    sample += math.sin(2 * math.pi * freq * dt) * env * 0.7

            val = int(sample * 18000)
            val = max(-32767, min(32767, val))
            frames.extend(struct.pack('<h', val))

        wav.writeframes(frames)
    print(f"Generated {path}")

if __name__ == '__main__':
    generate_mst_invasion_sound()
    generate_eviction_alert_sound()
