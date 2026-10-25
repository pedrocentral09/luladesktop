"""
Generate High-Definition Amarildo Editorial Caricature Sprites for Xandão (Mouse Arrest).
4 dramatic frames:
- 0: Descending entrance, judicial robe billowing, gleaming bald dome
- 1: High wind-up, golden gavel raised at peak, dazzling bald flare
- 2: Gavel impact strike on sounding block, sparks and shockwave, chrome handcuffs locking
- 3: Solemn authoritarian decree pose, holding STF arrest warrant
"""
from PIL import Image, ImageDraw
import os

os.makedirs('assets/xandao', exist_ok=True)

# Load base Xandão
xandao = Image.open('assets/hd/xandao_base.png').convert('RGBA')

# Target sprite dimensions in Xandao widget: 220w x 200h
target_h = 190
target_w = int(xandao.width * (target_h / xandao.height))
xandao_scaled = xandao.resize((target_w, target_h), Image.Resampling.LANCZOS)

CANVAS_W = 250
CANVAS_H = 205
ox = (CANVAS_W - xandao_scaled.width) // 2
oy = CANVAS_H - xandao_scaled.height

head_top_x = ox + int(xandao_scaled.width * 0.48)
head_top_y = oy + int(xandao_scaled.height * 0.12)
cx = ox + xandao_scaled.width - 25
cy = CANVAS_H - 30

# Frame 0: Descending entrance - gleaming bald reflection
frame_0 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
frame_0.paste(xandao_scaled, (ox, oy), xandao_scaled)
d0 = ImageDraw.Draw(frame_0)
d0.line([(head_top_x, head_top_y - 12), (head_top_x, head_top_y + 12)], fill=(255, 255, 255, 250), width=2)
d0.line([(head_top_x - 12, head_top_y), (head_top_x + 12, head_top_y)], fill=(255, 255, 255, 250), width=2)
d0.ellipse([head_top_x - 4, head_top_y - 4, head_top_x + 4, head_top_y + 4], fill=(255, 255, 255, 255))
frame_0.save('assets/xandao/xandao_0.png')

# Frame 1: Peak wind-up - lifted 4px, intense bald lens flare
frame_1 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
frame_1.paste(xandao_scaled, (ox, oy - 4), xandao_scaled)
d1 = ImageDraw.Draw(frame_1)
# Huge glistening star
d1.line([(head_top_x, head_top_y - 18), (head_top_x, head_top_y + 18)], fill=(255, 255, 220, 255), width=3)
d1.line([(head_top_x - 18, head_top_y), (head_top_x + 18, head_top_y)], fill=(255, 255, 220, 255), width=3)
d1.line([(head_top_x - 10, head_top_y - 10), (head_top_x + 10, head_top_y + 10)], fill=(255, 240, 150, 200), width=2)
d1.line([(head_top_x - 10, head_top_y + 10), (head_top_x + 10, head_top_y - 10)], fill=(255, 240, 150, 200), width=2)
d1.ellipse([head_top_x - 6, head_top_y - 6, head_top_x + 6, head_top_y + 6], fill=(255, 255, 255, 255))
frame_1.save('assets/xandao/xandao_1.png')

# Frame 2: Gavel slam impact strike!
frame_2 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
frame_2.paste(xandao_scaled, (ox, oy + 4), xandao_scaled)
d2 = ImageDraw.Draw(frame_2)
# Head sparkle
d2.line([(head_top_x, head_top_y - 8), (head_top_x, head_top_y + 8)], fill=(255, 255, 255, 220), width=2)
d2.line([(head_top_x - 8, head_top_y), (head_top_x + 8, head_top_y)], fill=(255, 255, 255, 220), width=2)

# Wooden sounding block
d2.rounded_rectangle([cx - 20, cy + 6, cx + 24, cy + 20], radius=4, fill=(110, 65, 30, 255), outline=(50, 30, 15, 255), width=2)
# Golden hammer head
d2.rectangle([cx - 14, cy - 8, cx + 18, cy + 6], fill=(245, 205, 45, 255), outline=(130, 95, 15, 255), width=2)

# Impact Shockwave sparks (BANG! 💥)
spark_col = (255, 225, 40, 255)
d2.line([(cx - 15, cy - 8), (cx - 30, cy - 22)], fill=spark_col, width=3)
d2.line([(cx + 2, cy - 10), (cx + 2, cy - 28)], fill=spark_col, width=3)
d2.line([(cx + 18, cy - 8), (cx + 32, cy - 22)], fill=spark_col, width=3)
d2.text((cx - 2, cy - 26), "💥", fill=(255, 200, 0, 255))

# Chrome Handcuffs
d2.ellipse([cx - 32, cy - 2, cx - 12, cy + 18], outline=(200, 205, 215, 255), width=3)
d2.ellipse([cx - 10, cy - 2, cx + 10, cy + 18], outline=(200, 205, 215, 255), width=3)
d2.line([(cx - 14, cy + 8), (cx - 8, cy + 8)], fill=(200, 205, 215, 255), width=2)
frame_2.save('assets/xandao/xandao_2.png')

# Frame 3: Locked in custody pose - glowing STF seal and locked handcuffs
frame_3 = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
frame_3.paste(xandao_scaled, (ox, oy + 1), xandao_scaled)
d3 = ImageDraw.Draw(frame_3)
# Head sparkle
d3.ellipse([head_top_x - 3, head_top_y - 3, head_top_x + 3, head_top_y + 3], fill=(255, 255, 255, 255))
# Sounding block
d3.rounded_rectangle([cx - 20, cy + 6, cx + 24, cy + 20], radius=4, fill=(110, 65, 30, 255), outline=(50, 30, 15, 255), width=2)
# Handcuffs with golden binding aura
d3.ellipse([cx - 32, cy - 2, cx - 12, cy + 18], outline=(255, 215, 0, 255), width=3)
d3.ellipse([cx - 10, cy - 2, cx + 10, cy + 18], outline=(255, 215, 0, 255), width=3)
d3.line([(cx - 14, cy + 8), (cx - 8, cy + 8)], fill=(255, 215, 0, 255), width=2)
# Decree paper in hand
d3.rectangle([ox + 10, oy + 90, ox + 45, oy + 140], fill=(255, 255, 240, 255), outline=(180, 20, 20, 255), width=2)
d3.line([(ox + 15, oy + 100), (ox + 40, oy + 100)], fill=(180, 20, 20, 255), width=2)
d3.line([(ox + 15, oy + 110), (ox + 40, oy + 110)], fill=(50, 50, 50, 255), width=1)
d3.line([(ox + 15, oy + 120), (ox + 35, oy + 120)], fill=(50, 50, 50, 255), width=1)
d3.ellipse([ox + 22, oy + 125, ox + 32, oy + 135], fill=(220, 30, 30, 255))
frame_3.save('assets/xandao/xandao_3.png')

print("HD Xandão 4-frame sprites generated successfully!")
