"""
Desktop and Taskbar Scanner for Desktop Lula.
Finds actual files and shortcuts on the user's desktop and taskbar,
extracts their authentic Windows icons via shell32, and calculates
their real screen coordinates!
"""
import os
import ctypes
from ctypes import wintypes
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QPoint

SHGFI_ICON = 0x000000100
SHGFI_LARGEICON = 0x000000000

class SHFILEINFOW(ctypes.Structure):
    _fields_ = [
        ('hIcon', wintypes.HICON),
        ('iIcon', ctypes.c_int),
        ('dwAttributes', wintypes.DWORD),
        ('szDisplayName', wintypes.WCHAR * 260),
        ('szTypeName', wintypes.WCHAR * 80)
    ]

def extract_file_icon(file_path):
    """Extracts the actual Windows icon of a file or shortcut as a QPixmap."""
    try:
        shinfo = SHFILEINFOW()
        res = ctypes.windll.shell32.SHGetFileInfoW(
            file_path,
            0,
            ctypes.byref(shinfo),
            ctypes.sizeof(shinfo),
            SHGFI_ICON | SHGFI_LARGEICON
        )
        if res and shinfo.hIcon:
            qimg = QImage.fromHICON(shinfo.hIcon)
            ctypes.windll.user32.DestroyIcon(shinfo.hIcon)
            if not qimg.isNull():
                return QPixmap.fromImage(qimg)
    except Exception as e:
        print(f"Error extracting icon for {file_path}: {e}")
    return None

def scan_real_desktop_icons(screen_rect):
    """
    Scans the actual User Desktop and Public Desktop folders,
    extracts their real icons and calculates their real screen grid positions.
    """
    desktop_dirs = [
        os.path.expanduser('~/Desktop'),
        r'C:\Users\Public\Desktop'
    ]

    real_targets = []
    seen_names = set()

    # Always include the Windows Recycle Bin (Lixeira) at top-left grid slot 0
    bin_pix = None
    if os.path.exists('assets/stolen_icons/lixeira.png'):
        bin_pix = QPixmap('assets/stolen_icons/lixeira.png')
    real_targets.append({
        "name": "Lixeira",
        "type": "desktop",
        "grid_col": 0,
        "grid_row": 0,
        "x": screen_rect.left() + 35,
        "y": screen_rect.top() + 35,
        "pixmap": bin_pix,
        "phrase": "A Lixeira agora e patrimonio federal do povo!"
    })
    seen_names.add("lixeira")

    # Collect actual files from both desktop directories
    desktop_files = []
    for d in desktop_dirs:
        if os.path.exists(d):
            try:
                for fname in sorted(os.listdir(d)):
                    if fname.lower() in ('desktop.ini', 'thumbs.db'):
                        continue
                    full_path = os.path.join(d, fname)
                    clean_name = os.path.splitext(fname)[0]
                    if clean_name.lower() in seen_names:
                        continue
                    seen_names.add(clean_name.lower())
                    desktop_files.append((clean_name, full_path))
            except Exception:
                pass

    # Windows standard grid metrics: icon spacing is ~84px horizontal, ~82px vertical
    icon_w = 84
    icon_h = 82
    max_rows = max(1, (screen_rect.height() - 90) // icon_h)

    # Place subsequent icons starting from slot index 1
    for idx, (clean_name, full_path) in enumerate(desktop_files, start=1):
        col = idx // max_rows
        row = idx % max_rows
        
        pos_x = screen_rect.left() + 35 + (col * icon_w)
        pos_y = screen_rect.top() + 35 + (row * icon_h)

        pix = extract_file_icon(full_path)
        
        # Fallback to generic icon if needed
        if not pix and os.path.exists('assets/stolen_icons/pasta.png'):
            pix = QPixmap('assets/stolen_icons/pasta.png')

        real_targets.append({
            "name": clean_name,
            "type": "desktop",
            "grid_col": col,
            "grid_row": row,
            "x": pos_x,
            "y": pos_y,
            "pixmap": pix,
            "phrase": f"O atalho do '{clean_name}' agora e da Uniao!"
        })

    # Add real Taskbar targets (bottom bar)
    taskbar_y = screen_rect.bottom() - 35
    
    # 1. Start Button (Windows logo)
    start_pix = QPixmap('assets/stolen_icons/iniciar.png') if os.path.exists('assets/stolen_icons/iniciar.png') else None
    real_targets.append({
        "name": "Botão Iniciar",
        "type": "taskbar",
        "x": screen_rect.center().x() - 90, # Windows 11 centered start or left
        "y": taskbar_y,
        "pixmap": start_pix,
        "phrase": "Estatizei o botao Iniciar da barra de tarefas!"
    })

    # 2. Pinned Apps in Taskbar center
    chrome_pix = QPixmap('assets/stolen_icons/chrome.png') if os.path.exists('assets/stolen_icons/chrome.png') else None
    real_targets.append({
        "name": "Navegador da Barra",
        "type": "taskbar",
        "x": screen_rect.center().x() - 40,
        "y": taskbar_y,
        "pixmap": chrome_pix,
        "phrase": "Guardei o aplicativo da barra de tarefas no paleto!"
    })

    # 3. System Tray (Clock / Notify area at right)
    real_targets.append({
        "name": "Icones do Relogio",
        "type": "taskbar",
        "x": screen_rect.right() - 80,
        "y": taskbar_y,
        "pixmap": start_pix,
        "phrase": "Surrupiei o relogio do Windows pro bem comum!"
    })

    return real_targets
