"""
Generate Xandão (Alexandre de Moraes) Sprites and Judicial Gavel Strike Sound.
Minister with black STF judicial robe, shiny bald head with reflection,
golden gavel, arrest warrant, and handcuffs to arrest the user's mouse!
"""
from PIL import Image, ImageDraw, ImageFont
import os
import wave
import struct
import math

def generate_xandao_assets():
    os.makedirs('assets/xandao', exist_ok=True)
    os.makedirs('assets/sounds', exist_ok=True)

    # Sprite dimensions: 180 x 180 px
    width, height = 180, 180

    for frame in range(2):
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        center_x = 90
        # Head center at x=90, y=55
        head_cx = 90
        head_cy = 55
        head_r = 28

        # -------------------------------------------------------------
        # 1. Black STF Judicial Robe (Toga Preta de Ministro)
        # -------------------------------------------------------------
        # Wide shoulders from x=30 to x=150, draped down to y=175
        robe_pts = [
            (center_x - 18, head_cy + 24), # Left neck
            (center_x - 45, head_cy + 34), # Left shoulder
            (center_x - 65, height - 10),  # Left sleeve bottom
            (center_x - 45, height - 8),
            (center_x - 30, height - 2),
            (center_x + 30, height - 2),
            (center_x + 45, height - 8),
            (center_x + 65, height - 10),  # Right sleeve bottom
            (center_x + 45, head_cy + 34), # Right shoulder
            (center_x + 18, head_cy + 24)  # Right neck
        ]
        # Deep black judicial robe with dark satin sheen
        d.polygon(robe_pts, fill=(20, 22, 28, 255), outline=(10, 10, 14, 255), width=2)
        
        # Robe folds / fabric shading
        d.line([(center_x - 12, head_cy + 38), (center_x - 18, height - 10)], fill=(40, 42, 50, 255), width=3)
        d.line([(center_x + 12, head_cy + 38), (center_x + 18, height - 10)], fill=(40, 42, 50, 255), width=3)
        d.line([(center_x, head_cy + 42), (center_x, height - 5)], fill=(35, 38, 45, 255), width=2)

        # White pleated collar / jabot de magistrado (colarinho branco plissado)
        jabot_pts = [
            (center_x - 15, head_cy + 24),
            (center_x + 15, head_cy + 24),
            (center_x + 10, head_cy + 48),
            (center_x, head_cy + 52),
            (center_x - 10, head_cy + 48)
        ]
        d.polygon(jabot_pts, fill=(245, 248, 252, 255), outline=(180, 185, 195, 255))
        # Pleat lines on collar
        d.line([(center_x - 6, head_cy + 26), (center_x - 4, head_cy + 48)], fill=(190, 195, 205, 255), width=1)
        d.line([(center_x, head_cy + 26), (center_x, head_cy + 50)], fill=(190, 195, 205, 255), width=1)
        d.line([(center_x + 6, head_cy + 26), (center_x + 4, head_cy + 48)], fill=(190, 195, 205, 255), width=1)

        # Golden STF Medal / Ribbon
        d.polygon([(center_x - 6, head_cy + 52), (center_x + 6, head_cy + 52), (center_x, head_cy + 60)], fill=(230, 185, 35, 255))
        d.ellipse([center_x - 5, head_cy + 58, center_x + 5, head_cy + 68], fill=(245, 200, 40, 255), outline=(150, 110, 15, 255))

        # -------------------------------------------------------------
        # 2. Xandão's Head & Face (Famosa careca reluzente e olhar firme)
        # -------------------------------------------------------------
        # Neck
        d.rectangle([center_x - 14, head_cy + 15, center_x + 14, head_cy + 26], fill=(240, 198, 168, 255))

        # Head / Bald dome
        d.ellipse([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r], 
                  fill=(248, 208, 178, 255), outline=(140, 95, 65, 255), width=2)

        # Shiny Bald Head Glare / Reflection (O famoso brilho na careca!)
        glare_x = head_cx - 10
        glare_y = head_cy - 18
        # Soft glare glow
        d.ellipse([glare_x - 8, glare_y - 6, glare_x + 14, glare_y + 10], fill=(255, 255, 255, 140))
        # Intense central star/sparkle
        d.ellipse([glare_x - 2, glare_y - 2, glare_x + 6, glare_y + 4], fill=(255, 255, 255, 255))
        # Sparkle cross rays
        d.line([(glare_x + 2, glare_y - 8), (glare_x + 2, glare_y + 10)], fill=(255, 255, 255, 240), width=2)
        d.line([(glare_x - 7, glare_y + 1), (glare_x + 11, glare_y + 1)], fill=(255, 255, 255, 240), width=2)

        # Ears
        d.ellipse([head_cx - head_r - 4, head_cy - 2, head_cx - head_r + 4, head_cy + 14], fill=(242, 195, 165, 255), outline=(140, 95, 65, 255))
        d.ellipse([head_cx + head_r - 4, head_cy - 2, head_cx + head_r + 4, head_cy + 14], fill=(242, 195, 165, 255), outline=(140, 95, 65, 255))

        # Distinctive arched authoritative eyebrows (\  /)
        d.line([head_cx - 19, head_cy - 4, head_cx - 5, head_cy - 1], fill=(25, 20, 15, 255), width=4)
        d.line([head_cx + 19, head_cy - 4, head_cx + 5, head_cy - 1], fill=(25, 20, 15, 255), width=4)

        # Piercing judicial eyes
        d.ellipse([head_cx - 16, head_cy + 2, head_cx - 6, head_cy + 10], fill=(255, 255, 255, 255), outline=(30, 25, 20, 255))
        d.ellipse([head_cx + 6, head_cy + 2, head_cx + 16, head_cy + 10], fill=(255, 255, 255, 255), outline=(30, 25, 20, 255))
        # Dark pupils locked forward
        d.ellipse([head_cx - 12, head_cy + 4, head_cx - 8, head_cy + 8], fill=(15, 15, 20, 255))
        d.ellipse([head_cx + 8, head_cy + 4, head_cx + 12, head_cy + 8], fill=(15, 15, 20, 255))

        # Nose
        d.line([head_cx, head_cy + 3, head_cx - 2, head_cy + 14], fill=(160, 110, 80, 255), width=2)
        d.line([head_cx - 2, head_cy + 14, head_cx + 3, head_cy + 14], fill=(160, 110, 80, 255), width=2)

        # Firm, authoritative mouth
        d.line([head_cx - 10, head_cy + 20, head_cx + 10, head_cy + 20], fill=(120, 50, 40, 255), width=3)
        # Chin cleft / shadow
        d.arc([head_cx - 5, head_cy + 22, head_cx + 5, head_cy + 26], 0, 180, fill=(160, 110, 80, 255), width=2)

        # -------------------------------------------------------------
        # 3. Left Hand: Warrant Paper (MANDADO DO STF)
        # -------------------------------------------------------------
        warrant_x = 22
        warrant_y = 95
        # White document with red wax seal
        d.rectangle([warrant_x, warrant_y, warrant_x + 38, warrant_y + 54], fill=(255, 255, 248, 255), outline=(70, 70, 70, 255), width=2)
        # Text simulation lines on warrant
        d.line([(warrant_x + 4, warrant_y + 8), (warrant_x + 34, warrant_y + 8)], fill=(190, 20, 20, 255), width=2) # "STF"
        d.line([(warrant_x + 4, warrant_y + 16), (warrant_x + 32, warrant_y + 16)], fill=(30, 30, 30, 255), width=1)
        d.line([(warrant_x + 4, warrant_y + 22), (warrant_x + 28, warrant_y + 22)], fill=(30, 30, 30, 255), width=1)
        d.line([(warrant_x + 4, warrant_y + 28), (warrant_x + 34, warrant_y + 28)], fill=(30, 30, 30, 255), width=1)
        # Red wax stamp
        d.ellipse([warrant_x + 12, warrant_y + 36, warrant_x + 26, warrant_y + 50], fill=(210, 25, 25, 255), outline=(130, 10, 10, 255))
        d.text((warrant_x + 15, warrant_y + 37), "⚖️", fill=(255, 255, 255, 255))

        # Left hand fingers holding warrant
        d.ellipse([warrant_x + 26, warrant_y + 26, warrant_x + 42, warrant_y + 40], fill=(245, 202, 172, 255), outline=(140, 95, 65, 255))

        # -------------------------------------------------------------
        # 4. Right Hand: Golden Judicial Gavel (Martelo da Justiça)
        # Frame 0: Gavel raised high (Threatening decision)
        # Frame 1: Gavel struck down onto mouse / anvil (Arrest executed!)
        # -------------------------------------------------------------
        if frame == 0:
            # Gavel Raised High in the air (ready to strike!)
            hand_x = 138
            hand_y = 65
            # Hand
            d.ellipse([hand_x - 6, hand_y - 6, hand_x + 10, hand_y + 10], fill=(245, 202, 172, 255), outline=(140, 95, 65, 255))
            # Wooden handle going up-right
            d.line([(hand_x, hand_y), (hand_x + 22, hand_y - 35)], fill=(130, 80, 40, 255), width=5)
            # Golden hammer head (heavy cylinder)
            gh_cx = hand_x + 24
            gh_cy = hand_y - 38
            d.polygon([
                (gh_cx - 16, gh_cy - 10),
                (gh_cx + 14, gh_cy + 8),
                (gh_cx + 8, gh_cy + 18),
                (gh_cx - 22, gh_cy)
            ], fill=(240, 195, 40, 255), outline=(130, 95, 10, 255), width=2)
            # Gold bands on hammer
            d.line([(gh_cx - 12, gh_cy - 7), (gh_cx - 18, gh_cy + 2)], fill=(255, 240, 120, 255), width=2)
            d.line([(gh_cx + 10, gh_cy + 6), (gh_cx + 4, gh_cy + 15)], fill=(255, 240, 120, 255), width=2)
            # Motion lines
            d.arc([gh_cx - 30, gh_cy - 20, gh_cx + 20, gh_cy + 30], 210, 310, fill=(255, 220, 50, 200), width=2)

        else:
            # Gavel SLAMMED DOWN with impact shockwaves and handcuffs!
            hand_x = 135
            hand_y = 115
            # Hand pressing down
            d.ellipse([hand_x - 8, hand_y - 6, hand_x + 8, hand_y + 10], fill=(245, 202, 172, 255), outline=(140, 95, 65, 255))
            # Handle horizontal/slanted down
            d.line([(hand_x - 4, hand_y + 2), (hand_x + 18, hand_y + 14)], fill=(130, 80, 40, 255), width=5)
            # Gavel head striking table/block at bottom right (x=155, y=142)
            d.rectangle([140, 134, 168, 150], fill=(240, 195, 40, 255), outline=(130, 95, 10, 255), width=2)
            # Sounding block / Anvil underneath
            d.rounded_rectangle([132, 150, 174, 162], radius=3, fill=(100, 60, 30, 255), outline=(60, 35, 15, 255), width=2)

            # Impact Shockwave Sparks (BANG! 💥)
            spark_col = (255, 225, 40, 255)
            d.line([(140, 134), (130, 124)], fill=spark_col, width=2)
            d.line([(154, 132), (154, 118)], fill=spark_col, width=2)
            d.line([(168, 134), (178, 124)], fill=spark_col, width=2)
            d.line([(174, 146), (180, 144)], fill=spark_col, width=2)

            # Handcuffs (Algemas de Prisão do Mouse!)
            # Left cuff
            d.ellipse([116, 136, 134, 154], outline=(190, 195, 205, 255), width=3)
            # Right cuff (locked around mouse area)
            d.ellipse([136, 136, 154, 154], outline=(190, 195, 205, 255), width=3)
            # Connecting chain link
            d.line([(130, 145), (140, 145)], fill=(190, 195, 205, 255), width=2)

        img.save(f'assets/xandao/xandao_{frame}.png')

    print("Xandão sprites successfully generated!")

    # -------------------------------------------------------------
    # 5. Gavel Slam Sound Effect (BANG! + Solemn Court Bass Tone)
    # -------------------------------------------------------------
    sample_rate = 44100
    duration = 1.8
    n_samples = int(sample_rate * duration)

    with wave.open('assets/sounds/xandao_gavel.wav', 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = bytearray()

        for i in range(n_samples):
            t = i / sample_rate
            sample_total = 0.0

            # 1. Heavy Wooden Gavel Impact at t = 0.05
            dt1 = t - 0.05
            if 0 <= dt1 < 0.6:
                # Low boom + punchy wood transient
                boom_freq = 140.0 * math.exp(-dt1 * 18.0)
                boom = math.sin(2 * math.pi * boom_freq * dt1) * math.exp(-dt1 * 12.0)
                # Wood crack transient
                crack = (math.sin(2 * math.pi * 950 * dt1) * 0.4 + math.sin(2 * math.pi * 1600 * dt1) * 0.2) * math.exp(-dt1 * 40.0)
                sample_total += (boom * 0.7 + crack * 0.5)

            # 2. Second Quick Echo/Follow-up Strike at t = 0.35 ("TOC-TOC!")
            dt2 = t - 0.35
            if 0 <= dt2 < 0.5:
                boom_freq2 = 180.0 * math.exp(-dt2 * 20.0)
                boom2 = math.sin(2 * math.pi * boom_freq2 * dt2) * math.exp(-dt2 * 14.0)
                crack2 = math.sin(2 * math.pi * 1100 * dt2) * 0.35 * math.exp(-dt2 * 45.0)
                sample_total += (boom2 * 0.5 + crack2 * 0.4)

            # 3. Metallic Handcuffs Click-Clack at t = 0.70 ("CLINK-CLANK!")
            dt3 = t - 0.70
            if 0 <= dt3 < 0.35:
                metal_freq = 2800.0 * math.exp(-dt3 * 15.0)
                cuff = (math.sin(2 * math.pi * metal_freq * dt3) + 0.3 * math.sin(2 * math.pi * 4200 * dt3)) * math.exp(-dt3 * 30.0)
                sample_total += cuff * 0.45

            # 4. Solemn Law & Order Tone at t = 0.85 (Do-do-do...)
            dt4 = t - 0.85
            if 0 <= dt4 < 0.85:
                tone_freq = 220.0 # A3
                tone = math.sin(2 * math.pi * tone_freq * dt4) * math.exp(-dt4 * 4.0)
                sample_total += tone * 0.3

            # Master envelope
            env = 1.0
            if t > duration - 0.15:
                env = max(0.0, (duration - t) / 0.15)

            val = int(sample_total * 18000 * env)
            val = max(-32767, min(32767, val))
            frames.extend(struct.pack('<h', val))

        wav.writeframes(frames)

    print("Xandão judicial gavel strike audio generated successfully!")

if __name__ == '__main__':
    generate_xandao_assets()
