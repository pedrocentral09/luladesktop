"""
Drop Items (Money notes, red stars) dropped occasionally as trails.
Transparent, click-through, and fast-fading.
"""
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
import random
import os

ACTIVE_DROPS = []

def clear_all_drops():
    global ACTIVE_DROPS
    for d in list(ACTIVE_DROPS):
        d.close()
    ACTIVE_DROPS.clear()

class DropWidget(QLabel):
    def __init__(self, x, y, lifetime_sec=2.5, drop_type=None):
        super().__init__()
        
        # Transparent, completely click-through overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

        # Select drop sprite
        drops_dir = "assets/drops"
        available = []
        if os.path.exists(drops_dir):
            # Routine drops are stars and money; special drops (like tents) only when specified
            available = [os.path.join(drops_dir, f) for f in os.listdir(drops_dir) 
                         if f.endswith('.png') and not f.startswith('barraca')]
            if not available:
                available = [os.path.join(drops_dir, f) for f in os.listdir(drops_dir) if f.endswith('.png')]

        if drop_type:
            chosen = os.path.join(drops_dir, f"{drop_type}.png")
        else:
            chosen = random.choice(available) if available else None

        if chosen and os.path.exists(chosen):
            pix = QPixmap(chosen)
            self.setPixmap(pix)
            self.resize(pix.size())
        else:
            self.resize(24, 24)

        # Jitter slightly for natural feel behind feet
        jx = x + random.randint(-6, 6)
        jy = y + random.randint(35, 45)
        self.move(jx, jy)

        self.lifetime_ms = int(lifetime_sec * 1000)
        self.fade_interval = 40  # 40ms updates for smooth quick fade
        self.elapsed = 0

        # Self-destruct / fade timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.timer.start(self.fade_interval)

        ACTIVE_DROPS.append(self)
        self.show()

    def _step(self):
        self.elapsed += self.fade_interval
        # Start fading fast after 40% of lifetime has passed
        fade_start = self.lifetime_ms * 0.4
        if self.elapsed >= fade_start:
            remaining_ratio = max(0.0, (self.lifetime_ms - self.elapsed) / (self.lifetime_ms - fade_start))
            self.setWindowOpacity(remaining_ratio)
            
        if self.elapsed >= self.lifetime_ms:
            self.timer.stop()
            if self in ACTIVE_DROPS:
                ACTIVE_DROPS.remove(self)
            self.close()
