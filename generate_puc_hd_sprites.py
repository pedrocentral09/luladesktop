"""
Generate High-Definition Amarildo Editorial Caricature Sprites for PUC Students Protest.
4 dynamic frames:
- 0: Base stride, megaphone shouting with concentric soundwave arcs
- 1: Marching cadence bounce (+3px), panelaço impact spark explosion
- 2: Alternate stride, protest sign sway, chanting musical notes
- 3: High cadence bounce (+2px), panelaço recovery, Stanley cup sparkle
"""
from PIL import Image, ImageDraw
import os
import math

os.makedirs('assets/puc', exist_ok=True)

# Load base PUC students
puc = Image.open('assets/hd/puc_base.png').convert('RGBA')

# Target size: width=460, height=int(puc.height * 460 / puc.width)
target_w = 460
target_h = int(puc.height * (target_w / puc.width))
puc_scaled = puc.resize((target_w, target_h), Image.Resampling.LANCZOS)

CANVAS_W = 480
CANVAS_H = target_h + 25
ox = (CANVAS_W - puc_scaled.width) // 2
oy = CANVAS_H - puc_scaled.height

mega_x = ox + int(puc_scaled.width * 0.18)
mega_y = oy + int(puc_scaled.height * 0.38)
pan_x = ox + int(puc_scaled.width * 0.62)
pan_y = oy + int(puc_scaled.height * 0.48)
cup_x = ox + int(puc_scaled.width * 0.44)
cup_y = oy + int(puc_scaled.height * 0.52)

# Frame 0: Base stride + megaphone concentric soundwaves
f0 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
f0.paste(puc_scaled, (ox, oy), puc_scaled)
d0 = ImageDraw.Draw(f0)
d0.arc([mega_x - 14, mega_y - 22, mega_x + 14, mega_y + 22], -60, 60, fill=(230, 40, 40, 220), width=2)
d0.arc([mega_x - 22, mega_y - 32, mega_x + 22, mega_y + 32], -60, 60, fill=(230, 40, 40, 170), width=2)
d0.arc([mega_x - 30, mega_y - 42, mega_x + 30, mega_y + 42], -60, 60, fill=(230, 40, 40, 110), width=2)
f0.save('assets/puc/puc_march_0.png')

# Frame 1: Marching cadence bounce (+3px) + panelaço impact spark!
f1 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
f1.paste(puc_scaled, (ox, oy - 4), puc_scaled)
d1 = ImageDraw.Draw(f1)
spark_col = (255, 230, 40, 255)
d1.line([(pan_x - 8, pan_y - 16), (pan_x - 18, pan_y - 28)], fill=spark_col, width=2)
d1.line([(pan_x + 2, pan_y - 18), (pan_x + 6, pan_y - 32)], fill=spark_col, width=2)
d1.line([(pan_x + 12, pan_y - 14), (pan_x + 24, pan_y - 24)], fill=spark_col, width=2)
d1.text((pan_x - 4, pan_y - 32), "💥", fill=(255, 200, 0, 255))
f1.save('assets/puc/puc_march_1.png')

# Frame 2: Alternate stride + sign sway + chanting musical note
f2 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
# Slight horizontal sway (1px)
f2.paste(puc_scaled, (ox + 1, oy - 1), puc_scaled)
d2 = ImageDraw.Draw(f2)
d2.text((mega_x - 10, mega_y - 35), "🎶", fill=(220, 30, 30, 240))
d2.text((mega_x + 15, mega_y - 45), "🎵", fill=(220, 30, 30, 200))
f2.save('assets/puc/puc_march_2.png')

# Frame 3: Marching bounce (+2px) + Stanley cup glint
f3 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
f3.paste(puc_scaled, (ox - 1, oy - 3), puc_scaled)
d3 = ImageDraw.Draw(f3)
# Stanley cup sparkle
d3.line([(cup_x - 6, cup_y), (cup_x + 6, cup_y)], fill=(255, 255, 255, 240), width=2)
d3.line([(cup_x, cup_y - 6), (cup_x, cup_y + 6)], fill=(255, 255, 255, 240), width=2)
d3.ellipse([cup_x - 2, cup_y - 2, cup_x + 2, cup_y + 2], fill=(255, 255, 255, 255))
f3.save('assets/puc/puc_march_3.png')

print("HD PUC Students 4-frame sprites generated successfully!")
