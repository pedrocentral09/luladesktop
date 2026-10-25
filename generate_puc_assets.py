"""
Generate stereotypical PUC University Students Protest Assets:
Caricatured students with protest signs (pro-Lula and anti-Bolsonaro), megaphones,
Stanley cup, tote bags, iPhone, colorful hair, and authentic protest audio!
"""
from PIL import Image, ImageDraw, ImageFont
import os
import wave
import struct
import math

def generate_puc_assets():
    os.makedirs('assets/puc', exist_ok=True)
    os.makedirs('assets/sounds', exist_ok=True)

    # 1. Generate Animated Protest March Sprites (puc_march_0.png and puc_march_1.png)
    # Width: 380, Height: 150
    width, height = 380, 150

    for frame in range(2):
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        leg_shift = 6 if frame == 0 else -6
        arm_bounce = 3 if frame == 0 else -3

        # Ground level is around y=138
        ground_y = 138

        # ==============================================================
        # STUDENT 1: O LÍDER DO D.A. COM MEGAFONE (x: 20 to 95)
        # ==============================================================
        s1_x = 45

        # Legs / Shoes (Converse All-Star)
        d.line([s1_x - 8, ground_y - 25, s1_x - 12 - leg_shift, ground_y], fill=(45, 60, 110, 255), width=6) # Jeans
        d.line([s1_x + 8, ground_y - 25, s1_x + 12 + leg_shift, ground_y], fill=(45, 60, 110, 255), width=6)
        # Red sneakers
        d.rectangle([s1_x - 18 - leg_shift, ground_y - 4, s1_x - 7 - leg_shift, ground_y + 1], fill=(210, 30, 30, 255))
        d.rectangle([s1_x + 7 + leg_shift, ground_y - 4, s1_x + 18 + leg_shift, ground_y + 1], fill=(210, 30, 30, 255))

        # Torso: Linen beige shirt with "D.A. PUC" tote bag strap
        d.rectangle([s1_x - 14, ground_y - 65, s1_x + 14, ground_y - 25], fill=(235, 230, 215, 255), outline=(60, 55, 50, 255))
        # Tote bag strap (brown diagonal)
        d.line([s1_x - 12, ground_y - 64, s1_x + 12, ground_y - 32], fill=(130, 80, 45, 255), width=3)
        # Tote bag at waist (Ecobag com broches)
        d.rectangle([s1_x + 6, ground_y - 42, s1_x + 24, ground_y - 20], fill=(220, 215, 190, 255), outline=(100, 95, 80, 255))
        d.ellipse([s1_x + 10, ground_y - 38, s1_x + 16, ground_y - 32], fill=(220, 30, 30, 255)) # Broche vermelho da estrela
        d.ellipse([s1_x + 17, ground_y - 34, s1_x + 21, ground_y - 30], fill=(40, 160, 60, 255)) # Broche verde

        # Neck & Head
        d.rectangle([s1_x - 4, ground_y - 72, s1_x + 4, ground_y - 65], fill=(240, 200, 165, 255))
        d.ellipse([s1_x - 12, ground_y - 94, s1_x + 12, ground_y - 70], fill=(245, 205, 175, 255)) # Face
        # Hipster beard/stubble
        d.arc([s1_x - 10, ground_y - 88, s1_x + 10, ground_y - 71], 20, 160, fill=(70, 45, 30, 255), width=2)
        # Glasses (round tortoiseshell)
        d.ellipse([s1_x - 9, ground_y - 86, s1_x - 1, ground_y - 78], outline=(50, 30, 20, 255), width=2)
        d.ellipse([s1_x + 1, ground_y - 86, s1_x + 9, ground_y - 78], outline=(50, 30, 20, 255), width=2)
        d.line([s1_x - 1, ground_y - 82, s1_x + 1, ground_y - 82], fill=(50, 30, 20, 255), width=2)
        # Red Che Guevara Beret with yellow star
        d.chord([s1_x - 16, ground_y - 108, s1_x + 17, ground_y - 85], 180, 360, fill=(205, 25, 25, 255), outline=(140, 15, 15, 255))
        d.polygon([(s1_x, ground_y - 100), (s1_x + 3, ground_y - 95), (s1_x - 3, ground_y - 95)], fill=(255, 225, 40, 255)) # Star

        # Megaphone in hand pointing right
        mega_y = ground_y - 60 + arm_bounce
        d.line([s1_x + 6, ground_y - 50, s1_x + 22, mega_y + 4], fill=(240, 200, 165, 255), width=5) # Arm
        # Megaphone cone (white/red)
        d.polygon([(s1_x + 20, mega_y + 2), (s1_x + 44, mega_y - 10), (s1_x + 44, mega_y + 14), (s1_x + 20, mega_y + 6)], fill=(240, 240, 245, 255), outline=(50, 50, 50, 255))
        d.ellipse([s1_x + 40, mega_y - 10, s1_x + 48, mega_y + 14], fill=(225, 30, 30, 255), outline=(50, 50, 50, 255))
        d.rectangle([s1_x + 22, mega_y + 6, s1_x + 27, mega_y + 14], fill=(40, 40, 40, 255)) # Handle
        # Sound waves from megaphone
        wave_col = (230, 40, 40, 220 if frame == 0 else 120)
        d.arc([s1_x + 48, mega_y - 14, s1_x + 62, mega_y + 18], -50, 50, fill=wave_col, width=2)
        d.arc([s1_x + 55, mega_y - 20, s1_x + 75, mega_y + 24], -50, 50, fill=wave_col, width=2)

        # ==============================================================
        # STUDENT 2: A ESTUDANTE DE SOCIAIS COM COPO STANLEY E CARTAZ (x: 105 to 195)
        # ==============================================================
        s2_x = 135

        # Legs / Mom Jeans
        d.line([s2_x - 7, ground_y - 25, s2_x - 11 + leg_shift, ground_y], fill=(100, 135, 175, 255), width=6)
        d.line([s2_x + 7, ground_y - 25, s2_x + 11 - leg_shift, ground_y], fill=(100, 135, 175, 255), width=6)
        # White platform sneakers
        d.rectangle([s2_x - 17 + leg_shift, ground_y - 5, s2_x - 6 + leg_shift, ground_y + 1], fill=(250, 250, 250, 255), outline=(120, 120, 120, 255))
        d.rectangle([s2_x + 6 - leg_shift, ground_y - 5, s2_x + 17 - leg_shift, ground_y + 1], fill=(250, 250, 250, 255), outline=(120, 120, 120, 255))

        # Torso: Red cropped top with "L" and belly button
        d.rectangle([s2_x - 13, ground_y - 65, s2_x + 13, ground_y - 40], fill=(220, 30, 30, 255)) # Red Crop Top
        d.text((s2_x - 5, ground_y - 62), "L", fill=(255, 255, 255, 255))
        d.rectangle([s2_x - 10, ground_y - 40, s2_x + 10, ground_y - 25], fill=(245, 205, 175, 255)) # Midriff exposed
        d.point((s2_x, ground_y - 32), fill=(160, 100, 80, 255)) # Piercing no umbigo

        # Pink / Dyed Hair + Head
        d.ellipse([s2_x - 15, ground_y - 102, s2_x + 15, ground_y - 68], fill=(235, 70, 150, 255)) # Pink hair volume
        # High Messy Bun with green streak
        d.ellipse([s2_x - 9, ground_y - 114, s2_x + 9, ground_y - 96], fill=(235, 70, 150, 255))
        d.ellipse([s2_x - 4, ground_y - 112, s2_x + 4, ground_y - 100], fill=(40, 190, 120, 255)) # Green dye highlight
        # Face
        d.ellipse([s2_x - 11, ground_y - 92, s2_x + 11, ground_y - 70], fill=(245, 205, 175, 255))
        # Round glasses
        d.ellipse([s2_x - 9, ground_y - 85, s2_x - 2, ground_y - 78], outline=(30, 30, 30, 255), width=1)
        d.ellipse([s2_x + 2, ground_y - 85, s2_x + 9, ground_y - 78], outline=(30, 30, 30, 255), width=1)
        d.line([s2_x - 2, ground_y - 81, s2_x + 2, ground_y - 81], fill=(30, 30, 30, 255), width=1)
        # Red lipstick / shouting mouth
        d.ellipse([s2_x - 4, ground_y - 75, s2_x + 4, ground_y - 71], fill=(200, 20, 50, 255))

        # Left hand: Stanley Cup (pastel pink with straw)
        d.line([s2_x - 12, ground_y - 55, s2_x - 22, ground_y - 42], fill=(245, 205, 175, 255), width=4)
        # Stanley tumbler body
        d.polygon([(s2_x - 28, ground_y - 48), (s2_x - 18, ground_y - 48), (s2_x - 20, ground_y - 32), (s2_x - 26, ground_y - 32)], fill=(245, 175, 190, 255), outline=(100, 100, 100, 255))
        d.line([s2_x - 23, ground_y - 48, s2_x - 23, ground_y - 54], fill=(200, 200, 200, 255), width=2) # Straw

        # Right hand raising big Cardboard Protest Sign
        sign_tilt = -2 if frame == 0 else 2
        d.line([s2_x + 10, ground_y - 55, s2_x + 20, ground_y - 92], fill=(245, 205, 175, 255), width=4) # Raised arm
        # Wooden pole
        d.line([s2_x + 20, ground_y - 35, s2_x + 20, ground_y - 138], fill=(145, 100, 60, 255), width=4)
        # Big cardboard sign [ FORA BOLSONARO / iPhone ]
        sign_x = s2_x - 30 + sign_tilt
        sign_y = ground_y - 146
        d.rectangle([sign_x, sign_y, sign_x + 100, sign_y + 46], fill=(225, 195, 150, 255), outline=(70, 50, 35, 255), width=2)
        d.text((sign_x + 6, sign_y + 4), "FORA BOLSONARO!", fill=(185, 20, 20, 255))
        d.text((sign_x + 8, sign_y + 18), "DEMOCRACIA VIVE", fill=(30, 30, 30, 255))
        d.text((sign_x + 5, sign_y + 31), "(via iPhone 15 Pro)", fill=(100, 100, 100, 255))

        # ==============================================================
        # STUDENT 3: O ESTUDANTE 'GRATILUZ' DE LETRAS / ARTES (x: 215 to 295)
        # ==============================================================
        s3_x = 245

        # Legs / Linen Pants
        d.line([s3_x - 7, ground_y - 25, s3_x - 10 - leg_shift, ground_y], fill=(215, 205, 185, 255), width=6)
        d.line([s3_x + 7, ground_y - 25, s3_x + 10 + leg_shift, ground_y], fill=(215, 205, 185, 255), width=6)
        # Leather sandals (Birkenstock)
        d.rectangle([s3_x - 15 - leg_shift, ground_y - 3, s3_x - 5 - leg_shift, ground_y + 1], fill=(95, 60, 35, 255))
        d.rectangle([s3_x + 5 + leg_shift, ground_y - 3, s3_x + 15 + leg_shift, ground_y + 1], fill=(95, 60, 35, 255))

        # Torso: Tie-Dye shirt (rainbow pastel)
        d.rectangle([s3_x - 13, ground_y - 65, s3_x + 13, ground_y - 25], fill=(245, 230, 130, 255), outline=(80, 80, 80, 255))
        d.line([s3_x - 12, ground_y - 50, s3_x + 12, ground_y - 45], fill=(130, 210, 240, 255), width=4)
        d.line([s3_x - 12, ground_y - 35, s3_x + 12, ground_y - 30], fill=(240, 140, 180, 255), width=4)
        # Crystal necklace (Quartzo verde/rosa)
        d.polygon([(s3_x, ground_y - 55), (s3_x + 4, ground_y - 48), (s3_x - 4, ground_y - 48)], fill=(80, 220, 150, 255))

        # Head & Wavy Hair with Bandana
        d.ellipse([s3_x - 14, ground_y - 94, s3_x + 14, ground_y - 68], fill=(90, 55, 30, 255)) # Brown wavy hair
        d.ellipse([s3_x - 11, ground_y - 92, s3_x + 11, ground_y - 70], fill=(240, 200, 165, 255)) # Face
        # Colorful Bandana across forehead
        d.rectangle([s3_x - 13, ground_y - 93, s3_x + 13, ground_y - 86], fill=(230, 160, 40, 255))
        # Eyes with happy/zen expression ^ ^
        d.arc([s3_x - 8, ground_y - 84, s3_x - 2, ground_y - 78], 180, 360, fill=(40, 30, 20, 255), width=2)
        d.arc([s3_x + 2, ground_y - 84, s3_x + 8, ground_y - 78], 180, 360, fill=(40, 30, 20, 255), width=2)
        d.arc([s3_x - 4, ground_y - 76, s3_x + 4, ground_y - 70], 0, 180, fill=(160, 40, 40, 255), width=2) # Smile

        # Holding Yellow Le Creuset Casserole Pan / Pot (Panelaço contra o Bozo!)
        pan_y = ground_y - 48 + arm_bounce
        d.ellipse([s3_x + 10, pan_y - 8, s3_x + 32, pan_y + 12], fill=(235, 180, 20, 255), outline=(120, 80, 10, 255), width=2) # Panela
        d.line([s3_x + 28, pan_y + 2, s3_x + 40, pan_y + 2], fill=(40, 40, 40, 255), width=4) # Cabo da panela
        # Wooden spoon / Colher de pau striking pan
        spoon_angle = 12 if frame == 0 else -18
        d.line([s3_x + 20, pan_y - 20, s3_x + 18 + spoon_angle, pan_y - 2], fill=(160, 110, 60, 255), width=3)
        # Sound spark of panelaço
        if frame == 0:
            d.polygon([(s3_x + 18, pan_y - 14), (s3_x + 14, pan_y - 22), (s3_x + 22, pan_y - 20)], fill=(255, 235, 50, 255))

        # Sign held behind/above: [ MAIS PICANHA / FAZ O L ✨ ]
        d.line([s3_x - 15, ground_y - 45, s3_x - 15, ground_y - 138], fill=(145, 100, 60, 255), width=4)
        sign2_x = s3_x - 55 - sign_tilt
        sign2_y = ground_y - 146
        d.rectangle([sign2_x, sign2_y, sign2_x + 82, sign2_y + 44], fill=(255, 255, 245, 255), outline=(210, 30, 30, 255), width=2)
        d.text((sign2_x + 4, sign2_y + 4), "★ MAIS PICANHA ★", fill=(210, 20, 20, 255))
        d.text((sign2_x + 10, sign2_y + 18), "FAZ O L! ✨", fill=(180, 30, 140, 255))
        d.text((sign2_x + 8, sign2_y + 30), "GRATIDÃO & AMOR", fill=(40, 140, 60, 255))

        # ==============================================================
        # STUDENT 4: O ESTUDANTE COM BANDEIRA OFICIAL DA PUC (x: 310 to 375)
        # ==============================================================
        s4_x = 330

        # Legs / Ripped Jeans
        d.line([s4_x - 7, ground_y - 25, s4_x - 10 + leg_shift, ground_y], fill=(60, 80, 110, 255), width=6)
        d.line([s4_x + 7, ground_y - 25, s4_x + 10 - leg_shift, ground_y], fill=(60, 80, 110, 255), width=6)
        # Vans shoes (black & white checkerboard style)
        d.rectangle([s4_x - 16 + leg_shift, ground_y - 4, s4_x - 5 + leg_shift, ground_y + 1], fill=(25, 25, 25, 255))
        d.rectangle([s4_x + 5 - leg_shift, ground_y - 4, s4_x + 16 - leg_shift, ground_y + 1], fill=(25, 25, 25, 255))

        # Torso: Dark jacket with AirPods Max over ears
        d.rectangle([s4_x - 13, ground_y - 65, s4_x + 13, ground_y - 25], fill=(40, 45, 55, 255), outline=(20, 20, 20, 255))
        d.text((s4_x - 8, ground_y - 50), "PUC", fill=(255, 255, 255, 255))

        # Head & AirPods Max
        d.ellipse([s4_x - 11, ground_y - 92, s4_x + 11, ground_y - 70], fill=(245, 205, 175, 255))
        # Short spiky hair
        d.chord([s4_x - 12, ground_y - 98, s4_x + 12, ground_y - 82], 180, 360, fill=(35, 30, 25, 255))
        # Big Silver Headphones (AirPods Max)
        d.arc([s4_x - 13, ground_y - 98, s4_x + 13, ground_y - 78], 180, 360, fill=(200, 205, 215, 255), width=3) # Headband
        d.ellipse([s4_x - 15, ground_y - 88, s4_x - 10, ground_y - 76], fill=(210, 215, 225, 255), outline=(140, 145, 155, 255))
        d.ellipse([s4_x + 10, ground_y - 88, s4_x + 15, ground_y - 76], fill=(210, 215, 225, 255), outline=(140, 145, 155, 255))

        # Big Official Red Protest Flag Wave (Bandeira da PUC em Luta)
        flag_pole_x = s4_x + 15
        d.line([flag_pole_x, ground_y - 20, flag_pole_x, ground_y - 145], fill=(120, 120, 125, 255), width=4) # Metal pole
        # Red cloth banner flapping
        flag_points = [
            (flag_pole_x, ground_y - 142),
            (flag_pole_x - 45, ground_y - 144 + arm_bounce),
            (flag_pole_x - 45, ground_y - 105 + arm_bounce),
            (flag_pole_x, ground_y - 105)
        ]
        d.polygon(flag_points, fill=(215, 25, 25, 255), outline=(160, 15, 15, 255))
        d.text((flag_pole_x - 42, ground_y - 138 + arm_bounce), "★ PUC ★", fill=(255, 225, 50, 255))
        d.text((flag_pole_x - 43, ground_y - 122 + arm_bounce), "EM LUTA!", fill=(255, 255, 255, 255))

        img.save(f'assets/puc/puc_march_{frame}.png')

    print("PUC University students sprites successfully generated!")

    # 2. Generate Authentic Student Protest Sound (Whistle + Panelaço + Chants)
    # 44100Hz, ~2.8 seconds
    sample_rate = 44100
    duration = 2.8
    n_samples = int(sample_rate * duration)

    with wave.open('assets/sounds/protesto_puc.wav', 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = bytearray()

        for i in range(n_samples):
            t = i / sample_rate

            sample_total = 0.0

            # A. Manifestation Whistle (Apito tritonal agudo: ~2400Hz com trêmolo)
            # Apito toca nos primeiros 0.8s e depois entre 1.4s e 2.0s
            is_whistling = (0.05 < t < 0.75) or (1.4 < t < 2.1)
            if is_whistling:
                tremolo = 1.0 + 0.15 * math.sin(2 * math.pi * 32 * t)
                whistle_freq = 2450 * tremolo
                whistle_sample = math.sin(2 * math.pi * whistle_freq * t) + 0.3 * math.sin(2 * math.pi * whistle_freq * 1.5 * t)
                sample_total += whistle_sample * 0.45

            # B. Panelaço / Batucada (Yellow Le Creuset Pot beats: "TOC... TOC... TOC-TOC-TOC")
            beat_times = [0.1, 0.5, 0.9, 1.3, 1.5, 1.8, 2.2, 2.4]
            for bt in beat_times:
                dt = t - bt
                if 0 <= dt < 0.12:
                    pan_freq = 920.0 * math.exp(-dt * 30) # Metallic ring
                    pan_env = math.exp(-dt * 25)
                    pan_sound = (math.sin(2 * math.pi * pan_freq * dt) + 0.4 * math.sin(2 * math.pi * pan_freq * 2.2 * dt)) * pan_env
                    sample_total += pan_sound * 0.5

            # C. Melodia de Protesto ("Olê, Olê, Olê, Olá... Lula, Lula!")
            # Notes: E4 (330Hz), G4 (392Hz), A4 (440Hz), B4 (493Hz)
            # Chanted by students in festive sync
            chant_notes = [
                (0.2, 0.45, 392.0), # O-
                (0.45, 0.7, 440.0), # lê
                (0.7, 1.0, 392.0),  # o-
                (1.0, 1.3, 440.0),  # lê
                (1.3, 1.55, 330.0), # o-
                (1.55, 1.85, 349.0),# lá
                (1.9, 2.3, 440.0),  # Lu-
                (2.3, 2.7, 392.0)   # lá!
            ]
            for n_start, n_end, n_freq in chant_notes:
                if n_start <= t < n_end:
                    dt = t - n_start
                    dur = n_end - n_start
                    env = math.sin(math.pi * (dt / dur))
                    # Warm choir/brass synth tone
                    chant_tone = (math.sin(2 * math.pi * n_freq * t) + 
                                  0.5 * math.sin(2 * math.pi * (n_freq * 2) * t) +
                                  0.25 * math.sin(2 * math.pi * (n_freq * 3) * t)) * env
                    sample_total += chant_tone * 0.4

            # Master envelope
            env_master = 1.0
            if t < 0.1:
                env_master = t / 0.1
            elif t > duration - 0.2:
                env_master = max(0.0, (duration - t) / 0.2)

            val = int(sample_total * 14000 * env_master)
            val = max(-32767, min(32767, val))
            frames.extend(struct.pack('<h', val))

        wav.writeframes(frames)

    print("PUC Student protest audio generated!")

if __name__ == '__main__':
    generate_puc_assets()
