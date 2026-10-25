"""
Generate High-Definition Amarildo Editorial Caricature Sprites for Janja's Aerolula.
Creates 4 animated frames with traveling wave banner cloth ripples and engine contrail exhaust.
"""
from PIL import Image, ImageDraw
import os
import math

os.makedirs('assets/plane', exist_ok=True)

# Load base plane
plane = Image.open('assets/hd/plane_base.png').convert('RGBA')

# Target size: width=680, height=int(plane.height * 680 / plane.width)
target_w = 680
target_h = int(plane.height * (target_w / plane.width))
plane_scaled = plane.resize((target_w, target_h), Image.Resampling.LANCZOS)

CANVAS_W = 700
CANVAS_H = target_h + 30
ox = (CANVAS_W - plane_scaled.width) // 2
oy = 15

# Split point between banner and jet: approx x=380 in scaled coordinates
SPLIT_X = 390
STRIP_W = 10

for frame in range(4):
    img = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    phase = frame * (2.0 * math.pi / 4.0)

    # 1. Trailing Banner with traveling harmonic wave
    # Slices from left to right up to SPLIT_X
    for sx in range(0, SPLIT_X, STRIP_W):
        sw = min(STRIP_W, SPLIT_X - sx)
        strip = plane_scaled.crop((sx, 0, sx + sw, plane_scaled.height))
        # Larger amplitude towards the trailing tail (left), damping towards tow line
        amp = 7.0 * (1.0 - (sx / float(SPLIT_X)) * 0.75)
        wave_y = int(amp * math.sin(phase + sx * 0.035))
        img.paste(strip, (ox + sx, oy + wave_y), strip)

    # 2. Jet body (SPLIT_X .. plane_scaled.width)
    jet_strip = plane_scaled.crop((SPLIT_X, 0, plane_scaled.width, plane_scaled.height))
    # Subtle aerodynamic flight pitch / altitude bobbing
    jet_bob = int(math.sin(phase) * 2.0)
    img.paste(jet_strip, (ox + SPLIT_X, oy + jet_bob), jet_strip)

    # 3. Dynamic jet contrails & engine exhaust puffs behind turbines
    d = ImageDraw.Draw(img)
    # Turbine engine exhaust positions (approx x=460, y=oy+jet_bob+230)
    eng_x = ox + int(plane_scaled.width * 0.68)
    eng_y = oy + jet_bob + int(plane_scaled.height * 0.58)

    # White semi-transparent contrail puffs trailing behind jet
    for i in range(3):
        puff_x = eng_x - 30 - i * 35 - (frame * 6)
        puff_y = eng_y + int(math.sin(phase + i) * 3)
        radius = 8 + i * 5
        alpha = max(20, 110 - i * 30)
        d.ellipse([puff_x - radius, puff_y - radius, puff_x + radius, puff_y + radius], fill=(255, 255, 255, alpha))

    # Save frame
    img.save(f'assets/plane/janja_plane_{frame}.png')
    if frame == 0:
        img.save('assets/plane/janja_plane.png')

print("HD Janja Aerolula 4-frame fluttering banner sprites generated successfully!")
