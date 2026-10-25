"""
Generate Dynamic HD Sprites for MST & CUT Occupation and Tent Building Animation.
Generates:
- 4 frames of MST Pitching / Chanting (assets/mst/mst_pitch_0.png to 3.png)
- 4 frames of MST Panic Fleeing (assets/mst/mst_flee_0.png to 3.png)
- 5 stages of animated tent construction (assets/mst/tent_stage_0.png to 4.png + collapse.png)
"""
from PIL import Image, ImageDraw, ImageFilter
import os
import math

os.makedirs('assets/mst', exist_ok=True)

# -------------------------------------------------------------------------
# 1. GENERATE MILITANTS PITCHING FRAMES (assets/mst/mst_pitch_0..3.png)
# -------------------------------------------------------------------------
pitch_base = Image.open('assets/hd/mst_pitch_base.png').convert('RGBA')

# Scaled dimensions for on-screen parade/occupation widget
TARGET_W = 460
TARGET_H = int(pitch_base.height * (TARGET_W / pitch_base.width))
pitch_scaled = pitch_base.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

CANVAS_W = 480
CANVAS_H = TARGET_H + 25
ox = (CANVAS_W - pitch_scaled.width) // 2
oy = CANVAS_H - pitch_scaled.height

# Approximate positions of features
mallet_x = ox + int(pitch_scaled.width * 0.28)
mallet_y = oy + int(pitch_scaled.height * 0.58)
flag_x = ox + int(pitch_scaled.width * 0.72)
flag_y = oy + int(pitch_scaled.height * 0.22)
mega_x = ox + int(pitch_scaled.width * 0.85)
mega_y = oy + int(pitch_scaled.height * 0.40)
pot_x = ox + int(pitch_scaled.width * 0.12)
pot_y = oy + int(pitch_scaled.height * 0.80)

# Frame 0: Base stance + rising campfire smoke from iron pot
f0 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
f0.paste(pitch_scaled, (ox, oy), pitch_scaled)
d0 = ImageDraw.Draw(f0)
# Smoke puff 1
d0.ellipse([pot_x - 6, pot_y - 20, pot_x + 6, pot_y - 10], fill=(220, 220, 220, 160))
d0.ellipse([pot_x - 3, pot_y - 34, pot_x + 11, pot_y - 22], fill=(220, 220, 220, 120))
d0.ellipse([pot_x + 2, pot_y - 48, pot_x + 18, pot_y - 34], fill=(220, 220, 220, 80))
f0.save('assets/mst/mst_pitch_0.png')

# Frame 1: Mallet strike impact (POW! + sparks) + flag wave + campfire smoke
f1 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
# Cadence bounce (-3px)
f1.paste(pitch_scaled, (ox, oy - 3), pitch_scaled)
d1 = ImageDraw.Draw(f1)
# Hammer impact spark on ground stake
spark_col = (255, 230, 40, 255)
d1.line([(mallet_x, mallet_y), (mallet_x - 12, mallet_y - 12)], fill=spark_col, width=2)
d1.line([(mallet_x, mallet_y), (mallet_x + 14, mallet_y - 10)], fill=spark_col, width=2)
d1.line([(mallet_x, mallet_y), (mallet_x + 2, mallet_y - 16)], fill=spark_col, width=2)
# Smoke puff 2
d1.ellipse([pot_x - 8, pot_y - 24, pot_x + 5, pot_y - 12], fill=(230, 230, 230, 170))
d1.ellipse([pot_x - 1, pot_y - 38, pot_x + 14, pot_y - 24], fill=(230, 230, 230, 130))
f1.save('assets/mst/mst_pitch_1.png')

# Frame 2: Megaphone soundwaves + flag billowing + slogan musical note
f2 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
f2.paste(pitch_scaled, (ox + 1, oy - 1), pitch_scaled)
d2 = ImageDraw.Draw(f2)
# Soundwaves from megaphone
d2.arc([mega_x - 12, mega_y - 20, mega_x + 12, mega_y + 20], -60, 60, fill=(230, 30, 30, 220), width=2)
d2.arc([mega_x - 20, mega_y - 30, mega_x + 20, mega_y + 30], -60, 60, fill=(230, 30, 30, 160), width=2)
d2.arc([mega_x - 28, mega_y - 40, mega_x + 28, mega_y + 40], -60, 60, fill=(230, 30, 30, 110), width=2)
# Flag flutter highlight
d2.line([(flag_x - 15, flag_y - 10), (flag_x + 25, flag_y - 14)], fill=(255, 255, 255, 140), width=2)
f2.save('assets/mst/mst_pitch_2.png')

# Frame 3: Alternate rhythm bounce + pot bubble
f3 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
f3.paste(pitch_scaled, (ox - 1, oy - 2), pitch_scaled)
d3 = ImageDraw.Draw(f3)
# Smoke puff 3
d3.ellipse([pot_x - 4, pot_y - 22, pot_x + 8, pot_y - 12], fill=(220, 220, 220, 150))
d3.ellipse([pot_x + 3, pot_y - 36, pot_x + 17, pot_y - 24], fill=(220, 220, 220, 110))
d3.ellipse([pot_x + 8, pot_y - 50, pot_x + 24, pot_y - 36], fill=(220, 220, 220, 70))
f3.save('assets/mst/mst_pitch_3.png')

print("Generated assets/mst/mst_pitch_0..3.png")

# -------------------------------------------------------------------------
# 2. GENERATE MILITANTS PANIC FLEEING FRAMES (assets/mst/mst_flee_0..3.png)
# -------------------------------------------------------------------------
flee_base = Image.open('assets/hd/mst_flee_base.png').convert('RGBA')

TARGET_FLEE_W = 460
TARGET_FLEE_H = int(flee_base.height * (TARGET_FLEE_W / flee_base.width))
flee_scaled = flee_base.resize((TARGET_FLEE_W, TARGET_FLEE_H), Image.Resampling.LANCZOS)

FLEE_CANVAS_W = 480
FLEE_CANVAS_H = TARGET_FLEE_H + 25
fox = (FLEE_CANVAS_W - flee_scaled.width) // 2
foy = FLEE_CANVAS_H - flee_scaled.height

# Frame 0: Base panic sprint + sweat drops
ff0 = Image.new('RGBA', (FLEE_CANVAS_W, FLEE_CANVAS_H), (0, 0, 0, 0))
ff0.paste(flee_scaled, (fox, foy), flee_scaled)
dff0 = ImageDraw.Draw(ff0)
# Sweat droplets
dff0.ellipse([fox + 110, foy + 40, fox + 118, foy + 50], fill=(130, 210, 255, 230))
dff0.ellipse([fox + 220, foy + 35, fox + 228, foy + 45], fill=(130, 210, 255, 230))
dff0.ellipse([fox + 310, foy + 45, fox + 318, foy + 55], fill=(130, 210, 255, 230))
ff0.save('assets/mst/mst_flee_0.png')

# Frame 1: High sprint bounce (+5px) + trailing dust clouds (💨)
ff1 = Image.new('RGBA', (FLEE_CANVAS_W, FLEE_CANVAS_H), (0, 0, 0, 0))
ff1.paste(flee_scaled, (fox, foy - 5), flee_scaled)
dff1 = ImageDraw.Draw(ff1)
# Wind / dust lines behind feet
dust_col = (200, 190, 175, 180)
dff1.ellipse([fox + 20, foy + TARGET_FLEE_H - 18, fox + 50, foy + TARGET_FLEE_H - 2], fill=dust_col)
dff1.ellipse([fox + 8, foy + TARGET_FLEE_H - 12, fox + 28, foy + TARGET_FLEE_H], fill=(210, 200, 185, 130))
ff1.save('assets/mst/mst_flee_1.png')

# Frame 2: Forward stumble stride + dropped wooden spoon/cup
ff2 = Image.new('RGBA', (FLEE_CANVAS_W, FLEE_CANVAS_H), (0, 0, 0, 0))
ff2.paste(flee_scaled, (fox + 2, foy - 1), flee_scaled)
dff2 = ImageDraw.Draw(ff2)
dff2.ellipse([fox + 115, foy + 48, fox + 123, foy + 58], fill=(130, 210, 255, 230))
dff2.ellipse([fox + 225, foy + 42, fox + 233, foy + 52], fill=(130, 210, 255, 230))
ff2.save('assets/mst/mst_flee_2.png')

# Frame 3: Alternate sprint bounce (+3px) + double dust trail
ff3 = Image.new('RGBA', (FLEE_CANVAS_W, FLEE_CANVAS_H), (0, 0, 0, 0))
ff3.paste(flee_scaled, (fox - 1, foy - 3), flee_scaled)
dff3 = ImageDraw.Draw(ff3)
dff3.ellipse([fox + 35, foy + TARGET_FLEE_H - 16, fox + 65, foy + TARGET_FLEE_H - 2], fill=dust_col)
dff3.ellipse([fox + 15, foy + TARGET_FLEE_H - 10, fox + 38, foy + TARGET_FLEE_H], fill=(210, 200, 185, 130))
ff3.save('assets/mst/mst_flee_3.png')

print("Generated assets/mst/mst_flee_0..3.png")

# -------------------------------------------------------------------------
# 3. GENERATE MULTI-STAGE ANIMATED TENT FRAMES (assets/mst/tent_stage_0..4.png)
# -------------------------------------------------------------------------
# Tent Canvas: 130w x 90h
TW = 130
TH = 90

# Stage 0: Stakes driven into ground + flat unrolled red tarp + mallet on ground
t0 = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
dt0 = ImageDraw.Draw(t0)
# Ground shadow
dt0.ellipse([15, 75, 115, 87], fill=(25, 25, 25, 70))
# Wooden stakes at corners
stake_col = (150, 110, 60, 255)
dt0.line([(25, 72), (25, 82)], fill=stake_col, width=3)
dt0.line([(65, 70), (65, 80)], fill=stake_col, width=3)
dt0.line([(105, 72), (105, 82)], fill=stake_col, width=3)
# Flat unrolled red tarp
dt0.polygon([(25, 76), (105, 76), (112, 82), (18, 82)], fill=(210, 30, 30, 255), outline=(150, 15, 15, 255))
# Wooden mallet lying on ground
dt0.line([(45, 79), (58, 83)], fill=(170, 130, 70, 255), width=2)
dt0.rectangle([56, 80, 62, 86], fill=(130, 90, 45, 255))
t0.save('assets/mst/tent_stage_0.png')

# Stage 1: Ridge pole raised + ropes pulled + tent canvas being lifted (25% up)
t1 = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
dt1 = ImageDraw.Draw(t1)
dt1.ellipse([15, 74, 115, 87], fill=(25, 25, 25, 80))
# Stakes
dt1.line([(20, 70), (20, 82)], fill=stake_col, width=3)
dt1.line([(110, 70), (110, 82)], fill=stake_col, width=3)
# Center pole
dt1.line([(65, 45), (65, 80)], fill=(180, 140, 75, 255), width=3)
# Tarp lifted low
dt1.polygon([(65, 45), (20, 78), (110, 78)], fill=(215, 28, 28, 255), outline=(150, 15, 15, 255))
# Mallet hammering stake with spark!
dt1.line([(28, 64), (18, 73)], fill=(170, 130, 70, 255), width=2)
dt1.rectangle([14, 70, 21, 76], fill=(130, 90, 45, 255))
dt1.line([(20, 70), (15, 63)], fill=(255, 220, 40, 255), width=2)
t1.save('assets/mst/tent_stage_1.png')

# Stage 2: Halfway hoisted tent (60% up) + guy ropes
t2 = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
dt2 = ImageDraw.Draw(t2)
dt2.ellipse([15, 73, 115, 87], fill=(25, 25, 25, 90))
# Guy lines from peak to stakes
dt2.line([(65, 28), (10, 80)], fill=(220, 220, 220, 200), width=1)
dt2.line([(65, 28), (120, 80)], fill=(220, 220, 220, 200), width=1)
# Main body forming
dt2.polygon([(65, 28), (22, 78), (108, 78)], fill=(220, 25, 25, 255), outline=(160, 15, 15, 255))
# Dark shadow inside
dt2.polygon([(65, 40), (52, 78), (78, 78)], fill=(35, 30, 30, 240))
t2.save('assets/mst/tent_stage_2.png')

# Stage 3: Fully erected iconic MST Red Tent with black flap entrance
t3 = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
dt3 = ImageDraw.Draw(t3)
dt3.ellipse([12, 72, 118, 88], fill=(20, 20, 20, 100))
# Guy lines
dt3.line([(65, 16), (8, 80)], fill=(230, 230, 230, 220), width=1)
dt3.line([(65, 16), (122, 80)], fill=(230, 230, 230, 220), width=1)
# Tent ridge pole
dt3.line([(65, 14), (65, 80)], fill=(160, 120, 60, 255), width=2)
# Tent canvas (A-frame red tent with highlights and shadow)
# Left half
dt3.polygon([(65, 16), (18, 78), (65, 78)], fill=(225, 25, 25, 255), outline=(160, 10, 10, 255))
# Right half (slightly darker shadow)
dt3.polygon([(65, 16), (112, 78), (65, 78)], fill=(195, 20, 20, 255), outline=(150, 10, 10, 255))
# Black front flap opening
dt3.polygon([(65, 32), (48, 78), (82, 78)], fill=(28, 25, 28, 255))
# Guy stakes
dt3.line([(8, 75), (8, 83)], fill=stake_col, width=3)
dt3.line([(122, 75), (122, 83)], fill=stake_col, width=3)
# Small red MST flag on top peak
dt3.line([(65, 4), (65, 16)], fill=(100, 100, 100, 255), width=2)
dt3.polygon([(65, 4), (84, 8), (65, 12)], fill=(235, 20, 20, 255))
dt3.ellipse([(71, 6), (75, 10)], fill=(255, 255, 255, 255)) # MST white emblem dot
t3.save('assets/mst/tent_stage_3.png')

# Stage 4: Tent with fluttering flag + active campfire & smoking iron cooking pot
t4 = t3.copy()
dt4 = ImageDraw.Draw(t4)
# Campfire stones at right
pot_cx = 106
pot_cy = 76
dt4.ellipse([pot_cx - 10, pot_cy + 2, pot_cx + 10, pot_cy + 8], fill=(60, 55, 55, 255))
# Fire glow
dt4.polygon([(pot_cx - 5, pot_cy + 4), (pot_cx, pot_cy - 4), (pot_cx + 5, pot_cy + 4)], fill=(255, 120, 20, 255))
dt4.polygon([(pot_cx - 2, pot_cy + 3), (pot_cx, pot_cy - 1), (pot_cx + 2, pot_cy + 3)], fill=(255, 230, 40, 255))
# Black iron pot on fire
dt4.ellipse([pot_cx - 7, pot_cy - 6, pot_cx + 7, pot_cy + 2], fill=(25, 25, 25, 255))
dt4.ellipse([pot_cx - 6, pot_cy - 6, pot_cx + 6, pot_cy - 3], fill=(45, 45, 45, 255))
# Rising aromatic feijoada steam puffs!
dt4.ellipse([pot_cx - 3, pot_cy - 14, pot_cx + 3, pot_cy - 8], fill=(225, 225, 225, 160))
dt4.ellipse([pot_cx, pot_cy - 22, pot_cx + 8, pot_cy - 14], fill=(225, 225, 225, 120))
dt4.ellipse([pot_cx + 3, pot_cy - 30, pot_cx + 13, pot_cy - 20], fill=(225, 225, 225, 80))
t4.save('assets/mst/tent_stage_4.png')

# Collapse frame: Tent flattened with dust cloud
tc = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
dtc = ImageDraw.Draw(tc)
dtc.ellipse([15, 75, 115, 87], fill=(25, 25, 25, 80))
# Flattened crumpled red tarp
dtc.polygon([(20, 78), (45, 72), (75, 76), (110, 79), (95, 84), (30, 83)], fill=(190, 25, 25, 230), outline=(140, 15, 15, 200))
# Broken poles
dtc.line([(35, 74), (60, 68)], fill=(150, 110, 50, 255), width=2)
# Dust puff cloud
dtc.ellipse([25, 60, 55, 78], fill=(210, 200, 185, 160))
dtc.ellipse([50, 52, 85, 74], fill=(210, 200, 185, 180))
dtc.ellipse([75, 58, 105, 76], fill=(210, 200, 185, 150))
tc.save('assets/mst/tent_collapse.png')

print("Generated assets/mst/tent_stage_0..4.png and tent_collapse.png successfully!")
