"""
Generate Bolsonaro peek-a-boo sprite doing finger guns (arminha) and sound effect.
"""
from PIL import Image, ImageDraw
import os
import wave
import struct
import math

def generate_bolsonaro():
    os.makedirs('assets/bolsonaro', exist_ok=True)
    os.makedirs('assets/sounds', exist_ok=True)

    # Sprite dimensions: 128 x 140 px
    w, h = 128, 140

    for frame in range(2):
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        # Center x = 64, Base y = 140
        recoil = 2 if frame == 1 else 0

        # Colors
        SKIN = (245, 195, 165, 255)
        HAIR_GRAY = (90, 95, 100, 255)
        HAIR_DARK = (45, 50, 55, 255)
        JERSEY_YELLOW = (255, 220, 0, 255)
        JERSEY_GREEN = (0, 140, 50, 255)
        BLUE = (30, 60, 150, 255)
        WHITE = (255, 255, 255, 255)
        BLACK = (20, 20, 20, 255)

        # Torso: Yellow Brazil Jersey (Camisa da Seleção)
        torso_top = 70 + recoil
        d.rounded_rectangle([28, torso_top, 100, 140], radius=8, fill=JERSEY_YELLOW, outline=(200, 170, 0, 255), width=2)
        # Green V-collar
        d.polygon([(52, torso_top), (76, torso_top), (64, torso_top + 14)], fill=JERSEY_GREEN)
        d.polygon([(56, torso_top), (72, torso_top), (64, torso_top + 10)], fill=SKIN)
        # Number 22 or CBF badge on chest
        d.rectangle([40, torso_top + 16, 52, torso_top + 30], fill=JERSEY_GREEN)
        d.text((43, torso_top + 18), "BR", fill=WHITE)

        # Head Base & Neck
        neck_top = torso_top - 10
        d.rectangle([56, neck_top, 72, torso_top + 2], fill=SKIN)

        head_y = 28 + recoil
        # Face
        d.ellipse([42, head_y, 86, head_y + 44], fill=SKIN)
        # Chin/Jawline shape
        d.polygon([(46, head_y + 25), (82, head_y + 25), (74, head_y + 44), (54, head_y + 44)], fill=SKIN)

        # Hair (Dark gray side-combed hair)
        # Hair top
        d.chord([40, head_y - 8, 88, head_y + 22], 180, 360, fill=HAIR_GRAY)
        # Side part & hairline
        d.polygon([(40, head_y + 8), (46, head_y - 6), (84, head_y - 6), (88, head_y + 12), (80, head_y + 2), (50, head_y + 2)], fill=HAIR_DARK)

        # Eyes & Eyebrows
        # Left brow & eye
        d.line([48, head_y + 14, 58, head_y + 15], fill=HAIR_DARK, width=2)
        d.rectangle([50, head_y + 17, 56, head_y + 21], fill=BLACK)
        d.point((52, head_y + 18), fill=WHITE)
        # Right brow & eye (slight wink / squint!)
        d.line([70, head_y + 15, 80, head_y + 14], fill=HAIR_DARK, width=2)
        d.rectangle([72, head_y + 17, 78, head_y + 21], fill=BLACK)
        d.point((74, head_y + 18), fill=WHITE)

        # Nose
        d.polygon([(62, head_y + 18), (66, head_y + 28), (60, head_y + 28)], fill=(215, 165, 135, 255))

        # Smile (wide grin: "Taokey?!")
        d.arc([54, head_y + 28, 74, head_y + 38], 0, 180, fill=BLACK, width=2)
        d.chord([56, head_y + 30, 72, head_y + 36], 0, 180, fill=WHITE)

        # ARMS DOING THE FINGER GUN GESTURE (ARMINHA 👉 👉)
        # Left Arm & Hand (pointing upward-right)
        arm_l_x = 18
        arm_l_y = torso_top + 10
        # Sleeve
        d.rectangle([arm_l_x + 8, arm_l_y, arm_l_x + 20, arm_l_y + 14], fill=JERSEY_YELLOW)
        d.rectangle([arm_l_x + 8, arm_l_y + 12, arm_l_x + 20, arm_l_y + 15], fill=JERSEY_GREEN)
        # Arm reaching up
        d.polygon([(arm_l_x + 10, arm_l_y + 14), (arm_l_x + 6, arm_l_y - 12), 
                   (arm_l_x + 16, arm_l_y - 12), (arm_l_x + 18, arm_l_y + 14)], fill=SKIN)
        # Left Hand Finger Gun: thumb up, index finger pointing up-left!
        hand_l_x = arm_l_x + 6
        hand_l_y = arm_l_y - 20 - recoil
        # Fist
        d.ellipse([hand_l_x, hand_l_y + 6, hand_l_x + 12, hand_l_y + 18], fill=SKIN)
        # Thumb pointing up (the hammer)
        d.rectangle([hand_l_x + 6, hand_l_y, hand_l_x + 10, hand_l_y + 8], fill=SKIN)
        # Index finger pointing out (the barrel 👉)
        d.rectangle([hand_l_x - 10, hand_l_y + 6, hand_l_x + 2, hand_l_y + 10], fill=SKIN)

        # Right Arm & Hand (pointing upward-right 👉)
        arm_r_x = 90
        arm_r_y = torso_top + 10
        # Sleeve
        d.rectangle([arm_r_x, arm_r_y, arm_r_x + 12, arm_r_y + 14], fill=JERSEY_YELLOW)
        d.rectangle([arm_r_x, arm_r_y + 12, arm_r_x + 12, arm_r_y + 15], fill=JERSEY_GREEN)
        # Arm reaching up
        d.polygon([(arm_r_x + 2, arm_r_y + 14), (arm_r_x + 4, arm_l_y - 12), 
                   (arm_r_x + 14, arm_l_y - 12), (arm_r_x + 10, arm_r_y + 14)], fill=SKIN)
        # Right Hand Finger Gun: thumb up, index finger pointing out 👉
        hand_r_x = arm_r_x + 4
        hand_r_y = arm_l_y - 20 - recoil
        # Fist
        d.ellipse([hand_r_x, hand_r_y + 6, hand_r_x + 12, hand_r_y + 18], fill=SKIN)
        # Thumb up
        d.rectangle([hand_r_x + 2, hand_r_y, hand_r_x + 6, hand_r_y + 8], fill=SKIN)
        # Index finger pointing right 👉
        d.rectangle([hand_r_x + 10, hand_r_y + 6, hand_r_x + 22, hand_r_y + 10], fill=SKIN)

        # Sparkle / Flash on finger tips when recoiling (frame 1)
        if frame == 1:
            # Left sparkle
            d.line([hand_l_x - 14, hand_l_y + 8, hand_l_x - 10, hand_l_y + 8], fill=(255, 230, 50, 255), width=2)
            d.line([hand_l_x - 12, hand_l_y + 6, hand_l_x - 12, hand_l_y + 10], fill=(255, 230, 50, 255), width=2)
            # Right sparkle
            d.line([hand_r_x + 22, hand_r_y + 8, hand_r_x + 26, hand_r_y + 8], fill=(255, 230, 50, 255), width=2)
            d.line([hand_r_x + 24, hand_r_y + 6, hand_r_x + 24, hand_r_y + 10], fill=(255, 230, 50, 255), width=2)

        img.save(f'assets/bolsonaro/bolsonaro_peek_{frame}.png')

    print("Bolsonaro peek sprites generated successfully!")

    # Sound effect: double finger-gun click + pop (pew-pew / click-click)
    sample_rate = 44100
    duration = 0.55
    n_samples = int(sample_rate * duration)
    with wave.open('assets/sounds/arminha.wav', 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            # Two clicks/pops at t=0.05 and t=0.28
            val = 0
            for pop_t in [0.05, 0.28]:
                dt = t - pop_t
                if 0 <= dt < 0.12:
                    # Pitch drops sharply from 900 to 200
                    p_freq = 800 - 4000 * dt
                    p_freq = max(150, p_freq)
                    env = math.exp(-35 * dt)
                    val += math.sin(2 * math.pi * p_freq * dt) * env
            val = max(-1.0, min(1.0, val))
            sample = int(val * 16000)
            frames.extend(struct.pack('<h', sample))
        wav.writeframes(frames)
    print("Arminha sound generated successfully!")

if __name__ == '__main__':
    generate_bolsonaro()
