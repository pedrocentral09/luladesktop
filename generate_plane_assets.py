"""
Generate Gorgeous Presidential Jet (Aerolula VC-1) with Janja and Trailing Banner.
Fixes:
1. Aerial banner is BEHIND the plane (on the left), pulled by tow cables, with the plane at the front (on the right) pointing forward!
2. High-detail, beautiful Aerolula with official FAB presidential livery and Brazilian flag on the tail.
3. Charming, glamorous Janja waving with designer sunglasses, gold bracelets, and a luxury shopping bag!
4. Animated banner ripple frames for aerodynamic wind effect!
5. High-quality jet turbine audio.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import wave
import struct
import math

def generate_plane_assets():
    os.makedirs('assets/plane', exist_ok=True)
    os.makedirs('assets/sounds', exist_ok=True)

    # Total canvas: 620 x 95 px
    # Left: Banner (x=15..395)
    # Middle: Tow cable (x=395..435)
    # Right: Plane (x=435..605, nose pointing RIGHT!)
    w, h = 620, 95

    # Generate 3 frames with undulating banner cloth for wind flutter
    for frame_idx in range(3):
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        wave_phase = frame_idx * (2.0 * math.pi / 3.0)

        # -------------------------------------------------------------
        # 1. THE AERIAL BANNER (TRAILING BEHIND THE PLANE, ON THE LEFT)
        # -------------------------------------------------------------
        banner_x1 = 25
        banner_x2 = 390
        banner_y_center = 46
        banner_half_h = 22

        # Draw undulating cloth banner
        # We sample points along the length and draw top and bottom wave
        top_pts = []
        bot_pts = []
        steps = 40
        for step in range(steps + 1):
            px = banner_x1 + (banner_x2 - banner_x1) * (step / steps)
            # Ripple wave increases towards the trailing tail (left side)
            ripple_amp = 2.5 * (1.0 - (px - banner_x1) / (banner_x2 - banner_x1) * 0.5)
            ripple = math.sin((px * 0.07) + wave_phase) * ripple_amp
            top_pts.append((px, banner_y_center - banner_half_h + ripple))
            bot_pts.append((px, banner_y_center + banner_half_h + ripple))

        # Banner polygon (cloth)
        banner_poly = top_pts + list(reversed(bot_pts))
        # Luxury ivory cloth background with soft shading
        d.polygon(banner_poly, fill=(255, 252, 240, 248), outline=(210, 25, 45, 255))

        # Red top and bottom decorative stripes on banner
        d.line([(top_pts[0][0], top_pts[0][1] + 2), (top_pts[-1][0], top_pts[-1][1] + 2)], fill=(210, 25, 45, 255), width=2)
        d.line([(bot_pts[0][0], bot_pts[0][1] - 2), (bot_pts[-1][0], bot_pts[-1][1] - 2)], fill=(210, 25, 45, 255), width=2)

        # Trailing ribbons / swallowtail cut at the back of the banner (left end)
        cut_y = banner_y_center + math.sin((banner_x1 * 0.07) + wave_phase) * 2.5
        d.polygon([
            (banner_x1, banner_y_center - banner_half_h + 3),
            (banner_x1 - 14, cut_y - 8),
            (banner_x1 - 4, cut_y),
            (banner_x1 - 14, cut_y + 8),
            (banner_x1, banner_y_center + banner_half_h - 3),
            (banner_x1 + 6, cut_y)
        ], fill=(225, 30, 50, 255), outline=(160, 15, 30, 255))

        # Banner Text (Super crisp and legible!)
        # Line 1: Header
        d.text((banner_x1 + 22, banner_y_center - 18), "🛍️ JANJA TOUR: PARTIU COMPRAS! 🛍️", fill=(195, 20, 35, 255))
        # Line 2: Itinerary
        d.text((banner_x1 + 24, banner_y_center + 1), "PARIS • LONDRES • MILAO • SOFA NOVO", fill=(15, 55, 130, 255))

        # Spreader Bar at the front of banner (vertical rigid rod at x=390)
        top_lead = top_pts[-1]
        bot_lead = bot_pts[-1]
        d.line([top_lead, bot_lead], fill=(70, 75, 85, 255), width=3)
        d.ellipse([top_lead[0] - 2, top_lead[1] - 2, top_lead[0] + 2, top_lead[1] + 2], fill=(220, 180, 40, 255))
        d.ellipse([bot_lead[0] - 2, bot_lead[1] - 2, bot_lead[0] + 2, bot_lead[1] + 2], fill=(220, 180, 40, 255))

        # -------------------------------------------------------------
        # 2. TOW CABLE / REBOQUE (x=390 to x=438)
        # -------------------------------------------------------------
        # V-bridle wires from spreader bar to main tow hook
        bridle_hook_x = 408
        bridle_hook_y = banner_y_center
        d.line([top_lead, (bridle_hook_x, bridle_hook_y)], fill=(110, 115, 125, 255), width=1)
        d.line([bot_lead, (bridle_hook_x, bridle_hook_y)], fill=(110, 115, 125, 255), width=1)
        # Main steel cable from bridle hook to plane tail cone at x=438
        plane_tail_attach = (440, 46)
        d.line([(bridle_hook_x, bridle_hook_y), plane_tail_attach], fill=(80, 85, 95, 255), width=2)
        # Little warning ribbon on cable
        d.line([(bridle_hook_x + 12, bridle_hook_y), (bridle_hook_x + 12, bridle_hook_y + 6)], fill=(255, 50, 50, 255), width=2)

        # -------------------------------------------------------------
        # 3. PRESIDENTIAL JET (AEROLULA VC-1) - FLYING RIGHT
        # -------------------------------------------------------------
        # Nose is at x=605 (FRONT, RIGHT), Tail is at x=438 (BACK, LEFT)
        fuselage_top = 28
        fuselage_bot = 62
        fuselage_mid = 45
        nose_x = 604
        tail_x = 440

        # A. Horizontal Stabilizer (elevator) at the tail
        d.polygon([
            (tail_x + 2, fuselage_mid),
            (tail_x - 12, fuselage_mid - 4),
            (tail_x - 2, fuselage_mid - 8),
            (tail_x + 18, fuselage_mid - 2)
        ], fill=(230, 232, 240, 255), outline=(170, 175, 185, 255))

        # B. Vertical Stabilizer (Tail Fin with Brazilian Flag)
        fin_poly = [
            (tail_x + 10, fuselage_top + 4),
            (tail_x - 10, 8),
            (tail_x + 14, 8),
            (tail_x + 36, fuselage_top + 4)
        ]
        d.polygon(fin_poly, fill=(245, 248, 252, 255), outline=(170, 175, 185, 255))
        # Brazilian Flag on Tail Fin:
        # Green field
        d.polygon([
            (tail_x - 6, 11),
            (tail_x + 11, 11),
            (tail_x + 28, fuselage_top),
            (tail_x + 11, fuselage_top)
        ], fill=(0, 155, 58, 255))
        # Yellow Rhombus / Diamond
        d.polygon([
            (tail_x + 11, 14),
            (tail_x + 18, 22),
            (tail_x + 11, 28),
            (tail_x + 4, 22)
        ], fill=(254, 223, 0, 255))
        # Blue circle with white stars arc
        d.ellipse([tail_x + 7, 18, tail_x + 15, 26], fill=(0, 39, 118, 255))
        d.arc([tail_x + 8, 20, tail_x + 14, 24], 180, 360, fill=(255, 255, 255, 255), width=1)

        # C. Main Fuselage Body (Aerodynamic Airbus Shape)
        # Rounded tail cone to sleek nose
        fuselage_pts = [
            (tail_x, fuselage_mid),
            (tail_x + 8, fuselage_top + 2),
            (nose_x - 28, fuselage_top + 1),
            (nose_x - 10, fuselage_top + 6),
            (nose_x, fuselage_mid),          # Nose tip
            (nose_x - 8, fuselage_bot - 4),
            (nose_x - 26, fuselage_bot),
            (tail_x + 12, fuselage_bot),
            (tail_x, fuselage_mid)
        ]
        # Pristine white executive fuselage with soft 3D gradient look
        d.polygon(fuselage_pts, fill=(252, 253, 255, 255), outline=(175, 180, 190, 255), width=2)

        # D. Sleek Cockpit Windshield (Dark reflective blue)
        cockpit_pts = [
            (nose_x - 24, fuselage_top + 4),
            (nose_x - 12, fuselage_top + 8),
            (nose_x - 12, fuselage_top + 14),
            (nose_x - 26, fuselage_top + 12)
        ]
        d.polygon(cockpit_pts, fill=(30, 65, 130, 255), outline=(100, 130, 180, 255))
        # Windshield glare reflection
        d.line([(nose_x - 22, fuselage_top + 6), (nose_x - 15, fuselage_top + 9)], fill=(200, 230, 255, 255), width=1)

        # E. Official Presidential Livery Stripes (Verde e Amarelo com Azul)
        # Deep navy blue stripe along windows
        d.line([(tail_x + 14, fuselage_mid + 2), (nose_x - 12, fuselage_mid + 2)], fill=(16, 46, 110, 255), width=3)
        # Emerald green line
        d.line([(tail_x + 14, fuselage_mid + 5), (nose_x - 14, fuselage_mid + 5)], fill=(0, 155, 58, 255), width=2)
        # Golden yellow line
        d.line([(tail_x + 14, fuselage_mid + 7), (nose_x - 18, fuselage_mid + 7)], fill=(254, 223, 0, 255), width=2)

        # FAB / BRASIL Official Markings
        d.text((tail_x + 28, fuselage_mid + 8), "BRASIL 01", fill=(15, 50, 25, 255))

        # F. Swept-Back Main Wing
        wing_poly = [
            (tail_x + 65, fuselage_bot - 4),
            (tail_x + 35, fuselage_bot + 16),
            (tail_x + 55, fuselage_bot + 16),
            (tail_x + 105, fuselage_bot - 2)
        ]
        d.polygon(wing_poly, fill=(225, 228, 236, 255), outline=(160, 165, 175, 255))
        # Winglet tip (Green and yellow aerodynamic winglet)
        d.polygon([
            (tail_x + 35, fuselage_bot + 16),
            (tail_x + 32, fuselage_bot + 9),
            (tail_x + 38, fuselage_bot + 9),
            (tail_x + 40, fuselage_bot + 16)
        ], fill=(0, 155, 58, 255))
        d.point((tail_x + 35, fuselage_bot + 11), fill=(255, 220, 0, 255))

        # G. CFM Turbine Engine Pod under Wing
        eng_x1 = tail_x + 60
        eng_y1 = fuselage_bot + 4
        eng_x2 = tail_x + 90
        eng_y2 = fuselage_bot + 18
        # Engine pylon mount
        d.rectangle([eng_x1 + 8, eng_y1 - 4, eng_x1 + 22, eng_y1 + 2], fill=(160, 165, 175, 255))
        # Engine nacelle body
        d.rounded_rectangle([eng_x1, eng_y1, eng_x2, eng_y2], radius=5, fill=(240, 242, 248, 255), outline=(140, 145, 155, 255))
        # Engine intake lip (Chrome ring facing front/right!)
        d.ellipse([eng_x2 - 5, eng_y1, eng_x2 + 3, eng_y2], fill=(190, 195, 205, 255), outline=(100, 105, 115, 255))
        d.ellipse([eng_x2 - 3, eng_y1 + 2, eng_x2 + 1, eng_y2 - 2], fill=(30, 35, 45, 255)) # Dark fan intake
        # Exhaust nozzle (rear/left)
        d.ellipse([eng_x1 - 4, eng_y1 + 2, eng_x1 + 2, eng_y2 - 2], fill=(80, 85, 95, 255))
        # Heat vapor trail / exhaust glow
        d.ellipse([eng_x1 - 12, eng_y1 + 4, eng_x1 - 2, eng_y2 - 4], fill=(225, 235, 255, 120))

        # -------------------------------------------------------------
        # 4. EXECUTIVE VIP CABIN WINDOW WITH JANJA WAVING!
        # -------------------------------------------------------------
        # Panoramic window located around x = tail_x + 78 to tail_x + 115
        win_x = tail_x + 82
        win_y = fuselage_top + 4
        win_w = 34
        win_h = 23

        # Window chrome bezel
        d.rounded_rectangle([win_x - 1, win_y - 1, win_x + win_w + 1, win_y + win_h + 1], radius=8, fill=(200, 205, 215, 255))
        # Sky blue interior tint
        d.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + win_h], radius=7, fill=(75, 135, 205, 255))

        # JANJA (SUPER BONITINHA & CARICATA!):
        # Wavy voluminous brunette hair with caramel shine
        d.ellipse([win_x + 4, win_y + 1, win_x + 28, win_y + 21], fill=(85, 45, 22, 255)) # Base hair
        d.ellipse([win_x + 2, win_y + 4, win_x + 12, win_y + 20], fill=(130, 75, 35, 255)) # Left wave
        d.ellipse([win_x + 20, win_y + 4, win_x + 28, win_y + 18], fill=(130, 75, 35, 255)) # Right wave

        # Smooth smiling face
        d.ellipse([win_x + 8, win_y + 5, win_x + 24, win_y + 19], fill=(248, 208, 178, 255))

        # Glamorous designer sunglasses (dark black oversized lenses with golden frame!)
        d.ellipse([win_x + 9, win_y + 8, win_x + 15, win_y + 14], fill=(20, 20, 25, 255), outline=(240, 200, 50, 255), width=1)
        d.ellipse([win_x + 17, win_y + 8, win_x + 23, win_y + 14], fill=(20, 20, 25, 255), outline=(240, 200, 50, 255), width=1)
        d.line([win_x + 15, win_y + 10, win_x + 17, win_y + 10], fill=(240, 200, 50, 255), width=1)
        # Sunglass reflection
        d.point((win_x + 11, win_y + 10), fill=(255, 255, 255, 255))
        d.point((win_x + 19, win_y + 10), fill=(255, 255, 255, 255))

        # Smiling mouth with vibrant red lipstick
        d.chord([win_x + 12, win_y + 14, win_x + 20, win_y + 19], 0, 180, fill=(215, 25, 40, 255))
        d.line([win_x + 13, win_y + 15, win_x + 19, win_y + 15], fill=(255, 255, 255, 255), width=1) # Teeth

        # Pearl / gold necklace hint
        d.arc([win_x + 11, win_y + 17, win_x + 21, win_y + 22], 0, 180, fill=(255, 225, 60, 255), width=2)

        # Waving hand with gold bracelets!
        d.ellipse([win_x + 24, win_y + 2, win_x + 30, win_y + 8], fill=(248, 208, 178, 255)) # Palm
        d.line([win_x + 26, win_y + 7, win_x + 30, win_y + 7], fill=(255, 215, 0, 255), width=2) # Gold bracelet
        # Sparkle on bracelet
        d.point((win_x + 28, win_y + 4), fill=(255, 255, 255, 255))

        # Mini luxury boutique shopping bag held at the window edge!
        bag_x = win_x + 26
        bag_y = win_y + 9
        d.rectangle([bag_x, bag_y, bag_x + 7, bag_y + 11], fill=(255, 195, 210, 255), outline=(210, 50, 100, 255)) # Pink bag
        d.arc([bag_x + 1, bag_y - 3, bag_x + 6, bag_y + 2], 180, 360, fill=(210, 50, 100, 255), width=1) # Handle
        d.text((bag_x + 1, bag_y + 2), "D", fill=(210, 50, 100, 255)) # "Dior" mark

        # Save frame
        img.save(f'assets/plane/janja_plane_{frame_idx}.png')
        if frame_idx == 0:
            # Also save default fallback
            img.save('assets/plane/janja_plane.png')

    print("All Janja airplane frames (fixed rear banner, high detail) generated successfully!")

    # 5. Jet Flyby Sound Effect (Smoother, fuller stereo whoosh)
    sample_rate = 44100
    duration = 2.2
    n_samples = int(sample_rate * duration)
    with wave.open('assets/sounds/plane_flyby.wav', 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            # Jet rumble + turbine whine with smooth doppler pitch drop
            freq = 280.0 - 90.0 * (t / duration)
            rumble = math.sin(2 * math.pi * freq * t) + 0.35 * math.sin(2 * math.pi * (freq * 2.05) * t)
            # High-pitch turbine hiss
            turbine = math.sin(2 * math.pi * 1450.0 * t) * math.sin(2 * math.pi * 320.0 * t) * 0.22
            val = (rumble + turbine) * 0.75
            # Smooth bell curve envelope
            env = math.sin(math.pi * (t / duration)) ** 1.5
            sample = int(val * 16000 * env)
            sample = max(-32767, min(32767, sample))
            frames.extend(struct.pack('<h', sample))
        wav.writeframes(frames)
    print("Plane flyby sound effect generated successfully!")

if __name__ == '__main__':
    generate_plane_assets()
