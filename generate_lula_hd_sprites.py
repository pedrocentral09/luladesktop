"""
Generate Master Quality 16-Frame Amarildo Editorial Caricature Sprites for Lula.
Generates 16 frames per animation cycle (at least 15 frames) for cinema-grade fluidity:
- walk (16 frames): 16-phase alternating stride walk cycle with heel-strike, weight recoil, passing, and push-off
- idle (16 frames): 16-phase continuous natural sinusoidal chest breathing & living posture sway
- sneak (16 frames): 16-phase low crouched tip-toe stealth creeping steps
- angry (16 frames): 16-phase outraged stomping & fist pumping protest cycle
- crouch (16 frames): 16-phase terrified cowering shivering jitter
- hide (16 frames): 16-phase proud standing posture while hiding mouse
- drag (16 frames): 16-phase heavy pulling strain cycle
- chase (16 frames): 16-phase high-speed sprinting leaps
Saves both right (_r) and left (_l) directions.
"""
from PIL import Image
import os
import math

os.makedirs('assets/sprites', exist_ok=True)

# Target sprite dimensions in pet_window
TARGET_W = 140
TARGET_H = 185
BASELINE_Y = 177

# Load high-resolution transparent editorial artworks
stand_art = Image.open('assets/hd/lula_stand.png').convert('RGBA')
walk_a_art = Image.open('assets/hd/lula_walk_a.png').convert('RGBA')
walk_b_art = Image.open('assets/hd/lula_walk_b.png').convert('RGBA')
sneak_art = Image.open('assets/hd/lula_sneak.png').convert('RGBA')
angry_art = Image.open('assets/hd/lula_angry.png').convert('RGBA')
crouch_art = Image.open('assets/hd/lula_crouch.png').convert('RGBA')

# Universal uniform scale factor based on standard standing height
SCALE_FACTOR = 168.0 / stand_art.height

def make_sprite(img, scale_factor=SCALE_FACTOR, bob_x=0, bob_y=0, scale_y_mult=1.0, scale_x_mult=1.0, tilt=0):
    """
    Renders an editorial caricature keyframe into the target sprite canvas
    with exact baseline ground alignment and smooth physical squash/stretch.
    """
    w, h = img.size
    nw = max(10, int(w * scale_factor * scale_x_mult))
    nh = max(10, int(h * scale_factor * scale_y_mult))
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    if tilt != 0:
        resized = resized.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=True)
        nw, nh = resized.size

    canvas = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    ox = (TARGET_W - nw) // 2 + bob_x
    oy = BASELINE_Y - nh + bob_y
    canvas.paste(resized, (ox, oy), resized)
    return canvas

def save_dual_directions(img, category, index):
    """Saves both right-facing and left-facing versions."""
    r_path = f"assets/sprites/{category}_r_{index}.png"
    l_path = f"assets/sprites/{category}_l_{index}.png"
    img.save(r_path)
    img_l = img.transpose(Image.FLIP_LEFT_RIGHT)
    img_l.save(l_path)

print("Assembling 16-frame cinema-grade editorial caricature sprites...")

# -------------------------------------------------------------
# 1. WALK (16 frames) - 16-phase alternating stride cycle
# -------------------------------------------------------------
walk_frames = []
# 00..03: Contact A to Recoil A
walk_frames.append(make_sprite(walk_a_art, bob_x=0, bob_y=0, scale_y_mult=1.00, tilt=0))
walk_frames.append(make_sprite(walk_a_art, bob_x=0, bob_y=2, scale_y_mult=0.98, tilt=-0.5))
walk_frames.append(make_sprite(walk_a_art, bob_x=0, bob_y=4, scale_y_mult=0.96, tilt=-1.0))
walk_frames.append(make_sprite(walk_a_art, bob_x=0, bob_y=2, scale_y_mult=0.98, tilt=-0.5))

# 04..07: Transition A -> Stand (Passing 1) -> Reach B
walk_frames.append(Image.blend(make_sprite(walk_a_art, bob_y=0, scale_y_mult=1.00), make_sprite(stand_art, bob_y=-1, scale_y_mult=1.01), 0.35))
walk_frames.append(make_sprite(stand_art, bob_x=0, bob_y=-3, scale_y_mult=1.03, tilt=1.0))
walk_frames.append(make_sprite(stand_art, bob_x=0, bob_y=-4, scale_y_mult=1.04, tilt=1.5))
walk_frames.append(Image.blend(make_sprite(stand_art, bob_y=-2, scale_y_mult=1.02), make_sprite(walk_b_art, bob_y=-1, scale_y_mult=1.00), 0.40))

# 08..11: Contact B to Recoil B
walk_frames.append(make_sprite(walk_b_art, bob_x=0, bob_y=0, scale_y_mult=1.00, tilt=0))
walk_frames.append(make_sprite(walk_b_art, bob_x=0, bob_y=2, scale_y_mult=0.98, tilt=0.5))
walk_frames.append(make_sprite(walk_b_art, bob_x=0, bob_y=4, scale_y_mult=0.96, tilt=1.0))
walk_frames.append(make_sprite(walk_b_art, bob_x=0, bob_y=2, scale_y_mult=0.98, tilt=0.5))

# 12..15: Transition B -> Stand (Passing 2) -> Reach A
walk_frames.append(Image.blend(make_sprite(walk_b_art, bob_y=0, scale_y_mult=1.00), make_sprite(stand_art, bob_y=-1, scale_y_mult=1.01), 0.35))
walk_frames.append(make_sprite(stand_art, bob_x=0, bob_y=-3, scale_y_mult=1.03, tilt=-1.0))
walk_frames.append(make_sprite(stand_art, bob_x=0, bob_y=-4, scale_y_mult=1.04, tilt=-1.5))
walk_frames.append(Image.blend(make_sprite(stand_art, bob_y=-2, scale_y_mult=1.02), make_sprite(walk_a_art, bob_y=-1, scale_y_mult=1.00), 0.40))

for i, f in enumerate(walk_frames):
    save_dual_directions(f, "walk", i)

# -------------------------------------------------------------
# 2. IDLE (16 frames) - Silky-smooth sinusoidal chest breathing
# -------------------------------------------------------------
idle_frames = []
for i in range(16):
    theta = i * (2.0 * math.pi / 16.0)
    sine_val = (math.sin(theta) + 1.0) / 2.0 # 0.0 to 1.0
    s_y = 1.00 + 0.045 * sine_val
    b_y = -round(4.0 * sine_val)
    tlt = 1.2 * math.sin(theta)
    idle_frames.append(make_sprite(stand_art, bob_y=b_y, scale_y_mult=s_y, tilt=tlt))

for i, f in enumerate(idle_frames):
    save_dual_directions(f, "idle", i)

# -------------------------------------------------------------
# 3. SNEAK (16 frames) - 16-phase tip-toe stealth creeping
# -------------------------------------------------------------
sneak_frames = []
# Step 1 (0..7)
sneak_frames.append(make_sprite(sneak_art, bob_x=-3, bob_y=0, scale_y_mult=1.00))
sneak_frames.append(make_sprite(sneak_art, bob_x=-2, bob_y=2, scale_y_mult=0.97))
sneak_frames.append(make_sprite(sneak_art, bob_x=-1, bob_y=4, scale_y_mult=0.95, tilt=-1.0))
sneak_frames.append(make_sprite(sneak_art, bob_x=0, bob_y=2, scale_y_mult=0.97))
sneak_frames.append(make_sprite(sneak_art, bob_x=1, bob_y=0, scale_y_mult=1.00))
sneak_frames.append(make_sprite(sneak_art, bob_x=0, bob_y=-1, scale_y_mult=1.02))
sneak_frames.append(make_sprite(sneak_art, bob_x=1, bob_y=0, scale_y_mult=1.01))
sneak_frames.append(make_sprite(sneak_art, bob_x=2, bob_y=1, scale_y_mult=0.99))

# Step 2 (8..15)
sneak_frames.append(make_sprite(sneak_art, bob_x=3, bob_y=0, scale_y_mult=1.00))
sneak_frames.append(make_sprite(sneak_art, bob_x=2, bob_y=2, scale_y_mult=0.97))
sneak_frames.append(make_sprite(sneak_art, bob_x=1, bob_y=4, scale_y_mult=0.95, tilt=1.0))
sneak_frames.append(make_sprite(sneak_art, bob_x=0, bob_y=2, scale_y_mult=0.97))
sneak_frames.append(make_sprite(sneak_art, bob_x=-1, bob_y=0, scale_y_mult=1.00))
sneak_frames.append(make_sprite(sneak_art, bob_x=0, bob_y=-1, scale_y_mult=1.02))
sneak_frames.append(make_sprite(sneak_art, bob_x=-1, bob_y=0, scale_y_mult=1.01))
sneak_frames.append(make_sprite(sneak_art, bob_x=-2, bob_y=1, scale_y_mult=0.99))

for i, f in enumerate(sneak_frames):
    save_dual_directions(f, "sneak", i)

# -------------------------------------------------------------
# 4. ANGRY (16 frames) - 16-phase outraged stomping & fist pumping
# -------------------------------------------------------------
angry_frames = []
# Left stomp & pump (0..7)
angry_frames.append(make_sprite(angry_art, bob_x=-3, bob_y=2, scale_y_mult=0.97, tilt=-2.0))
angry_frames.append(make_sprite(angry_art, bob_x=-4, bob_y=4, scale_y_mult=0.95, tilt=-2.5))
angry_frames.append(make_sprite(angry_art, bob_x=-2, bob_y=1, scale_y_mult=0.98, tilt=-1.0))
angry_frames.append(make_sprite(angry_art, bob_x=-1, bob_y=-2, scale_y_mult=1.01, tilt=0.0))
angry_frames.append(make_sprite(angry_art, bob_x=0, bob_y=-5, scale_y_mult=1.04, tilt=0.0))
angry_frames.append(make_sprite(angry_art, bob_x=1, bob_y=-4, scale_y_mult=1.03, tilt=0.5))
angry_frames.append(make_sprite(angry_art, bob_x=0, bob_y=-2, scale_y_mult=1.01, tilt=0.0))
angry_frames.append(make_sprite(angry_art, bob_x=1, bob_y=0, scale_y_mult=0.99, tilt=0.5))

# Right stomp & pump (8..15)
angry_frames.append(make_sprite(angry_art, bob_x=3, bob_y=2, scale_y_mult=0.97, tilt=2.0))
angry_frames.append(make_sprite(angry_art, bob_x=4, bob_y=4, scale_y_mult=0.95, tilt=2.5))
angry_frames.append(make_sprite(angry_art, bob_x=2, bob_y=1, scale_y_mult=0.98, tilt=1.0))
angry_frames.append(make_sprite(angry_art, bob_x=1, bob_y=-2, scale_y_mult=1.01, tilt=0.0))
angry_frames.append(make_sprite(angry_art, bob_x=0, bob_y=-5, scale_y_mult=1.04, tilt=0.0))
angry_frames.append(make_sprite(angry_art, bob_x=-1, bob_y=-4, scale_y_mult=1.03, tilt=-0.5))
angry_frames.append(make_sprite(angry_art, bob_x=0, bob_y=-2, scale_y_mult=1.01, tilt=0.0))
angry_frames.append(make_sprite(angry_art, bob_x=-1, bob_y=0, scale_y_mult=0.99, tilt=-0.5))

for i, f in enumerate(angry_frames):
    save_dual_directions(f, "angry", i)

# -------------------------------------------------------------
# 5. CROUCH (16 frames) - 16-phase terrified quivering jitter
# -------------------------------------------------------------
crouch_frames = []
jitter_x = [-2, 1, -3, 2, -1, 3, -2, 0, 2, -3, 1, -2, 3, -1, 2, 0]
jitter_y = [0, 2, 1, 3, 2, 4, 3, 1, 0, 2, 3, 4, 2, 3, 1, 0]
jitter_scales = [1.00, 0.98, 0.97, 0.96, 0.97, 0.95, 0.96, 0.98, 1.00, 0.98, 0.96, 0.95, 0.97, 0.96, 0.98, 0.99]

for i in range(16):
    crouch_frames.append(make_sprite(crouch_art, bob_x=jitter_x[i], bob_y=jitter_y[i], scale_y_mult=jitter_scales[i]))

for i, f in enumerate(crouch_frames):
    save_dual_directions(f, "crouch", i)

# -------------------------------------------------------------
# 6. HIDE (16 frames) - 16-phase proud posture holding coat pocket
# -------------------------------------------------------------
hide_frames = []
for i in range(16):
    theta = i * (2.0 * math.pi / 16.0)
    sine_val = (math.sin(theta) + 1.0) / 2.0
    s_y = 1.00 + 0.040 * sine_val
    b_y = -round(3.0 * sine_val)
    tlt = 1.0 * math.cos(theta)
    hide_frames.append(make_sprite(stand_art, bob_y=b_y, scale_y_mult=s_y, tilt=tlt))

for i, f in enumerate(hide_frames):
    save_dual_directions(f, "hide", i)

# -------------------------------------------------------------
# 7. DRAG (16 frames) - 16-phase heavy meme pull strain
# -------------------------------------------------------------
drag_frames = []
# Pull phase 1 (0..7)
drag_frames.append(make_sprite(walk_a_art, bob_x=-2, bob_y=2, scale_x_mult=1.03, tilt=8.0))
drag_frames.append(make_sprite(walk_a_art, bob_x=-3, bob_y=3, scale_x_mult=1.04, tilt=8.5))
drag_frames.append(make_sprite(stand_art, bob_x=-4, bob_y=-1, scale_x_mult=1.02, tilt=9.0))
drag_frames.append(make_sprite(stand_art, bob_x=-5, bob_y=-2, scale_x_mult=1.03, tilt=9.5))
drag_frames.append(make_sprite(stand_art, bob_x=-4, bob_y=-1, scale_x_mult=1.02, tilt=9.0))
drag_frames.append(make_sprite(walk_a_art, bob_x=-3, bob_y=1, scale_x_mult=1.01, tilt=8.0))
drag_frames.append(make_sprite(walk_a_art, bob_x=-2, bob_y=2, scale_x_mult=1.02, tilt=7.5))
drag_frames.append(make_sprite(walk_a_art, bob_x=-1, bob_y=1, scale_x_mult=1.01, tilt=7.0))

# Pull phase 2 (8..15)
drag_frames.append(make_sprite(walk_b_art, bob_x=-2, bob_y=2, scale_x_mult=1.03, tilt=8.0))
drag_frames.append(make_sprite(walk_b_art, bob_x=-3, bob_y=3, scale_x_mult=1.04, tilt=8.5))
drag_frames.append(make_sprite(stand_art, bob_x=-4, bob_y=-1, scale_x_mult=1.02, tilt=9.0))
drag_frames.append(make_sprite(stand_art, bob_x=-5, bob_y=-2, scale_x_mult=1.03, tilt=9.5))
drag_frames.append(make_sprite(stand_art, bob_x=-4, bob_y=-1, scale_x_mult=1.02, tilt=9.0))
drag_frames.append(make_sprite(walk_b_art, bob_x=-3, bob_y=1, scale_x_mult=1.01, tilt=8.0))
drag_frames.append(make_sprite(walk_b_art, bob_x=-2, bob_y=2, scale_x_mult=1.02, tilt=7.5))
drag_frames.append(make_sprite(walk_b_art, bob_x=-1, bob_y=1, scale_x_mult=1.01, tilt=7.0))

for i, f in enumerate(drag_frames):
    save_dual_directions(f, "drag", i)

# -------------------------------------------------------------
# 8. CHASE (16 frames) - 16-phase fast sprinting leaps
# -------------------------------------------------------------
chase_frames = []
# Sprint leap A (0..7)
chase_frames.append(make_sprite(walk_a_art, bob_x=2, bob_y=-6, scale_y_mult=1.02, tilt=-12.0))
chase_frames.append(make_sprite(walk_a_art, bob_x=1, bob_y=-3, scale_y_mult=1.01, tilt=-11.0))
chase_frames.append(make_sprite(walk_a_art, bob_x=0, bob_y=1, scale_y_mult=0.98, tilt=-9.0))
chase_frames.append(make_sprite(walk_a_art, bob_x=0, bob_y=4, scale_y_mult=0.95, tilt=-7.0))
chase_frames.append(make_sprite(walk_a_art, bob_x=1, bob_y=2, scale_y_mult=0.97, tilt=-8.0))
chase_frames.append(make_sprite(stand_art, bob_x=2, bob_y=-2, scale_y_mult=1.02, tilt=-10.0))
chase_frames.append(make_sprite(stand_art, bob_x=3, bob_y=-4, scale_y_mult=1.03, tilt=-11.0))
chase_frames.append(make_sprite(walk_b_art, bob_x=2, bob_y=-5, scale_y_mult=1.02, tilt=-12.0))

# Sprint leap B (8..15)
chase_frames.append(make_sprite(walk_b_art, bob_x=2, bob_y=-6, scale_y_mult=1.02, tilt=-12.0))
chase_frames.append(make_sprite(walk_b_art, bob_x=1, bob_y=-3, scale_y_mult=1.01, tilt=-11.0))
chase_frames.append(make_sprite(walk_b_art, bob_x=0, bob_y=1, scale_y_mult=0.98, tilt=-9.0))
chase_frames.append(make_sprite(walk_b_art, bob_x=0, bob_y=4, scale_y_mult=0.95, tilt=-7.0))
chase_frames.append(make_sprite(walk_b_art, bob_x=1, bob_y=2, scale_y_mult=0.97, tilt=-8.0))
chase_frames.append(make_sprite(stand_art, bob_x=2, bob_y=-2, scale_y_mult=1.02, tilt=-10.0))
chase_frames.append(make_sprite(stand_art, bob_x=3, bob_y=-4, scale_y_mult=1.03, tilt=-11.0))
chase_frames.append(make_sprite(walk_a_art, bob_x=2, bob_y=-5, scale_y_mult=1.02, tilt=-12.0))

for i, f in enumerate(chase_frames):
    save_dual_directions(f, "chase", i)

print("All 16-frame master quality editorial caricature sprites generated successfully!")
