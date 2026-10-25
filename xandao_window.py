"""
Xandão (Alexandre de Moraes) Mouse Arrest Widget.
Triggered when the user closes a presidential meme brought by Lula!
Xandão descends dramatically with his black judicial robe from the sky,
winds up his golden gavel, slams it down with expanding shockwaves and screen shake,
locks the mouse cursor under a monocratic arrest warrant,
and frees the mouse under parole after a solemn detention period!
"""
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer, QRectF, QRect, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QFont, QFontMetrics, QColor, QBrush, QPen, QPainterPath, QCursor
import random
import math
import os
import ctypes

ACTIVE_XANDAO = []

def clear_all_xandao():
    global ACTIVE_XANDAO
    for x in list(ACTIVE_XANDAO):
        x._restore_cursor()
        x.close()
    ACTIVE_XANDAO.clear()

class XandaoArrestWidget(QWidget):
    arrest_finished = pyqtSignal()

    def __init__(self, screen_rect, sound_manager=None, target_pos=None):
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
        self.sound = sound_manager

        # Sprite dimensions (Xandão 4-frame dynamic editorial caricature)
        self.sprite_w = 250
        self.sprite_h = 205

        # Load Xandão frames (up to 4 dynamic frames)
        self.frames = []
        for i in range(4):
            path = f"assets/xandao/xandao_{i}.png"
            if os.path.exists(path):
                self.frames.append(QPixmap(path))
        if self.frames:
            self.sprite_w = self.frames[0].width()
            self.sprite_h = self.frames[0].height()
        self.frame_index = 0

        # Decrees / Monocratic quotes
        quotes = [
            "⚖️ DECISÃO MONOCRÁTICA!\nMouse preso preventivamente por 48 horas!",
            "⚖️ MULTA DE R$ 50.000 POR MINUTO\ne bloqueio imediato do cursor!",
            "⚖️ FECHOU O MEME?!\nInquérito das Fake News instaurado contra seu mouse!",
            "⚖️ ATENTADO CONTRA A DEMOCRACIA!\nO cursor vai passar uma noite na Papuda!",
            "⚖️ RECURSO NEGADO!\nMouse detido em regime fechado monocrático!"
        ]
        self.speech_text = random.choice(quotes)
        self.bubble_w = 0
        self.bubble_h = 0
        self.tail_h = 8

        # Target position around user's mouse cursor
        cursor_pt = target_pos or QCursor.pos()
        self.cursor_x = cursor_pt.x()
        self.cursor_y = cursor_pt.y()

        self._update_bubble_geometry()

        # Dramatic entrance: starts above screen
        self.start_y = max(float(self.screen_rect.top() - self.total_h - 40), self.base_y - 350)
        self.current_x = self.base_x
        self.current_y = self.start_y
        self.move(round(self.current_x), round(self.current_y))

        # Cursor lock state
        self.cursor_locked = False

        # Animation state machine & slowed-down stately pacing
        self.ticks = 0
        self.shake_ticks = 0
        self.descent_duration = 50    # ~0.83s smooth majestic glide from above
        self.windup_duration = 30     # ~0.50s dramatic pause with gavel raised
        self.strike_tick = self.descent_duration + self.windup_duration # tick 80
        self.decree_tick = self.strike_tick + 20                         # tick 100
        self.arrest_duration = 540    # ~9.0s total at 60 FPS (gives ~5.5s to read decree)
        self.parole_tick = self.arrest_duration - 110                    # tick 430 (~1.2s to read parole)

        # Shockwave list: [{'r': float, 'max_r': float, 'alpha': float}]
        self.shockwaves = []

        # 60 FPS timer (16ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.timer.start(16)

        ACTIVE_XANDAO.append(self)
        self.show()

    def _update_bubble_geometry(self):
        """Calcula dinamicamente a largura e altura do balão de fala estilo Lula para que todas as frases caibam perfeitamente."""
        if not self.speech_text:
            self.bubble_w = 0
            self.bubble_h = 0
            self.total_w = self.sprite_w + 30
            self.total_h = self.sprite_h + 15
        else:
            font = QFont("Segoe UI", 9, QFont.Weight.Bold)
            fm = QFontMetrics(font)

            # Largura confortável de até 290px para que as decisões judiciais caibam inteiras e com quebra suave
            max_inner_w = 290
            text_rect = fm.boundingRect(
                QRect(0, 0, max_inner_w, 1000),
                Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                self.speech_text
            )

            calc_w = max(text_rect.width() + 28, 180)
            calc_h = max(text_rect.height() + 18, 42)

            self.bubble_w = min(calc_w, 350)
            self.bubble_h = calc_h

            self.total_w = max(self.sprite_w + 30, self.bubble_w + 24)
            self.total_h = self.bubble_h + self.tail_h + self.sprite_h + 10

        self.setFixedSize(self.total_w, self.total_h)

        # Recalculate anchor so Xandão's gavel/handcuffs align with the target cursor
        draw_x = int((self.total_w - self.sprite_w) / 2)
        draw_y = (self.bubble_h + self.tail_h + 5) if (self.speech_text and self.bubble_w > 0) else 5
        self.base_x = float(self.cursor_x - (draw_x + 195))
        self.base_y = float(self.cursor_y - (draw_y + 170))

        # Keep strictly within screen bounds
        self.base_x = max(float(self.screen_rect.left() + 10), 
                          min(self.base_x, float(self.screen_rect.right() - self.total_w - 10)))
        self.base_y = max(float(self.screen_rect.top() + 10), 
                          min(self.base_y, float(self.screen_rect.bottom() - self.total_h - 10)))

    def _lock_cursor(self):
        if not self.cursor_locked:
            try:
                QApplication.setOverrideCursor(Qt.CursorShape.BlankCursor)
            except Exception:
                pass
            self.cursor_locked = True

    def _restore_cursor(self):
        if self.cursor_locked:
            try:
                QApplication.restoreOverrideCursor()
            except Exception:
                pass
            self.cursor_locked = False

    def closeEvent(self, event):
        self._restore_cursor()
        super().closeEvent(event)

    def _step(self):
        self.ticks += 1

        # 1. Dramatic Descending Entrance (cubic ease-out)
        if self.ticks <= self.descent_duration:
            progress = min(1.0, self.ticks / float(self.descent_duration))
            eased = 1.0 - math.pow(1.0 - progress, 3)
            self.current_y = self.start_y + (self.base_y - self.start_y) * eased
            self.frame_index = 0

        # 2. Wind-up before strike (gavel raised with intense focus)
        elif self.ticks < self.strike_tick:
            self.current_y = self.base_y
            self.frame_index = 1 if len(self.frames) > 1 else 0

        # 3. IMPACT GAVEL STRIKE MOMENT!
        elif self.ticks == self.strike_tick:
            self.frame_index = 2 if len(self.frames) > 2 else 1
            self.shake_ticks = 16
            self._lock_cursor()
            if self.sound:
                self.sound.play("xandao_gavel")
            # Trigger concentric shockwave rings
            self.shockwaves.append({'r': 8.0, 'max_r': 90.0, 'alpha': 255.0})
            self.shockwaves.append({'r': 2.0, 'max_r': 120.0, 'alpha': 220.0})

        # 4. Monocratic Decree Pose (holds solemn pose so user can read decree)
        elif self.ticks >= self.decree_tick and self.ticks < self.parole_tick:
            self.frame_index = 3 if len(self.frames) > 3 else (2 if len(self.frames) > 2 else 1)

        # 5. Parole release
        if self.ticks == self.parole_tick:
            self.speech_text = "⚖️ LIBERADO SOB CONDICIONAL!\nUso obrigatório de tornozeleira no cursor!"
            self._update_bubble_geometry()
            self._restore_cursor()
            # Minor release shockwave
            self.shockwaves.append({'r': 5.0, 'max_r': 65.0, 'alpha': 180.0})

        # Exit glide back up into the clouds (last 40 ticks ~0.67s)
        exit_start = self.arrest_duration - 40
        if self.ticks > exit_start:
            exit_progress = (self.ticks - exit_start) / 40.0
            eased_exit = math.pow(exit_progress, 2)
            self.current_y = self.base_y - 250 * eased_exit

        # Gavel strike impact screen shake
        shake_x = 0
        shake_y = 0
        if self.shake_ticks > 0:
            self.shake_ticks -= 1
            mag = int(self.shake_ticks * 0.9)
            shake_x = random.randint(-mag, mag)
            shake_y = random.randint(-mag, mag)

        # Pin mouse cursor to Xandão's golden handcuffs during monocratic detention
        if self.cursor_locked and self.ticks >= self.strike_tick and self.ticks < self.parole_tick:
            pix = self.frames[self.frame_index % len(self.frames)] if self.frames else None
            draw_x = int((self.total_w - (pix.width() if pix else self.sprite_w)) / 2)
            top_offset = (self.bubble_h + self.tail_h + 5) if (self.speech_text and self.bubble_w > 0) else 5
            handcuff_screen_x = int(self.current_x + draw_x + 195)
            handcuff_screen_y = int(self.current_y + top_offset + 170)
            try:
                ctypes.windll.user32.SetCursorPos(handcuff_screen_x, handcuff_screen_y)
            except Exception:
                pass

        # Update shockwaves
        for sw in list(self.shockwaves):
            sw['r'] += 4.5
            sw['alpha'] *= 0.88
            if sw['r'] >= sw['max_r'] or sw['alpha'] < 10:
                self.shockwaves.remove(sw)

        self.move(round(self.current_x + shake_x), round(self.current_y + shake_y))

        # Finish arrest and close
        if self.ticks >= self.arrest_duration:
            self.timer.stop()
            self._restore_cursor()
            try:
                self.arrest_finished.emit()
            except Exception:
                pass
            if self in ACTIVE_XANDAO:
                ACTIVE_XANDAO.remove(self)
            self.close()
            return

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        top_offset = (self.bubble_h + self.tail_h + 5) if (self.speech_text and self.bubble_w > 0) else 5

        # 1. Speech Bubble on Top (Identical design system to Lula's bubble!)
        if self.speech_text and self.bubble_w > 0:
            font = QFont("Segoe UI", 9, QFont.Weight.Bold)
            painter.setFont(font)

            bubble_x = (self.total_w - self.bubble_w) / 2
            bubble_y = 4
            bubble_rect = QRectF(bubble_x, bubble_y, self.bubble_w, self.bubble_h)

            # Bubble background (bright clean white with dark crisp border, exactly like Lula's)
            painter.setPen(QPen(QColor(35, 35, 35), 1.8))
            painter.setBrush(QBrush(QColor(255, 255, 255, 252)))
            painter.drawRoundedRect(bubble_rect, 8, 8)

            # Bubble pointer tail pointing down towards Xandão's bald head
            tail_x = self.total_w / 2
            tail_base_y = bubble_y + self.bubble_h
            tail = QPainterPath()
            tail.moveTo(tail_x - 6, tail_base_y)
            tail.lineTo(tail_x + 6, tail_base_y)
            tail.lineTo(tail_x, tail_base_y + self.tail_h)
            tail.closeSubpath()
            painter.fillPath(tail, QBrush(QColor(255, 255, 255, 252)))
            painter.strokePath(tail, QPen(QColor(35, 35, 35), 1.8))

            # Speech text with generous inner margins
            text_rect = bubble_rect.adjusted(10, 6, -10, -6)
            painter.setPen(QColor(20, 20, 20))
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self.speech_text)

        # 2. Draw Xandão Sprite
        if self.frames:
            pix = self.frames[self.frame_index % len(self.frames)]
            draw_x = int((self.total_w - pix.width()) / 2)
            draw_y = top_offset
            painter.drawPixmap(draw_x, draw_y, pix)

            # Handcuff position coordinates
            aura_x = draw_x + 195
            aura_y = draw_y + 170

            # Draw expanding golden shockwave rings radiating from gavel / handcuffs!
            for sw in self.shockwaves:
                r = sw['r']
                alpha = int(sw['alpha'])
                pen = QPen(QColor(255, 215, 0, alpha), 2.5)
                painter.setPen(pen)
                painter.setBrush(QBrush(QColor(255, 50, 50, int(alpha * 0.25))))
                painter.drawEllipse(QRectF(aura_x - r, aura_y - r, r * 2, r * 2))

            # Pulsing handcuffs aura while cursor is arrested
            if self.cursor_locked and self.ticks >= self.strike_tick:
                pulse = 12 + math.sin(self.ticks * 0.25) * 5
                painter.setPen(QPen(QColor(255, 215, 0, 220), 2))
                painter.setBrush(QBrush(QColor(255, 60, 60, 70)))
                painter.drawEllipse(QRectF(aura_x - pulse, aura_y - pulse, pulse * 2, pulse * 2))
