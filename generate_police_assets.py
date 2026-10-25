"""
Generate Police Cruiser with Sergio Moro and Deltan Dallagnol, plus police siren sound.
"""
from PIL import Image, ImageDraw
import os
import wave
import struct
import math

def generate_police_assets():
    os.makedirs('assets/police', exist_ok=True)
    os.makedirs('assets/sounds', exist_ok=True)

    # 1. Police Cruiser (Viatura da PF) with Moro and Deltan
    # 2 frames to animate siren lights (red/blue alternating)
    width, height = 260, 95

    for frame in range(2):
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        # Car dimensions
        # Wheels at y=68
        # Chassis from x=15 to x=245
        
        # Cabin / Windows
        # Cabin roof at y=25, bottom at y=50
        d.polygon([(65, 25), (175, 25), (205, 50), (45, 50)], fill=(30, 32, 40, 255), outline=(15, 15, 20, 255))
        # Window glass (light blue tinted)
        d.polygon([(70, 28), (120, 28), (120, 48), (55, 48)], fill=(120, 160, 200, 220)) # Rear window (Deltan)
        d.polygon([(125, 28), (170, 28), (198, 48), (125, 48)], fill=(120, 160, 200, 220)) # Front window (Moro)

        # PASSENGER 1: SÉRGIO MORO (Front window, x=135..185)
        # Slicked dark hair
        d.chord([140, 24, 168, 42], 180, 360, fill=(20, 22, 28, 255))
        # Face (stern look)
        d.ellipse([142, 29, 164, 46], fill=(240, 195, 165, 255))
        # Eyes with serious brow
        d.line([145, 34, 152, 35], fill=(20, 20, 20, 255), width=2)
        d.line([156, 35, 163, 34], fill=(20, 20, 20, 255), width=2)
        d.point((148, 37), fill=(20, 20, 20, 255))
        d.point((159, 37), fill=(20, 20, 20, 255))
        # Stern straight mouth
        d.line([148, 43, 158, 43], fill=(80, 40, 40, 255), width=1)
        # Black Judge Suit & dark tie
        d.rectangle([138, 46, 170, 52], fill=(20, 22, 28, 255))
        d.polygon([(152, 46), (156, 46), (154, 52)], fill=(180, 20, 20, 255)) # tie

        # PASSENGER 2: DELTAN DALLAGNOL (Rear window, x=75..115)
        # Brown neat hair
        d.chord([80, 25, 104, 40], 180, 360, fill=(70, 45, 25, 255))
        # Face
        d.ellipse([82, 30, 102, 46], fill=(245, 205, 175, 255))
        # Wireframe Glasses
        d.ellipse([85, 34, 91, 40], outline=(40, 40, 40, 255), width=1)
        d.ellipse([93, 34, 99, 40], outline=(40, 40, 40, 255), width=1)
        d.line([91, 37, 93, 37], fill=(40, 40, 40, 255), width=1)
        # Mini PowerPoint diagram in Deltan's hand!
        # White paper with red center circle & arrows
        d.rectangle([60, 32, 80, 49], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
        d.ellipse([67, 38, 73, 44], fill=(220, 20, 20, 255)) # "Lula" center circle!
        d.line([64, 35, 68, 39], fill=(30, 30, 180, 255), width=1)
        d.line([75, 35, 71, 39], fill=(30, 30, 180, 255), width=1)
        d.line([70, 45, 70, 48], fill=(30, 30, 180, 255), width=1)

        # Siren Lightbar on roof (x=110..135, y=16..24)
        d.rectangle([112, 22, 134, 25], fill=(80, 80, 80, 255)) # Siren base
        siren_left_color = (240, 20, 20, 255) if frame == 0 else (20, 80, 240, 255)
        siren_right_color = (20, 80, 240, 255) if frame == 0 else (240, 20, 20, 255)
        
        # Left siren light + glow
        d.rounded_rectangle([110, 15, 122, 23], radius=3, fill=siren_left_color)
        d.ellipse([104, 9, 128, 28], fill=(siren_left_color[0], siren_left_color[1], siren_left_color[2], 90))
        # Right siren light + glow
        d.rounded_rectangle([124, 15, 136, 23], radius=3, fill=siren_right_color)
        d.ellipse([118, 9, 142, 28], fill=(siren_right_color[0], siren_right_color[1], siren_right_color[2], 90))

        # Main Car Body (Federal Police SUV - Black & Silver with Gold emblem)
        d.rounded_rectangle([20, 45, 235, 72], radius=6, fill=(35, 38, 48, 255), outline=(20, 22, 26, 255), width=2)
        # Hood / Front bumper slope
        d.polygon([(205, 50), (242, 58), (242, 70), (205, 70)], fill=(35, 38, 48, 255))
        # Front grill & headlights
        d.rectangle([238, 57, 244, 65], fill=(255, 250, 200, 255)) # Headlight
        # Yellow stripe & POLÍCIA FEDERAL text
        d.rectangle([25, 55, 230, 60], fill=(215, 165, 25, 255))
        d.text((45, 60), "POLICIA FEDERAL", fill=(255, 255, 255, 255))
        d.text((170, 60), "LAVA-JATO", fill=(255, 220, 40, 255))

        # Wheels (x=55 and x=195, y=72)
        # Left Wheel
        d.ellipse([45, 62, 75, 92], fill=(25, 25, 30, 255), outline=(10, 10, 12, 255), width=2)
        d.ellipse([53, 70, 67, 84], fill=(180, 185, 195, 255)) # Rim
        # Right Wheel
        d.ellipse([180, 62, 210, 92], fill=(25, 25, 30, 255), outline=(10, 10, 12, 255), width=2)
        d.ellipse([188, 70, 202, 84], fill=(180, 185, 195, 255)) # Rim

        img.save(f'assets/police/viatura_{frame}.png')

    print("Police cruiser sprites generated!")

    # 2. Siren Sound (Two-tone wailing siren: wee-woo-wee-woo)
    sample_rate = 44100
    duration = 2.4
    n_samples = int(sample_rate * duration)
    with wave.open('assets/sounds/police_siren.wav', 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            # Siren frequency oscillation between 650Hz and 950Hz
            cycle = (t * 2.2) % 1.0 # ~2.2 sweeps per second
            freq = 650 + 320 * (0.5 + 0.5 * math.sin(2 * math.pi * cycle))
            sample_val = math.sin(2 * math.pi * freq * t)
            # Envelope (fade in and fade out)
            env = 1.0
            if t < 0.2:
                env = t / 0.2
            elif t > duration - 0.3:
                env = max(0.0, (duration - t) / 0.3)
            val = int(sample_val * 16000 * env)
            frames.extend(struct.pack('<h', val))
        wav.writeframes(frames)

    print("Police siren sound generated!")

if __name__ == '__main__':
    generate_police_assets()
