"""
Stereotypical PUC University Students Protest Widget.
Marching across the screen with rhythmic cadence bounce,
panelaço sparks, megaphones, Stanley cups, and tote bags,
chanting pro-Lula and anti-Bolsonaro slogans!
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor, QBrush, QPen, QPainterPath
import random
import math
import os

ACTIVE_PUC = []

def clear_all_protests():
    global ACTIVE_PUC
    for p in list(ACTIVE_PUC):
        p.close()
    ACTIVE_PUC.clear()

class PUCProtestWidget(QWidget):
    protest_exited = pyqtSignal()

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

        # Load marching frames (up to 4 dynamic frames)
        self.frames = []
        for i in range(4):
            path = f"assets/puc/puc_march_{i}.png"
            if os.path.exists(path):
                self.frames.append(QPixmap(path))

        # Dimensions: 480w x 325h
        self.total_w = 480
        self.total_h = 325
        self.bubble_h = 48
        self.setFixedSize(self.total_w, self.total_h)

        # Stereotypical PUC protest chants & slogans
        quotes = [
            "PUC: 🎶 'Recua, fascista, recua! O poder popular ta na rua!' 🎶",
            "ESTUDANTES: 'Nao vai ter golpe, vai ter picanha e pos-graduacao!' ✊",
            "PUC: 'Fora Bolsonaro! (Com todo respeito aos vizinhos do predio)'",
            "ESTUDANTES: 'Faz o L! O amor venceu o odio! Taokey?!' ✨",
            "PUC: 'Pelo fim do teto e ampliacao do matcha com aveia!' 🍵",
            "ESTUDANTES: 'Companheiro Lula, a PUC esta contigo ate o almoco!' 🚩",
            "PUC: 'Fascistas nao passarao no meu condominio!' ✊",
            "ESTUDANTES: 'Pela revogacao do teto e mais cristais energeticos!' ✨",
            "PUC: 'Sem anistia! (digitado do meu iPhone 15 Pro Max)' 📱"
        ]
        self.speech_text = random.choice(quotes)

        # Start position (just offscreen to the left)
        self.current_x = float(self.screen_rect.left() - self.total_w - 30)
        self.base_y = float(self.screen_rect.bottom() - self.total_h - 15)
        self.current_y = self.base_y
        self.move(round(self.current_x), round(self.current_y))

        # Rising protest particle sparks: [{'x': float, 'y': float, 'text': str, 'alpha': float}]
        self.chant_particles = []

        # March step animation timer (110ms interval)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._toggle_frame)
        self.anim_timer.start(110)

        # 60 FPS movement timer (16ms)
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self._step)
        self.move_timer.start(16)

        ACTIVE_PUC.append(self)
        self.show()

    def _toggle_frame(self):
        if self.frames:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.update()

    def _step(self):
        self.ticks += 1
        self.current_x += self.speed

        # Rhythmic demonstration cadence bounce
        cadence_bounce = abs(math.sin(self.current_x * 0.08)) * 3.8
        self.current_y = self.base_y - cadence_bounce

        # Spawn rising chant emoji particles above megaphone
        if self.ticks % 28 == 0:
            char_choice = random.choice(["✊", "✨", "🚩", "🎶", "🎵"])
            self.chant_particles.append({
                'x': float(100 + random.randint(-15, 15)),
                'y': float(self.bubble_h + 30),
                'text': char_choice,
                'alpha': 255.0
            })

        # Update particles
        for p in list(self.chant_particles):
            p['y'] -= 0.8
            p['x'] += 0.2
            p['alpha'] *= 0.95
            if p['alpha'] < 10 or p['y'] < 0:
                self.chant_particles.remove(p)

        self.move(round(self.current_x), round(self.current_y))

        # Exit screen check
        if self.current_x > self.screen_rect.right() + 40:
            self.anim_timer.stop()
            self.move_timer.stop()
            try:
                self.protest_exited.emit()
            except Exception:
                pass
            if self in ACTIVE_PUC:
                ACTIVE_PUC.remove(self)
            self.close()
            return

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Rising chant particles
        for p in self.chant_particles:
            painter.setFont(QFont("Segoe UI Emoji", 11))
            col = QColor(220, 20, 20, int(p['alpha']))
            painter.setPen(col)
            painter.drawText(int(p['x']), int(p['y']), p['text'])

        # 2. Speech Bubble on Top
        if self.speech_text:
            painter.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            bubble_rect = QRectF(15, 4, self.total_w - 30, self.bubble_h - 10)

            # Red-bordered protest speech bubble
            painter.setPen(QPen(QColor(180, 20, 20), 2.0))
            painter.setBrush(QBrush(QColor(255, 255, 245, 250)))
            painter.drawRoundedRect(bubble_rect, 8, 8)

            # Pointer tail
            tail = QPainterPath()
            tail.moveTo(100, self.bubble_h - 6)
            tail.lineTo(114, self.bubble_h - 6)
            tail.lineTo(107, self.bubble_h)
            tail.closeSubpath()
            painter.fillPath(tail, QBrush(QColor(255, 255, 245, 250)))
            painter.strokePath(tail, QPen(QColor(180, 20, 20), 2.0))

            painter.setPen(QColor(180, 20, 20))
            painter.drawText(bubble_rect, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self.speech_text)

        # 3. PUC Students Sprite
        if self.frames:
            pix = self.frames[self.frame_index % len(self.frames)]
            draw_x = int((self.total_w - pix.width()) / 2)
            draw_y = self.bubble_h
            painter.drawPixmap(draw_x, draw_y, pix)
