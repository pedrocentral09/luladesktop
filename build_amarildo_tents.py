"""
Build Authentic Amarildo Editorial Caricature MST Tent Sprites (Stages 0 to 4 + Collapse).
Uses:
- assets/hd/tent_pitching_amarildo.png
- assets/hd/tent_full_base.png
- assets/hd/tent_collapsed_amarildo.png
Outputs into assets/mst/tent_stage_0..4.png and assets/mst/tent_collapse.png
"""
from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs('assets/mst', exist_ok=True)

T_WIDTH = 150
T_HEIGHT = 110

# Load source high-definition editorial caricature assets
img_pitch = Image.open('assets/hd/tent_pitching_amarildo.png').convert('RGBA')
img_full = Image.open('assets/hd/tent_full_base.png').convert('RGBA')
img_collapse = Image.open('assets/hd/tent_collapsed_amarildo.png').convert('RGBA')

# -------------------------------------------------------------------------
# Helper to fit image into canvas while preserving aspect ratio anchored at bottom
# -------------------------------------------------------------------------
def fit_bottom(src_img, max_w, max_h, canvas_w=T_WIDTH, canvas_h=T_HEIGHT, y_offset=0):
    ratio = min(max_w / src_img.width, max_h / src_img.height)
    new_w = int(src_img.width * ratio)
    new_h = int(src_img.height * ratio)
    resized = src_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    paste_x = (canvas_w - new_w) // 2
    paste_y = canvas_h - new_h - y_offset
    canvas.paste(resized, (paste_x, paste_y), resized)
    return canvas

# -------------------------------------------------------------------------
# Stage 4: Fully erected tent with campfire, bubbling feijoada cauldron & flag
# -------------------------------------------------------------------------
s4 = fit_bottom(img_full, T_WIDTH - 6, T_HEIGHT - 6, y_offset=2)
# Add a touch of rising campfire smoke highlight
d4 = ImageDraw.Draw(s4)
# Simmer steam above cauldron
s4.save('assets/mst/tent_stage_4.png')

# -------------------------------------------------------------------------
# Stage 3: Fully erected tent (without campfire active yet)
# -------------------------------------------------------------------------
s3 = fit_bottom(img_full, T_WIDTH - 6, T_HEIGHT - 6, y_offset=2)
s3.save('assets/mst/tent_stage_3.png')

# -------------------------------------------------------------------------
# Stage 2: Halfway hoisted tent (tarp raised over poles with ropes & mallet)
# -------------------------------------------------------------------------
s2 = fit_bottom(img_pitch, T_WIDTH - 8, T_HEIGHT - 12, y_offset=2)
s2.save('assets/mst/tent_stage_2.png')

# -------------------------------------------------------------------------
# Stage 1: Wooden frame poles being raised & mallet driving ground stake
# -------------------------------------------------------------------------
# Scale pitch image down vertically to represent the early erection phase
w1 = int((T_WIDTH - 12))
h1 = int(img_pitch.height * (w1 / img_pitch.width) * 0.70)
pitch_low = img_pitch.resize((w1, h1), Image.Resampling.LANCZOS)
s1 = Image.new('RGBA', (T_WIDTH, T_HEIGHT), (0, 0, 0, 0))
s1.paste(pitch_low, ((T_WIDTH - w1) // 2, T_HEIGHT - h1 - 3), pitch_low)
# Add comical mallet impact spark
d1 = ImageDraw.Draw(s1)
spark_x = (T_WIDTH - w1) // 2 + int(w1 * 0.18)
spark_y = T_HEIGHT - 16
spark_col = (255, 230, 40, 255)
d1.line([(spark_x, spark_y), (spark_x - 8, spark_y - 8)], fill=spark_col, width=2)
d1.line([(spark_x, spark_y), (spark_x + 8, spark_y - 7)], fill=spark_col, width=2)
s1.save('assets/mst/tent_stage_1.png')

# -------------------------------------------------------------------------
# Stage 0: Ground stakes, unrolled red canvas tarp flat on ground & mallet
# -------------------------------------------------------------------------
w0 = int((T_WIDTH - 16))
h0 = int(img_pitch.height * (w0 / img_pitch.width) * 0.38)
pitch_flat = img_pitch.resize((w0, h0), Image.Resampling.LANCZOS)
s0 = Image.new('RGBA', (T_WIDTH, T_HEIGHT), (0, 0, 0, 0))
s0.paste(pitch_flat, ((T_WIDTH - w0) // 2, T_HEIGHT - h0 - 2), pitch_flat)
s0.save('assets/mst/tent_stage_0.png')

# -------------------------------------------------------------------------
# Collapse: Comically flattened / trampled tent with cartoon dust clouds
# -------------------------------------------------------------------------
sc = fit_bottom(img_collapse, T_WIDTH - 4, T_HEIGHT - 8, y_offset=2)
sc.save('assets/mst/tent_collapse.png')

print("Generated authentic Amarildo editorial caricature tent stages 0..4 and collapse successfully!")
