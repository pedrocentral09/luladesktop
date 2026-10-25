"""
Presidential Jet (Aerolula) Flyover Window.
Flies gracefully across the top of the screen at 60 FPS.
The jet leads at the front, with Janja waving from the cabin window,
pulling the undulating aerial banner with traveling cloth ripples behind it!
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor
import random
import math
import os

ACTIVE_PLANES = []

def clear_all_planes():
    global ACTIVE_PLANES
    for p in list(ACTIVE_PLANES):
        p.close()
    ACTIVE_PLANES.clear()

class JanjaPlaneWidget(QWidget):
    def __init__(self, screen_rect, speed=1.6):
        super().__init__()
        
        # Click-through, borderless, transparent overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

        self.screen_rect = screen_rect
        self.speed = speed
        self.flight_tick = 0
        self.frame_index = 0

        # Load animated banner frames (700x399 px)
        self.frames = []
        for i in range(4):
            path = f"assets/plane/janja_plane_{i}.png"
            if os.path.exists(path):
                self.frames.append(QPixmap(path))
        
        if not self.frames:
            fallback = "assets/plane/janja_plane.png"
            if os.path.exists(fallback):
                self.frames.append(QPixmap(fallback))

        if self.frames:
            self.setFixedSize(self.frames[0].width() + 40, self.frames[0].height() + 20)
        else:
            self.setFixedSize(740, 420)

        # Start position (just offscreen to the left)
        self.current_x = float(self.screen_rect.left() - self.width() - 10)
        self.base_y = float(random.randint(self.screen_rect.top() + 35, self.screen_rect.top() + 110))
        self.current_y = self.base_y
        self.move(round(self.current_x), round(self.current_y))

        # Trailing contrail cloud particles: [{'x': float, 'y': float, 'r': float, 'alpha': float}]
        self.contrails = []

        # 60 FPS flight timer (16ms interval) for silky smooth movement!
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.timer.start(16)

        ACTIVE_PLANES.append(self)
        self.show()

    def _step(self):
        self.flight_tick += 1
        self.current_x += self.speed

        # Animate fluttering banner cloth every 7 ticks (~112ms)
        if self.frames and self.flight_tick % 7 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        # Gentle aerodynamic dual-frequency altitude oscillation
        altitude_offset = math.sin(self.flight_tick * 0.02) * 6.0 + math.sin(self.flight_tick * 0.05) * 2.0
        self.current_y = self.base_y + altitude_offset

        # Spawn trailing contrail cloud particles from twin jet engines
        if self.flight_tick % 6 == 0:
            eng_x = 480
            eng_y = 230 + altitude_offset
            self.contrails.append({'x': float(eng_x), 'y': float(eng_y), 'r': 6.0, 'alpha': 150.0})

        # Update contrails
        for c in list(self.contrails):
            c['x'] -= (self.speed + 1.2)
            c['r'] += 0.4
            c['alpha'] *= 0.94
            if c['alpha'] < 8 or c['x'] < -50:
                self.contrails.remove(c)

        self.move(round(self.current_x), round(self.current_y))

        # Check if crossed the entire screen
        if self.current_x > self.screen_rect.right() + 40:
            self.timer.stop()
            if self in ACTIVE_PLANES:
                ACTIVE_PLANES.remove(self)
            self.close()
            return

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Trailing contrail clouds
        for c in self.contrails:
            alpha = int(c['alpha'])
            r = c['r']
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(245, 250, 255, alpha)))
            painter.drawEllipse(QRectF(c['x'] - r, c['y'] - r, r * 2, r * 2))

        # 2. Jet and fluttering banner sprite
        if self.frames:
            pix = self.frames[self.frame_index % len(self.frames)]
            painter.drawPixmap(0, 10, pix)
