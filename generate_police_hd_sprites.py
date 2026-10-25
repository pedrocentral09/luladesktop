"""
Generate High-Definition Amarildo Editorial Caricature Sprites for Police Cruiser (Moro & Deltan).
4 dynamic frames:
- 0: Left siren bright red beacon, right dim blue, left grill strobe
- 1: Dual purple strobe flash, Deltan raising PowerPoint diagram (+3px)
- 2: Right siren bright blue beacon, left dim red, right grill strobe
- 3: Full intense double strobe pulse with flashing headlights
"""
from PIL import Image, ImageDraw
import os

os.makedirs('assets/police', exist_ok=True)

# Load base police cruiser
police = Image.open('assets/hd/police_base.png').convert('RGBA')

# Target size: width=320, height=int(police.height * 320 / police.width)
target_w = 320
target_h = int(police.height * (target_w / police.width))
police_scaled = police.resize((target_w, target_h), Image.Resampling.LANCZOS)

CANVAS_W = 340
CANVAS_H = target_h + 20
ox = (CANVAS_W - police_scaled.width) // 2
oy = CANVAS_H - police_scaled.height

siren_cx = ox + int(police_scaled.width * 0.46)
siren_cy = oy + int(police_scaled.height * 0.18)

grill_lx = ox + int(police_scaled.width * 0.88)
grill_ly = oy + int(police_scaled.height * 0.65)
grill_rx = ox + int(police_scaled.width * 0.94)
grill_ry = oy + int(police_scaled.height * 0.68)

for frame in range(4):
    img = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    # Slight chassis vibration (1px)
    chassis_y = oy + (1 if frame % 2 == 1 else 0)
    img.paste(police_scaled, (ox, chassis_y), police_scaled)

    d = ImageDraw.Draw(img)

    if frame == 0:
        # Left Red Bright, Right Blue Dim
        d.ellipse([siren_cx - 30, siren_cy - 16, siren_cx - 2, siren_cy + 12], fill=(255, 30, 30, 140))
        d.ellipse([siren_cx - 22, siren_cy - 10, siren_cx - 8, siren_cy + 6], fill=(255, 50, 50, 255))
        d.ellipse([siren_cx + 8, siren_cy - 8, siren_cx + 18, siren_cy + 4], fill=(30, 80, 200, 180))
        # Left grill strobe white flash
        d.ellipse([grill_lx - 4, grill_ly - 4, grill_lx + 4, grill_ly + 4], fill=(255, 255, 255, 240))

    elif frame == 1:
        # Dual purple / emergency flash
        d.ellipse([siren_cx - 24, siren_cy - 12, siren_cx - 6, siren_cy + 8], fill=(255, 60, 180, 200))
        d.ellipse([siren_cx + 6, siren_cy - 12, siren_cx + 24, siren_cy + 8], fill=(180, 60, 255, 200))
        # PowerPoint diagram glow (where Deltan is holding it)
        ppt_x = ox + int(police_scaled.width * 0.28)
        ppt_y = chassis_y + int(police_scaled.height * 0.42)
        d.ellipse([ppt_x - 12, ppt_y - 12, ppt_x + 12, ppt_y + 12], fill=(255, 240, 50, 120))

    elif frame == 2:
        # Right Blue Bright, Left Red Dim
        d.ellipse([siren_cx - 18, siren_cy - 8, siren_cx - 8, siren_cy + 4], fill=(200, 30, 30, 180))
        d.ellipse([siren_cx + 2, siren_cy - 16, siren_cx + 30, siren_cy + 12], fill=(30, 110, 255, 140))
        d.ellipse([siren_cx + 8, siren_cy - 10, siren_cx + 22, siren_cy + 6], fill=(50, 140, 255, 255))
        # Right grill strobe white flash
        d.ellipse([grill_rx - 4, grill_ry - 4, grill_rx + 4, grill_ry + 4], fill=(255, 255, 255, 240))

    elif frame == 3:
        # Full high-intensity strobe pulse!
        d.ellipse([siren_cx - 32, siren_cy - 18, siren_cx, siren_cy + 14], fill=(255, 255, 255, 160))
        d.ellipse([siren_cx, siren_cy - 18, siren_cx + 32, siren_cy + 14], fill=(255, 255, 255, 160))
        d.ellipse([siren_cx - 22, siren_cy - 10, siren_cx - 8, siren_cy + 6], fill=(255, 40, 40, 255))
        d.ellipse([siren_cx + 8, siren_cy - 10, siren_cx + 22, siren_cy + 6], fill=(40, 120, 255, 255))
        # Both grill strobes
        d.ellipse([grill_lx - 5, grill_ly - 5, grill_lx + 5, grill_ly + 5], fill=(255, 255, 255, 255))
        d.ellipse([grill_rx - 5, grill_ry - 5, grill_rx + 5, grill_ry + 5], fill=(255, 255, 255, 255))

    img.save(f'assets/police/viatura_{frame}.png')

print("HD Police Cruiser 4-frame sprites generated successfully!")
