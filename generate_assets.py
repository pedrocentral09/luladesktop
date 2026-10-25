"""
Asset Generator for Desktop Lula - Presidential Edition.
Generates retro pixel-art sprites featuring:
- Elegant dark presidential suit (paletó e calça social)
- White dress shirt & red tie
- Official Brazilian presidential sash (faixa presidencial verde e amarela)
- Gray hair & full beard
- Poses: idle, walk, chase, drag, and pocket/hide (guardando o mouse dentro do paletó!)
"""
from PIL import Image, ImageDraw
import os
import math

def ensure_dirs():
    for d in ['assets/sprites', 'assets/memes', 'assets/notes', 'assets/sounds', 'assets/drops']:
        os.makedirs(d, exist_ok=True)

def draw_presidential_lula_frame(pose='idle', frame=0, facing_right=True):
    width, height = 64, 64
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bob = 0
    leg_offset = 0

    if pose == 'idle':
        bob = 1 if frame % 2 == 1 else 0
    elif pose == 'walk':
        bob = 1 if (frame % 2 == 1) else 0
        leg_offset = 4 * math.sin(frame * math.pi / 2)
    elif pose == 'chase':
        bob = (frame % 2) * 2
        leg_offset = 6 * (1 if frame % 2 == 0 else -1)
    elif pose == 'drag':
        bob = (frame % 2) * 2
        leg_offset = 4 * (1 if frame % 2 == 0 else -1)
    elif pose == 'hide': # Hiding mouse inside paletó
        bob = 1 if frame % 2 == 1 else 0
        leg_offset = 0
    elif pose == 'sneak': # Stealthy creeping tiptoe
        bob = 0 if frame % 2 == 0 else 1
        leg_offset = 2 * (1 if frame % 2 == 0 else -1)
    elif pose == 'angry': # Revolted / furious hands waving or on hips
        bob = (frame % 2) * 2
        leg_offset = 0
    elif pose == 'crouch': # Terrified crouching low, hiding from police!
        bob = 8 + (frame % 2)
        leg_offset = 0

    # Palette
    SKIN = (245, 198, 165, 255)
    SKIN_SHADOW = (215, 165, 130, 255)
    GREY_HAIR = (225, 228, 230, 255)
    DARK_HAIR = (165, 170, 175, 255)
    
    # Presidential Suit & Attire
    SUIT_DARK = (32, 35, 45, 255)       # Charcoal navy suit
    SUIT_LAPEL = (45, 48, 62, 255)      # Lapel accent
    SHIRT_WHITE = (248, 248, 252, 255)  # Crisp white shirt
    TIE_RED = (205, 25, 30, 255)        # Red presidential tie
    TIE_DARK = (150, 15, 20, 255)

    # Faixa Presidencial
    SASH_GREEN = (0, 140, 50, 255)
    SASH_YELLOW = (255, 215, 0, 255)
    SASH_GOLD = (218, 165, 32, 255)

    PANTS = (30, 33, 42, 255)
    SHOES = (15, 15, 20, 255)
    BLACK = (20, 20, 20, 255)
    WHITE = (255, 255, 255, 255)

    cy = 30 + bob
    cx = 32

    # 1. Legs & Formal Shoes
    leg_l_x = cx - 7 + int(leg_offset if not facing_right else -leg_offset)
    leg_r_x = cx + 3 - int(leg_offset if not facing_right else -leg_offset)
    leg_y = cy + 14

    # Left leg
    draw.rectangle([leg_l_x, leg_y, leg_l_x + 4, leg_y + 10], fill=PANTS)
    draw.rectangle([leg_l_x - 1, leg_y + 9, leg_l_x + 5, leg_y + 12], fill=SHOES)

    # Right leg
    draw.rectangle([leg_r_x, leg_y, leg_r_x + 4, leg_y + 10], fill=PANTS)
    draw.rectangle([leg_r_x - 1, leg_y + 9, leg_r_x + 5, leg_y + 12], fill=SHOES)

    # 2. Torso: White shirt base
    body_top = cy - 2
    draw.rectangle([cx - 10, body_top, cx + 10, body_top + 16], fill=SHIRT_WHITE)

    # 3. Red Necktie (Center)
    draw.polygon([(cx - 2, body_top), (cx + 2, body_top), (cx + 1, body_top + 12), (cx - 1, body_top + 12)], fill=TIE_RED)
    draw.polygon([(cx - 1, body_top + 12), (cx + 1, body_top + 12), (cx, body_top + 14)], fill=TIE_RED)

    # 4. Faixa Presidencial (Transversal across chest)
    # Right shoulder to left hip (or mirrored if facing other way)
    # We draw 3 parallel diagonal bands: Green, Yellow, Green
    if facing_right:
        sash_start = (cx + 7, body_top - 1)
        sash_end = (cx - 9, body_top + 15)
    else:
        sash_start = (cx - 7, body_top - 1)
        sash_end = (cx + 9, body_top + 15)

    # Draw sash diagonal polygon
    sx0, sy0 = sash_start
    sx1, sy1 = sash_end
    
    # Sash width = 5px (2px green, 2px yellow, 2px green)
    dx = 3 if facing_right else -3
    draw.polygon([(sx0 - dx, sy0), (sx0 + dx, sy0), (sx1 + dx, sy1), (sx1 - dx, sy1)], fill=SASH_GREEN)
    draw.polygon([(sx0 - int(dx*0.4), sy0), (sx0 + int(dx*0.4), sy0), (sx1 + int(dx*0.4), sy1), (sx1 - int(dx*0.4), sy1)], fill=SASH_YELLOW)

    # Rosette / Golden Medallion at hip
    draw.ellipse([sx1 - 2, sy1 - 2, sx1 + 3, sy1 + 3], fill=SASH_GOLD, outline=(180, 130, 20, 255))

    # 5. Paletó (Suit Jacket sides & lapels over the shirt/sash)
    # Left suit flank
    draw.rectangle([cx - 11, body_top, cx - 6, body_top + 16], fill=SUIT_DARK)
    # Right suit flank
    draw.rectangle([cx + 6, body_top, cx + 11, body_top + 16], fill=SUIT_DARK)
    # Bottom jacket hem
    draw.rectangle([cx - 11, body_top + 14, cx + 11, body_top + 16], fill=SUIT_DARK)

    # Suit Lapels (V shape framing tie & sash)
    draw.polygon([(cx - 10, body_top), (cx - 5, body_top + 9), (cx - 8, body_top + 9)], fill=SUIT_LAPEL)
    draw.polygon([(cx + 10, body_top), (cx + 5, body_top + 9), (cx + 8, body_top + 9)], fill=SUIT_LAPEL)

    # Buttons on paletó
    draw.rectangle([cx - 1, body_top + 11, cx + 1, body_top + 12], fill=BLACK)

    # 6. Head Base & Hair
    head_y = cy - 20
    # Hair back
    draw.ellipse([cx - 14, head_y - 2, cx + 14, head_y + 22], fill=GREY_HAIR)
    # Face
    draw.ellipse([cx - 11, head_y + 2, cx + 11, head_y + 19], fill=SKIN)
    # Top Hair
    draw.chord([cx - 13, head_y - 3, cx + 13, head_y + 13], 180, 360, fill=GREY_HAIR)
    draw.arc([cx - 11, head_y - 1, cx + 11, head_y + 7], 180, 360, fill=DARK_HAIR)

    # Full Beard
    beard_y = head_y + 11
    draw.chord([cx - 11, beard_y, cx + 11, beard_y + 13], 0, 180, fill=GREY_HAIR)
    draw.chord([cx - 8, beard_y + 2, cx + 8, beard_y + 12], 0, 180, fill=DARK_HAIR)

    # Eyes & Eyebrows
    look_dir = 2 if facing_right else -2
    if pose == 'crouch':
        # Worried scared eyebrows
        draw.line([cx - 6 + look_dir, head_y + 7, cx - 2 + look_dir, head_y + 5], fill=DARK_HAIR, width=2)
        draw.line([cx + 2 + look_dir, head_y + 5, cx + 6 + look_dir, head_y + 7], fill=DARK_HAIR, width=2)
        # Wide panic eyes
        draw.rectangle([cx - 6 + look_dir, head_y + 7, cx - 2 + look_dir, head_y + 11], fill=WHITE, outline=BLACK)
        draw.point((cx - 4 + look_dir, head_y + 9), fill=BLACK)
        draw.rectangle([cx + 2 + look_dir, head_y + 7, cx + 6 + look_dir, head_y + 11], fill=WHITE, outline=BLACK)
        draw.point((cx + 4 + look_dir, head_y + 9), fill=BLACK)
        # Giant sweat drop (gota de suor de pavor!)
        d_x = cx + (8 if facing_right else -12)
        draw.ellipse([d_x, head_y, d_x + 6, head_y + 8], fill=(90, 180, 255, 255))
        draw.polygon([(d_x, head_y + 4), (d_x + 3, head_y - 2), (d_x + 6, head_y + 4)], fill=(90, 180, 255, 255))
    elif pose == 'angry':
        # Sharp angry eyebrows slanted down inward!
        draw.line([cx - 7 + look_dir, head_y + 5, cx - 2 + look_dir, head_y + 8], fill=(180, 20, 20, 255), width=2)
        draw.line([cx + 2 + look_dir, head_y + 8, cx + 7 + look_dir, head_y + 5], fill=(180, 20, 20, 255), width=2)
        # Red glowing eyes
        draw.rectangle([cx - 5 + look_dir, head_y + 8, cx - 3 + look_dir, head_y + 10], fill=(220, 20, 20, 255))
        draw.rectangle([cx + 3 + look_dir, head_y + 8, cx + 5 + look_dir, head_y + 10], fill=(220, 20, 20, 255))
        # Anger mark on forehead (four red lines/cross)
        draw.line([cx - 8, head_y + 1, cx - 4, head_y + 1], fill=(230, 20, 20, 255), width=1)
        draw.line([cx - 6, head_y - 1, cx - 6, head_y + 3], fill=(230, 20, 20, 255), width=1)
    else:
        draw.line([cx - 6 + look_dir, head_y + 6, cx - 2 + look_dir, head_y + 6], fill=DARK_HAIR, width=2)
        draw.line([cx + 2 + look_dir, head_y + 6, cx + 6 + look_dir, head_y + 6], fill=DARK_HAIR, width=2)

    if pose == 'hide':
        # Mischievous wink / cheeky squint!
        draw.line([cx - 6 + look_dir, head_y + 9, cx - 2 + look_dir, head_y + 9], fill=BLACK, width=2)
        draw.rectangle([cx + 3 + look_dir, head_y + 8, cx + 5 + look_dir, head_y + 10], fill=BLACK)
        draw.point((cx + 3 + look_dir, head_y + 8), fill=WHITE)
    elif pose not in ('angry', 'crouch'):
        draw.rectangle([cx - 5 + look_dir, head_y + 8, cx - 3 + look_dir, head_y + 10], fill=BLACK)
        draw.rectangle([cx + 3 + look_dir, head_y + 8, cx + 5 + look_dir, head_y + 10], fill=BLACK)
        draw.point((cx - 5 + look_dir, head_y + 8), fill=WHITE)
        draw.point((cx + 3 + look_dir, head_y + 8), fill=WHITE)

    # Nose
    draw.rectangle([cx - 2 + look_dir, head_y + 9, cx + 1 + look_dir, head_y + 12], fill=SKIN_SHADOW)

    # Mouth / Smile in beard
    if pose == 'crouch':
        # Trembling nervous mouth
        draw.line([cx - 4, beard_y + 3, cx - 2, beard_y + 1], fill=BLACK, width=1)
        draw.line([cx - 2, beard_y + 1, cx + 2, beard_y + 4], fill=BLACK, width=1)
        draw.line([cx + 2, beard_y + 4, cx + 4, beard_y + 2], fill=BLACK, width=1)
    elif pose == 'angry':
        # Indignant shouting mouth!
        draw.rectangle([cx - 4 + look_dir, beard_y + 1, cx + 4 + look_dir, beard_y + 6], fill=BLACK)
        draw.rectangle([cx - 2 + look_dir, beard_y + 2, cx + 2 + look_dir, beard_y + 4], fill=WHITE)
    elif pose in ('chase', 'hide'):
        # Sneaky big smile!
        draw.rectangle([cx - 3 + look_dir, beard_y + 2, cx + 4 + look_dir, beard_y + 5], fill=BLACK)
        draw.rectangle([cx - 2 + look_dir, beard_y + 2, cx + 3 + look_dir, beard_y + 3], fill=WHITE)
    else:
        draw.line([cx - 3 + look_dir, beard_y + 3, cx + 3 + look_dir, beard_y + 3], fill=BLACK, width=1)

    # 7. Arms & Hands
    if pose == 'crouch':
        # Hands covering head in terror!
        draw.rectangle([cx - 12, body_top - 2, cx - 7, body_top + 6], fill=SUIT_DARK)
        draw.ellipse([cx - 12, head_y + 4, cx - 6, head_y + 10], fill=SKIN)
        draw.rectangle([cx + 7, body_top - 2, cx + 12, body_top + 6], fill=SUIT_DARK)
        draw.ellipse([cx + 6, head_y + 4, cx + 12, head_y + 10], fill=SKIN)
    elif pose == 'angry':
        # Clenched fists raised in indignation!
        arm_bob = (frame % 2) * 2
        # Left raised fist
        draw.rectangle([cx - 15, body_top - 4 - arm_bob, cx - 10, body_top + 8 - arm_bob], fill=SUIT_DARK)
        draw.ellipse([cx - 16, body_top - 8 - arm_bob, cx - 9, body_top - 2 - arm_bob], fill=SKIN)
        # Right raised fist
        draw.rectangle([cx + 10, body_top - 4 + arm_bob, cx + 15, body_top + 8 + arm_bob], fill=SUIT_DARK)
        draw.ellipse([cx + 9, body_top - 8 + arm_bob, cx + 16, body_top - 2 + arm_bob], fill=SKIN)
    elif pose == 'hide':
        # Hand tucked deeply inside the paletó coat pocket / chest!
        # One hand inside the jacket concealing the mouse, the other on the hip/side
        pocket_x = cx + (2 if facing_right else -6)
        pocket_y = body_top + 6
        
        # Arm reaching inside coat
        arm_x = cx + (8 if facing_right else -12)
        draw.rectangle([arm_x, body_top + 2, arm_x + 5, body_top + 8], fill=SUIT_DARK)
        draw.polygon([(arm_x, body_top + 7), (pocket_x + 4, pocket_y), (pocket_x, pocket_y + 4), (arm_x, body_top + 10)], fill=SUIT_DARK)
        # Bulge in paletó where mouse is hidden!
        draw.ellipse([pocket_x - 3, pocket_y - 2, pocket_x + 5, pocket_y + 5], fill=SUIT_LAPEL)
        # Hand tucked in
        draw.ellipse([pocket_x - 1, pocket_y, pocket_x + 4, pocket_y + 4], fill=SKIN)
        
        # Other arm resting comfortably
        other_arm_x = cx - 13 if facing_right else cx + 9
        draw.rectangle([other_arm_x, body_top + 2, other_arm_x + 4, body_top + 10], fill=SUIT_DARK)
        draw.ellipse([other_arm_x, body_top + 9, other_arm_x + 4, body_top + 13], fill=SKIN)

    elif pose == 'drag':
        # Hands raised pulling window
        arm_x = cx + (8 if facing_right else -12)
        draw.rectangle([arm_x, cy, arm_x + 6, cy + 6], fill=SUIT_DARK)
        draw.ellipse([arm_x + (4 if facing_right else -2), cy - 2, 
                      arm_x + (9 if facing_right else 3), cy + 4], fill=SKIN)
        # Other arm
        other_arm_x = cx - 12 if facing_right else cx + 8
        draw.rectangle([other_arm_x, cy + 2, other_arm_x + 5, cy + 8], fill=SUIT_DARK)
    elif pose == 'chase':
        # Arms forward reaching for cursor
        arm_x = cx + (7 if facing_right else -10)
        draw.rectangle([arm_x, cy + 2, arm_x + 5, cy + 8], fill=SUIT_DARK)
        draw.ellipse([arm_x + (3 if facing_right else -3), cy + 4, 
                      arm_x + (7 if facing_right else 1), cy + 9], fill=SKIN)
        other_x = cx - 10 if facing_right else cx + 7
        draw.rectangle([other_x, cy + 4, other_x + 4, cy + 9], fill=SUIT_DARK)
    else:
        # Normal walk/idle arms with suit sleeves
        arm_swing = int(leg_offset * 0.7)
        arm_l_x = cx - 13
        arm_r_x = cx + 9
        draw.rectangle([arm_l_x, cy + 2 - arm_swing, arm_l_x + 4, cy + 10 - arm_swing], fill=SUIT_DARK)
        draw.ellipse([arm_l_x - 1, cy + 9 - arm_swing, arm_l_x + 4, cy + 13 - arm_swing], fill=SKIN)
        draw.rectangle([arm_r_x, cy + 2 + arm_swing, arm_r_x + 4, cy + 10 + arm_swing], fill=SUIT_DARK)
        draw.ellipse([arm_r_x, cy + 9 + arm_swing, arm_r_x + 5, cy + 13 + arm_swing], fill=SKIN)

    return img

def generate_all_sprites():
    ensure_dirs()
    print("Generating presidential sprites...")
    
    # Idle frames
    for f in range(2):
        img_r = draw_presidential_lula_frame('idle', f, facing_right=True)
        img_r.save(f'assets/sprites/idle_r_{f}.png')
        img_l = draw_presidential_lula_frame('idle', f, facing_right=False)
        img_l.save(f'assets/sprites/idle_l_{f}.png')

    # Walk frames
    for f in range(4):
        img_r = draw_presidential_lula_frame('walk', f, facing_right=True)
        img_r.save(f'assets/sprites/walk_r_{f}.png')
        img_l = draw_presidential_lula_frame('walk', f, facing_right=False)
        img_l.save(f'assets/sprites/walk_l_{f}.png')

    # Chase frames
    for f in range(4):
        img_r = draw_presidential_lula_frame('chase', f, facing_right=True)
        img_r.save(f'assets/sprites/chase_r_{f}.png')
        img_l = draw_presidential_lula_frame('chase', f, facing_right=False)
        img_l.save(f'assets/sprites/chase_l_{f}.png')

    # Drag frames
    for f in range(2):
        img_r = draw_presidential_lula_frame('drag', f, facing_right=True)
        img_r.save(f'assets/sprites/drag_r_{f}.png')
        img_l = draw_presidential_lula_frame('drag', f, facing_right=False)
        img_l.save(f'assets/sprites/drag_l_{f}.png')

    # Hide / Pocket frames (guardando o mouse dentro do paletó!)
    for f in range(2):
        img_r = draw_presidential_lula_frame('hide', f, facing_right=True)
        img_r.save(f'assets/sprites/hide_r_{f}.png')
        img_l = draw_presidential_lula_frame('hide', f, facing_right=False)
        img_l.save(f'assets/sprites/hide_l_{f}.png')

    # Sneak frames (passinhos leves e furtivos!)
    for f in range(4):
        img_r = draw_presidential_lula_frame('sneak', f, facing_right=True)
        img_r.save(f'assets/sprites/sneak_r_{f}.png')
        img_l = draw_presidential_lula_frame('sneak', f, facing_right=False)
        img_l.save(f'assets/sprites/sneak_l_{f}.png')

    # Angry frames (revoltado com punhos erguidos!)
    for f in range(2):
        img_r = draw_presidential_lula_frame('angry', f, facing_right=True)
        img_r.save(f'assets/sprites/angry_r_{f}.png')
        img_l = draw_presidential_lula_frame('angry', f, facing_right=False)
        img_l.save(f'assets/sprites/angry_l_{f}.png')

    # Crouch / Hiding from police frames (agachado tremendo e suando frio!)
    for f in range(2):
        img_r = draw_presidential_lula_frame('crouch', f, facing_right=True)
        img_r.save(f'assets/sprites/crouch_r_{f}.png')
        img_l = draw_presidential_lula_frame('crouch', f, facing_right=False)
        img_l.save(f'assets/sprites/crouch_l_{f}.png')

    print("Presidential sprites generated successfully!")

if __name__ == '__main__':
    generate_all_sprites()
