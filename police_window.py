"""
Federal Police Cruiser Window with Sergio Moro and Deltan Dallagnol.
Features dual-harmonic suspension bounce, trailing exhaust smoke puffs,
multi-phase rotating siren lightbars, and smooth 60 FPS cruising speed!
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor, QBrush, QPen, QPainterPath
import random
import math
import os

ACTIVE_POLICE = []

def clear_all_police():
    global ACTIVE_POLICE
    for p in list(ACTIVE_POLICE):
        p.close()
    ACTIVE_POLICE.clear()

class PoliceCarWidget(QWidget):
    car_exited = pyqtSignal()

    def __init__(self, screen_rect, speed=1.5):
        super().__init__()

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
        self.frame_index = 0
        self.ticks = 0

        # Load 4-frame viatura siren animations
        self.frames = []
        for i in range(4):
            path = f"assets/police/viatura_{i}.png"
            if os.path.exists(path):
                self.frames.append(QPixmap(path))

        # Size: wider canvas for high-definition editorial caricature and speech bubble
        self.total_w = 370
        self.total_h = 300
        self.bubble_h = 48
        self.setFixedSize(self.total_w, self.total_h)

        # Quotes shouted from the police car
        quotes = [
            "MORO: Isto e uma conducao coercitiva, conje!",
            "DELTAN: Nao temos provas, mas temos conviccao!",
            "PF: Parado em nome da Operacao Lava-Jato!",
            "DELTAN: Veja as setas do meu PowerPoint!",
            "MORO: A Republica de Curitiba manda lembrancas!",
            "DELTAN: Todos os caminhos levam ao triplex!",
            "MORO: A sentenca ja esta pronta no meu gabinete!"
        ]
        self.speech_text = random.choice(quotes)

        # Start position (just offscreen to the left)
        self.current_x = float(self.screen_rect.left() - self.total_w - 20)
        self.base_y = float(self.screen_rect.bottom() - self.total_h - 15)
        self.current_y = self.base_y
        self.move(round(self.current_x), round(self.current_y))

        # Exhaust smoke puffs list: [{'x': float, 'y': float, 'r': float, 'alpha': float}]
        self.smoke_puffs = []

        # Siren rotation timer (75ms alternating strobes)
        self.siren_timer = QTimer(self)
        self.siren_timer.timeout.connect(self._toggle_siren)
        self.siren_timer.start(75)

        # 60 FPS physics and movement timer (16ms)
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self._step)
        self.move_timer.start(16)

        ACTIVE_POLICE.append(self)
        self.show()

    def _toggle_siren(self):
        if self.frames:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.update()

    def _step(self):
        self.ticks += 1
        self.current_x += self.speed

        # Dual-harmonic vehicle suspension bounce over desktop taskbar
        suspension = math.sin(self.current_x * 0.05) * 1.8 + math.sin(self.current_x * 0.12) * 0.8
        self.current_y = self.base_y + suspension

        # Emit exhaust smoke puff from rear tailpipe every 10 ticks
        if self.ticks % 10 == 0:
            tailpipe_x = 25
            tailpipe_y = self.total_h - 35
            self.smoke_puffs.append({
                'x': float(tailpipe_x),
                'y': float(tailpipe_y),
                'r': 5.0,
                'alpha': 160.0
            })

        # Update smoke particles
        for p in list(self.smoke_puffs):
            p['x'] -= (self.speed + 0.6)
            p['y'] -= 0.4
            p['r'] += 0.45
            p['alpha'] *= 0.94
            if p['alpha'] < 8 or p['x'] < -50:
                self.smoke_puffs.remove(p)

        self.move(round(self.current_x), round(self.current_y))

        # Check if exited screen
        if self.current_x > self.screen_rect.right() + 40:
            self.siren_timer.stop()
            self.move_timer.stop()
            try:
                self.car_exited.emit()
            except Exception:
                pass
            if self in ACTIVE_POLICE:
                ACTIVE_POLICE.remove(self)
            self.close()
            return

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Trailing exhaust smoke puffs behind vehicle
        for p in self.smoke_puffs:
            alpha = int(p['alpha'])
            r = p['r']
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(200, 205, 215, alpha)))
            painter.drawEllipse(QRectF(p['x'] - r, p['y'] - r, r * 2, r * 2))

        # 2. Speech Bubble on Top
        if self.speech_text:
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            bubble_rect = QRectF(15, 4, self.total_w - 30, self.bubble_h - 10)

            painter.setPen(QPen(QColor(15, 30, 80), 2.0))
            painter.setBrush(QBrush(QColor(255, 255, 255, 250)))
            painter.drawRoundedRect(bubble_rect, 8, 8)

            # Bubble pointer tail
            tail = QPainterPath()
            tail.moveTo(150, self.bubble_h - 6)
            tail.lineTo(164, self.bubble_h - 6)
            tail.lineTo(157, self.bubble_h)
            tail.closeSubpath()
            painter.fillPath(tail, QBrush(QColor(255, 255, 255, 250)))
            painter.strokePath(tail, QPen(QColor(15, 30, 80), 2.0))

            painter.setPen(QColor(10, 25, 75))
            painter.drawText(bubble_rect, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self.speech_text)

        # 3. Police Car Sprite
        if self.frames:
            pix = self.frames[self.frame_index % len(self.frames)]
            draw_x = int((self.total_w - pix.width()) / 2)
            draw_y = self.bubble_h
            painter.drawPixmap(draw_x, draw_y, pix)

            # Atmospheric sweeping siren light glow
            siren_x = draw_x + int(pix.width() * 0.46)
            siren_y = draw_y + int(pix.height() * 0.18)
            glow_col = QColor(255, 30, 30, 45) if self.frame_index % 2 == 0 else QColor(30, 100, 255, 45)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(glow_col))
            painter.drawEllipse(QRectF(siren_x - 45, siren_y - 25, 90, 50))
