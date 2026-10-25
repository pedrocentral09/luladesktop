"""
Generate classic Windows desktop & taskbar icons that Lula can steal.
"""
from PIL import Image, ImageDraw
import os

def generate_icons():
    os.makedirs('assets/stolen_icons', exist_ok=True)

    # 1. Lixeira do Windows (Recycle Bin)
    bin_img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(bin_img)
    # Bin body
    d.polygon([(7, 10), (25, 10), (22, 28), (10, 28)], fill=(120, 190, 230, 255), outline=(50, 110, 160, 255))
    # Bin lid
    d.rectangle([5, 7, 27, 9], fill=(90, 160, 205, 255), outline=(40, 90, 140, 255))
    d.rectangle([13, 5, 19, 7], fill=(90, 160, 205, 255))
    # Recycling ribbons
    d.line([14, 14, 18, 14], fill=(255, 255, 255, 255), width=2)
    d.line([18, 14, 16, 22], fill=(255, 255, 255, 255), width=2)
    d.line([16, 22, 12, 17], fill=(255, 255, 255, 255), width=2)
    bin_img.save('assets/stolen_icons/lixeira.png')

    # 2. Google Chrome
    chrome = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(chrome)
    # Outer circle divided into Red, Yellow, Green
    d.ellipse([3, 3, 29, 29], fill=(230, 50, 40, 255))
    d.pieslice([3, 3, 29, 29], 30, 150, fill=(45, 170, 75, 255))
    d.pieslice([3, 3, 29, 29], 150, 270, fill=(250, 200, 20, 255))
    # Center white and blue circle
    d.ellipse([9, 9, 23, 23], fill=(255, 255, 255, 255))
    d.ellipse([11, 11, 21, 21], fill=(60, 130, 245, 255))
    chrome.save('assets/stolen_icons/chrome.png')

    # 3. Pasta Amarela do Windows (Folder)
    folder = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(folder)
    # Tab
    d.rounded_rectangle([4, 6, 15, 12], radius=2, fill=(225, 170, 40, 255))
    # Back
    d.rounded_rectangle([4, 10, 28, 26], radius=2, fill=(235, 180, 50, 255))
    # Sheet inside
    d.rectangle([7, 8, 25, 18], fill=(255, 255, 255, 255))
    # Front flap
    d.polygon([(3, 13), (29, 13), (27, 27), (3, 27)], fill=(255, 210, 80, 255), outline=(210, 160, 30, 255))
    folder.save('assets/stolen_icons/pasta.png')

    # 4. Ícone do Menu Iniciar do Windows
    win_start = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(win_start)
    # 4 blue squares of Windows logo
    d.rectangle([5, 5, 14, 14], fill=(0, 120, 215, 255))
    d.rectangle([17, 5, 26, 14], fill=(0, 120, 215, 255))
    d.rectangle([5, 17, 14, 26], fill=(0, 120, 215, 255))
    d.rectangle([17, 17, 26, 26], fill=(0, 120, 215, 255))
    win_start.save('assets/stolen_icons/iniciar.png')

    # 5. Excel (Planilha)
    excel = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(excel)
    d.rounded_rectangle([4, 5, 28, 27], radius=3, fill=(16, 124, 65, 255))
    d.rectangle([7, 8, 25, 24], outline=(255, 255, 255, 180))
    d.line([13, 8, 13, 24], fill=(255, 255, 255, 180))
    d.line([19, 8, 19, 24], fill=(255, 255, 255, 180))
    d.line([7, 13, 25, 13], fill=(255, 255, 255, 180))
    d.line([7, 18, 25, 18], fill=(255, 255, 255, 180))
    # Green X badge
    d.rounded_rectangle([3, 10, 15, 22], radius=2, fill=(10, 95, 48, 255), outline=(255, 255, 255, 255))
    d.text((6, 9), "X", fill=(255, 255, 255, 255))
    excel.save('assets/stolen_icons/excel.png')

    # 6. Discord
    discord = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(discord)
    d.rounded_rectangle([4, 4, 28, 28], radius=6, fill=(88, 101, 242, 255))
    # Discord face
    d.ellipse([9, 13, 14, 18], fill=(255, 255, 255, 255))
    d.ellipse([18, 13, 23, 18], fill=(255, 255, 255, 255))
    d.arc([11, 15, 21, 23], 0, 180, fill=(255, 255, 255, 255), width=2)
    discord.save('assets/stolen_icons/discord.png')

    print("Desktop & Taskbar icons generated successfully!")

if __name__ == '__main__':
    generate_icons()
