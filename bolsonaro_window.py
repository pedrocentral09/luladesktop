"""
Bolsonaro Peek-a-boo Corner Widget.
Pops up in the corner of the screen with smooth elastic easing,
firing the finger-gun gesture (arminha) with recoil and muzzle flashes!
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor, QBrush, QPen, QPainterPath
import random
import math
import os

ACTIVE_BOLSONARO = []

def clear_all_bolsonaro():
    global ACTIVE_BOLSONARO
    for b in list(ACTIVE_BOLSONARO):
        b.close()
    ACTIVE_BOLSONARO.clear()

class BolsonaroPeekWidget(QWidget):
    def __init__(self, screen_rect):
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
        self.total_w = 210
        self.total_h = 205
        self.bubble_h = 45
        self.setFixedSize(self.total_w, self.total_h)

        # Load frames (up to 4 dynamic frames)
        self.frames = []
        for i in range(4):
            path = f"assets/bolsonaro/bolsonaro_peek_{i}.png"
            if os.path.exists(path):
                self.frames.append(QPixmap(path))
        self.frame_index = 0

        # Quotes
        quotes = [
            "👉👉 E ai, companheiro! Taokey?!",
            "👉👉 Faz o L agora!",
            "👉👉 Olha o capitao na sua tela! Taokey?!",
            "👉👉 Acabou a mamata!",
            "👉👉 Eu avisei que a taxa vinha!"
        ]
        self.speech_text = random.choice(quotes)

        # Positioning: Bottom-Right corner
        self.target_x = float(self.screen_rect.right() - self.total_w - 20)
        self.peek_y = float(self.screen_rect.bottom() - self.total_h) # Fully visible
        self.hidden_y = float(self.screen_rect.bottom() + 10)         # Hidden offscreen below
        
        self.current_x = self.target_x
        self.current_y = self.hidden_y
        self.move(round(self.current_x), round(self.current_y))

        # Easing and timing configuration (60 FPS)
        self.anim_state = 'sliding_up'
        self.ticks = 0
        self.state_ticks = 0
        self.rise_duration = 32     # ~0.53 seconds smooth elastic rise
        self.peek_duration = 190    # ~3.1 seconds peeking & shooting
        self.retreat_duration = 26  # ~0.43 seconds cubic dive

        # Loop timer: 16ms (60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.timer.start(16)

        ACTIVE_BOLSONARO.append(self)
        self.show()

    def _step(self):
        self.ticks += 1
        self.state_ticks += 1

        if self.anim_state == 'sliding_up':
            progress = min(1.0, self.state_ticks / float(self.rise_duration))
            # Cubic ease-out curve
            eased = 1.0 - math.pow(1.0 - progress, 3)
            # Elastic overshoot bump
            overshoot = math.sin(progress * math.pi) * 7.0
            self.current_y = self.hidden_y - (self.hidden_y - self.peek_y) * eased - overshoot

            if progress >= 1.0:
                self.current_y = self.peek_y
                self.anim_state = 'peeking'
                self.state_ticks = 0

        elif self.anim_state == 'peeking':
            # Dynamic arminha firing sequence (12-tick rhythm)
            # 0..4: aiming (frame 0)
            # 5..6: firing blast (frame 1)
            # 7..9: recoil & shell ejection (frame 2)
            # 10..11: smug re-aiming (frame 3)
            cycle = (self.state_ticks // 3) % 4
            self.frame_index = cycle if self.frames else 0

            # Subtle breathing and swaying while peeking
            sway = math.sin(self.ticks * 0.08) * 1.5
            self.current_y = self.peek_y + sway

            if self.state_ticks >= self.peek_duration:
                self.anim_state = 'sliding_down'
                self.state_ticks = 0

        elif self.anim_state == 'sliding_down':
            progress = min(1.0, self.state_ticks / float(self.retreat_duration))
            # Cubic ease-in curve
            eased = math.pow(progress, 3)
            self.current_y = self.peek_y + (self.hidden_y - self.peek_y) * eased

            if progress >= 1.0:
                self.timer.stop()
                if self in ACTIVE_BOLSONARO:
                    ACTIVE_BOLSONARO.remove(self)
                self.close()
                return

        self.move(round(self.current_x), round(self.current_y))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Speech Bubble on top
        if self.speech_text and self.anim_state == 'peeking':
            painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
            bubble_rect = QRectF(6, 4, self.total_w - 12, 30)

            painter.setPen(QPen(QColor(20, 20, 20), 1.5))
            painter.setBrush(QBrush(QColor(255, 255, 240, 245)))
            painter.drawRoundedRect(bubble_rect, 6, 6)

            # Bubble pointer tail
            tail = QPainterPath()
            tail.moveTo(100, 34)
            tail.lineTo(110, 34)
            tail.lineTo(105, 40)
            tail.closeSubpath()
            painter.fillPath(tail, QBrush(QColor(255, 255, 240, 245)))
            painter.strokePath(tail, QPen(QColor(20, 20, 20), 1.5))

            painter.setPen(QColor(20, 100, 30))
            painter.drawText(bubble_rect, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self.speech_text)

        # 2. Bolsonaro Sprite
        if self.frames:
            pix = self.frames[self.frame_index % len(self.frames)]
            draw_x = int((self.total_w - pix.width()) / 2)
            draw_y = self.bubble_h
            painter.drawPixmap(draw_x, draw_y, pix)
