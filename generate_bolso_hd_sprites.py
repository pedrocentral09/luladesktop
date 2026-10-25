"""
Generate High-Definition Amarildo Editorial Caricature Sprites for Bolsonaro (Corner Peek).
4 dynamic frames:
- 0: Aiming finger-guns with characteristic smirk
- 1: Recoil firing blast with muzzle flash star, flame and smoke
- 2: Shell ejection spark, smoke drift and recovery
- 3: Re-aiming pose with eyebrow raise
"""
from PIL import Image, ImageDraw
import os

os.makedirs('assets/bolsonaro', exist_ok=True)

# Load base Bolsonaro
bolso = Image.open('assets/hd/bolso_base.png').convert('RGBA')

# Target size for corner widget: 180w x 150h
target_h = 150
target_w = int(bolso.width * (target_h / bolso.height))
bolso_scaled = bolso.resize((target_w, target_h), Image.Resampling.LANCZOS)

CANVAS_W = 210
CANVAS_H = 160
fx = (CANVAS_W - bolso_scaled.width) // 2
fy = CANVAS_H - bolso_scaled.height

# Frame 0: Aiming finger-guns
frame_0 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
frame_0.paste(bolso_scaled, (fx, fy), bolso_scaled)
frame_0.save('assets/bolsonaro/bolsonaro_peek_0.png')

# Frame 1: Firing blast with kickback!
frame_1 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
# Kickback up and back slightly
kick_bolso = bolso_scaled.rotate(2, resample=Image.Resampling.BICUBIC, expand=True)
frame_1.paste(kick_bolso, (fx - 2, fy - 6), kick_bolso)

d1 = ImageDraw.Draw(frame_1)
gx = fx + bolso_scaled.width - 2
gy = fy + 52

# Multi-layered muzzle flash (starburst + core)
d1.line([(gx - 14, gy), (gx + 18, gy)], fill=(255, 240, 50, 255), width=3)
d1.line([(gx, gy - 14), (gx, gy + 14)], fill=(255, 240, 50, 255), width=3)
d1.line([(gx - 8, gy - 8), (gx + 12, gy + 8)], fill=(255, 160, 20, 255), width=2)
d1.line([(gx - 8, gy + 8), (gx + 12, gy - 8)], fill=(255, 160, 20, 255), width=2)
d1.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=(255, 255, 255, 255))
d1.ellipse([gx + 8, gy - 12, gx + 22, gy + 2], fill=(255, 200, 30, 200))
# Cartoon pow text
d1.text((gx + 10, gy - 20), "💥", fill=(255, 180, 0, 255))
frame_1.save('assets/bolsonaro/bolsonaro_peek_1.png')

# Frame 2: Recoil recovery & shell ejection / smoke drift
frame_2 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
frame_2.paste(bolso_scaled, (fx - 1, fy - 2), bolso_scaled)

d2 = ImageDraw.Draw(frame_2)
# Dissipating smoke puffs
d2.ellipse([gx + 14, gy - 18, gx + 26, gy - 6], fill=(220, 220, 220, 160))
d2.ellipse([gx + 22, gy - 26, gx + 36, gy - 12], fill=(240, 240, 240, 120))
# Ejected brass shell spark spinning in air
d2.rounded_rectangle([gx - 18, gy - 24, gx - 10, gy - 16], radius=2, fill=(240, 200, 50, 255), outline=(150, 100, 20, 255))
d2.line([(gx - 14, gy - 28), (gx - 14, gy - 12)], fill=(255, 255, 200, 200), width=1)
frame_2.save('assets/bolsonaro/bolsonaro_peek_2.png')

# Frame 3: Smug re-aiming with slight dip
frame_3 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
frame_3.paste(bolso_scaled, (fx, fy + 1), bolso_scaled)
d3 = ImageDraw.Draw(frame_3)
# Sparkle on teeth / grin
d3.line([(fx + 45, fy + 48), (fx + 51, fy + 48)], fill=(255, 255, 255, 240), width=2)
d3.line([(fx + 48, fy + 45), (fx + 48, fy + 51)], fill=(255, 255, 255, 240), width=2)
frame_3.save('assets/bolsonaro/bolsonaro_peek_3.png')

print("HD Bolsonaro 4-frame sprites generated successfully!")
