"""
Process MST/CUT Militants and Tent Assets with transparent background cutout.
"""
from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs('assets/hd', exist_ok=True)
os.makedirs('assets/mst', exist_ok=True)

brain_dir = r"C:\Users\phsou\.gemini\antigravity\brain\473b040c-1d53-47ab-bc11-1f5d67fd02fb"
img_pitch = os.path.join(brain_dir, "mst_cut_militants_editorial_cartoon_1792949186976.jpg")
img_flee = os.path.join(brain_dir, "militants_panicking_cartoon_1792949191497.jpg")

def remove_white_bg(img_path, out_path, white_thresh=242, flood_thresh=18):
    if not os.path.exists(img_path):
        print(f"Warning: {img_path} not found!")
        return None
    
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    pixels = im.load()

    # Binary mask of near-white pixels
    mask = Image.new('L', (w, h), 0)
    mask_pixels = mask.load()

    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            if r >= white_thresh and g >= white_thresh and b >= white_thresh:
                mask_pixels[x, y] = 255

    # Floodfill from edges to only remove outer background
    flood = mask.copy()
    for x in range(w):
        if flood.getpixel((x, 0)) == 255: ImageDraw.floodfill(flood, (x, 0), 128, thresh=flood_thresh)
        if flood.getpixel((x, h - 1)) == 255: ImageDraw.floodfill(flood, (x, h - 1), 128, thresh=flood_thresh)
    for y in range(h):
        if flood.getpixel((0, y)) == 255: ImageDraw.floodfill(flood, (0, y), 128, thresh=flood_thresh)
        if flood.getpixel((w - 1, y)) == 255: ImageDraw.floodfill(flood, (w - 1, y), 128, thresh=flood_thresh)

    # Invert to create alpha channel
    alpha = Image.new('L', (w, h), 255)
    alpha_pixels = alpha.load()
    flood_pixels = flood.load()

    for y in range(h):
        for x in range(w):
            if flood_pixels[x, y] == 128:
                alpha_pixels[x, y] = 0

    # Smooth edges with slight blur on alpha mask
    alpha_smooth = alpha.filter(ImageFilter.GaussianBlur(radius=0.7))

    rgba = im.convert('RGBA')
    rgba.putalpha(alpha_smooth)

    # Autocrop transparent borders
    bbox = rgba.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)

    rgba.save(out_path, 'PNG')
    print(f"Saved {out_path}: {rgba.size}")
    return rgba

if __name__ == "__main__":
    remove_white_bg(img_pitch, 'assets/hd/mst_pitch_base.png')
    remove_white_bg(img_flee, 'assets/hd/mst_flee_base.png')
