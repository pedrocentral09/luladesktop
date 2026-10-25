"""
MST & CUT Desktop Occupation Widget with Animated Tent Pitching.
Triggered when the user's computer is inactive for > 30 seconds (idle / improductive desktop).
Militants in MST caps and CUT shirts pitch multiple campsite tents across the screen.
When the user moves the mouse again, a 5-second eviction countdown begins,
followed by a Federal Police raid where militants comically panic and sprint off-screen!
"""
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF, QRect, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QFont, QFontMetrics, QColor, QBrush, QPen, QPainterPath, QCursor
import random
import math
import os
from police_window import PoliceCarWidget

ACTIVE_MST_INVASIONS = []
ACTIVE_MST_TENTS = []

def clear_all_mst_invasions():
    global ACTIVE_MST_INVASIONS, ACTIVE_MST_TENTS
    for t in list(ACTIVE_MST_TENTS):
        t.close()
    ACTIVE_MST_TENTS.clear()
    for inv in list(ACTIVE_MST_INVASIONS):
        inv.close()
    ACTIVE_MST_INVASIONS.clear()

# =========================================================================
# 1. ANIMATED TENT WIDGET (Barraca Vermelha do MST com Construção em Fases)
# =========================================================================
class MSTTentWidget(QWidget):
    def __init__(self, x, y, start_delay_ticks=0, tent_index=1):
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

        self.tent_w = 150
        self.tent_h = 110
        self.setFixedSize(self.tent_w, self.tent_h)
        self.move(int(x), int(y))

        # Load construction stages (0: stakes, 1: low pole, 2: halfway, 3: pitched, 4: pot/smoke)
        self.stages = []
        for i in range(5):
            path = f"assets/mst/tent_stage_{i}.png"
            if os.path.exists(path):
                self.stages.append(QPixmap(path))
        self.collapse_pix = QPixmap("assets/mst/tent_collapse.png") if os.path.exists("assets/mst/tent_collapse.png") else None

        self.current_stage = 0
        self.ticks = 0
        self.start_delay = start_delay_ticks
        self.tent_index = tent_index
        self.is_collapsed = False
        self.collapse_ticks = 0
        self.opacity = 1.0

        # Smoke particles for cooking pot at stage 4: [{'x': float, 'y': float, 'r': float, 'alpha': float}]
        self.smoke_particles = []

        # 60 FPS update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.timer.start(16)

        ACTIVE_MST_TENTS.append(self)
        self.show()

    def _step(self):
        self.ticks += 1

        if self.is_collapsed:
            self.collapse_ticks += 1
            if self.collapse_ticks > 25:
                self.opacity = max(0.0, 1.0 - (self.collapse_ticks - 25) / 25.0)
                self.setWindowOpacity(self.opacity)
            if self.collapse_ticks >= 50 or self.opacity <= 0.0:
                self.timer.stop()
                if self in ACTIVE_MST_TENTS:
                    ACTIVE_MST_TENTS.remove(self)
                self.close()
                return
            self.update()
            return

        # Construction progression
        if self.ticks > self.start_delay and self.stages:
            active_ticks = self.ticks - self.start_delay
            # Each stage takes ~24 ticks (~0.40s) to build
            calc_stage = min(len(self.stages) - 1, int(active_ticks / 24))
            self.current_stage = calc_stage

        # At stage 4 (camp life): feijoada steam/smoke particles!
        if self.current_stage >= 4 and self.ticks % 14 == 0:
            pot_x = 120
            pot_y = 78
            self.smoke_particles.append({
                'x': float(pot_x + random.randint(-3, 3)),
                'y': float(pot_y),
                'r': 3.5,
                'alpha': 180.0
            })

        # Update smoke
        for p in list(self.smoke_particles):
            p['y'] -= 0.7
            p['x'] += random.uniform(-0.2, 0.4)
            p['r'] += 0.12
            p['alpha'] *= 0.94
            if p['alpha'] < 10 or p['y'] < 0:
                self.smoke_particles.remove(p)

        self.update()

    def collapse(self):
        """Disparado quando a polícia chega: a barraca desaba com nuvem de poeira e é abandonada!"""
        self.is_collapsed = True
        self.collapse_ticks = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Draw collapsed frame
        if self.is_collapsed:
            if self.collapse_pix and not self.collapse_pix.isNull():
                painter.drawPixmap(0, 0, self.collapse_pix)
            return

        # 2. Draw current building stage
        if self.stages:
            pix = self.stages[min(self.current_stage, len(self.stages) - 1)]
            painter.drawPixmap(0, 0, pix)

        # 3. Draw active cooking smoke particles
        for p in self.smoke_particles:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(230, 230, 230, int(p['alpha']))))
            painter.drawEllipse(QRectF(p['x'] - p['r'], p['y'] - p['r'], p['r'] * 2, p['r'] * 2))

# =========================================================================
# 2. MST INVASION PARADE & OCCUPATION WIDGET
# =========================================================================
class MSTInvasionWidget(QWidget):
    invasion_finished = pyqtSignal()

    def __init__(self, screen_rect, sound_manager=None):
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

        # Total canvas: 500w x 340h (space for speech bubble + countdown + militants)
        self.total_w = 500
        self.total_h = 340
        self.bubble_h = 58
        self.tail_h = 8
        self.setFixedSize(self.total_w, self.total_h)

        # Load Pitching frames (assets/mst/mst_pitch_0..3.png)
        self.pitch_frames = []
        for i in range(4):
            path = f"assets/mst/mst_pitch_{i}.png"
            if os.path.exists(path):
                self.pitch_frames.append(QPixmap(path))

        # Load Panic Fleeing frames (assets/mst/mst_flee_0..3.png)
        self.flee_frames = []
        for i in range(4):
            path = f"assets/mst/mst_flee_{i}.png"
            if os.path.exists(path):
                self.flee_frames.append(QPixmap(path))

        self.frame_index = 0
        self.ticks = 0

        # State machine: 'occupying' -> 'countdown' -> 'fleeing'
        self.state = 'occupying'
        self.countdown_ticks = 300  # 300 ticks = 5.0 seconds at 60 FPS
        self.countdown_sec = 5

        # Speed and positioning
        self.speed = 1.6
        self.current_x = float(self.screen_rect.left() - self.total_w - 20)
        self.base_y = float(self.screen_rect.bottom() - self.total_h - 10)
        self.current_y = self.base_y
        self.move(round(self.current_x), round(self.current_y))

        # Initial mouse position to detect when user moves the mouse again!
        self.last_cursor_pos = QCursor.pos()
        self.mouse_moved_ticks = 0

        # Slogans & Improductivity arguments
        self.occupy_quotes = [
            "🚩 MST & CUT: 'DESKTOP IMPRODUTIVO HÁ MAIS DE 30 SEGUNDOS!\nOCUPAÇÃO LEGÍTIMA E REFORMA AGRÁRIA!' 🚩",
            "🚩 'ÁREA PARADA HÁ MEIO MINUTO! Desapropriação dos pixels!\nAqui vai ter horta e picanha popular!' 🚩",
            "🚩 'QUEM NÃO MEXE O MOUSE PERDE A TERRA!\nMonta o acampamento na Área de Trabalho!' 🚩",
            "🚩 'LATIFÚNDIO DIGITAL OCUPADO!\nReforma agrária nos pixels com amor e feijoada!' 🚩"
        ]
        self.speech_text = random.choice(self.occupy_quotes)

        # Rising protest particle sparks: [{'x': float, 'y': float, 'text': str, 'alpha': float}]
        self.chant_particles = []

        # Spawn multiple campsite tents across the screen!
        self.tents = []
        self._spawn_multiple_tents()

        # March cadence animation timer (110ms interval)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._toggle_frame)
        self.anim_timer.start(110)

        # 60 FPS movement & state timer (16ms)
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self._step)
        self.move_timer.start(16)

        # Play militant march sound
        if self.sound:
            self.sound.play("mst_invasion")

        ACTIVE_MST_INVASIONS.append(self)
        self.show()

    def _spawn_multiple_tents(self):
        """Cria várias barracas do MST espalhadas pelo desktop, com construção animada em fases escalonadas!"""
        scr = self.screen_rect
        ground_y = scr.bottom() - 125

        # 4 distinct campsite locations across the desktop
        tent_positions = [
            (scr.left() + 70, ground_y, 0),                        # Barraca 1 (começa imediatamente)
            (scr.left() + int(scr.width() * 0.35), ground_y + 4, 25), # Barraca 2 (atraso de ~0.4s)
            (scr.left() + int(scr.width() * 0.62), ground_y - 2, 50), # Barraca 3 (atraso de ~0.8s)
            (scr.right() - 210, ground_y + 2, 75)                  # Barraca 4 (atraso de ~1.2s)
        ]

        for idx, (tx, ty, delay) in enumerate(tent_positions):
            tent = MSTTentWidget(tx, ty, start_delay_ticks=delay, tent_index=idx + 1)
            self.tents.append(tent)

    def _toggle_frame(self):
        frames = self.flee_frames if self.state == 'fleeing' else self.pitch_frames
        if frames:
            self.frame_index = (self.frame_index + 1) % len(frames)
        self.update()

    def _step(self):
        self.ticks += 1

        # =====================================================================
        # PHASE 1: OCCUPYING (Militants march and pitch camp on idle desktop)
        # =====================================================================
        if self.state == 'occupying':
            # Stop militant group in a visible center-left spot to oversee the occupation
            target_hold_x = float(self.screen_rect.left() + 35)
            if self.current_x < target_hold_x:
                self.current_x += self.speed
            else:
                self.current_x = target_hold_x

            # Rhythmic cadence bounce
            bounce = abs(math.sin(self.ticks * 0.12)) * 3.2
            self.current_y = self.base_y - bounce

            # Rising chant particles
            if self.ticks % 24 == 0:
                char_choice = random.choice(["🚩", "✊", "🔨", "🍲", "✨", "📢"])
                self.chant_particles.append({
                    'x': float(120 + random.randint(-20, 20)),
                    'y': float(self.bubble_h + 35),
                    'text': char_choice,
                    'alpha': 255.0
                })

            # Check if user moved the mouse!
            current_cur = QCursor.pos()
            dx = abs(current_cur.x() - self.last_cursor_pos.x())
            dy = abs(current_cur.y() - self.last_cursor_pos.y())
            if dx > 4 or dy > 4:
                # USER IS BACK! TRIGGER 5-SECOND EVICTION WARNING!
                self.state = 'countdown'
                self.countdown_ticks = 300 # 5.0 seconds
                self.countdown_sec = 5
                self.speech_text = "🚨 ALERTA GERAL! O LATIFUNDIÁRIO MEXEU O MOUSE!\nA POLÍCIA FEDERAL CHEGA EM 5 SEGUNDOS! 🚨"
                if self.sound:
                    self.sound.play("eviction_alert")

        # =====================================================================
        # PHASE 2: 5-SECOND EVICTION COUNTDOWN
        # =====================================================================
        elif self.state == 'countdown':
            self.countdown_ticks -= 1
            sec_left = max(1, math.ceil(self.countdown_ticks / 60))
            if sec_left != self.countdown_sec:
                self.countdown_sec = sec_left
                self.speech_text = f"🚨 O LATIFUNDIÁRIO MEXEU O MOUSE!\nA FEDERAL CHEGA EM {self.countdown_sec}s! CATA AS PANELAS! 🚨"

            # Nervous tremble / jitter before fleeing
            shake_x = random.randint(-2, 2)
            shake_y = random.randint(-1, 1)
            self.current_y = self.base_y + shake_y

            # Panic particles: sweat drops and warnings
            if self.ticks % 10 == 0:
                self.chant_particles.append({
                    'x': float(random.randint(80, 280)),
                    'y': float(self.bubble_h + 40),
                    'text': random.choice(["💧", "😱", "🏃", "⚠️"]),
                    'alpha': 255.0
                })

            # When 5 seconds expire: LAUNCH POLICE RAID & MILITANTS FLEE!
            if self.countdown_ticks <= 0:
                self.state = 'fleeing'
                self.speed = 8.5 # High speed panic sprint!
                self.speech_text = "😱 'FUDEU! A FEDERAL TÁ AÍ! CORRE, COMPANHEIRO!'"
                self.frame_index = 0

                # Collapse all campsite tents immediately!
                for tent in self.tents:
                    tent.collapse()

                # Summon Federal Police cruiser chasing them!
                police_car = PoliceCarWidget(self.screen_rect, speed=5.0)
                if self.sound:
                    self.sound.play("police_siren")

        # =====================================================================
        # PHASE 3: PANIC FLEEING (Sprinting off-screen from police car)
        # =====================================================================
        elif self.state == 'fleeing':
            self.current_x += self.speed
            # High cartoon panic running bounce
            run_bounce = abs(math.sin(self.ticks * 0.28)) * 5.0
            self.current_y = self.base_y - run_bounce

            # Dust particles behind fleeing militants
            if self.ticks % 6 == 0:
                self.chant_particles.append({
                    'x': float(random.randint(20, 70)),
                    'y': float(self.total_h - 25),
                    'text': random.choice(["💨", "💨", "💥"]),
                    'alpha': 230.0
                })

            # Check if militants have escaped completely off the right edge of the screen
            if self.current_x > self.screen_rect.right() + 60:
                self.anim_timer.stop()
                self.move_timer.stop()
                try:
                    self.invasion_finished.emit()
                except Exception:
                    pass
                if self in ACTIVE_MST_INVASIONS:
                    ACTIVE_MST_INVASIONS.remove(self)
                self.close()
                return

        # Update rising particles
        for p in list(self.chant_particles):
            p['y'] -= 1.0
            p['alpha'] *= 0.94
            if p['alpha'] < 10 or p['y'] < 0:
                self.chant_particles.remove(p)

        self.move(round(self.current_x), round(self.current_y))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Rising chant / panic particles
        for p in self.chant_particles:
            painter.setFont(QFont("Segoe UI Emoji", 11))
            col = QColor(220, 20, 20, int(p['alpha']))
            painter.setPen(col)
            painter.drawText(int(p['x']), int(p['y']), p['text'])

        # 2. Dynamic Speech Bubble on Top
        if self.speech_text:
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            bubble_rect = QRectF(15, 6, self.total_w - 30, self.bubble_h)

            if self.state == 'countdown':
                # Flashing warning yellow/red border
                flash_col = QColor(255, 30, 30) if (self.ticks % 16 < 8) else QColor(240, 160, 0)
                painter.setPen(QPen(flash_col, 2.5))
                painter.setBrush(QBrush(QColor(255, 255, 240, 252)))
            elif self.state == 'fleeing':
                painter.setPen(QPen(QColor(220, 20, 20), 2.2))
                painter.setBrush(QBrush(QColor(255, 245, 245, 252)))
            else:
                # Iconic MST red/gold border
                painter.setPen(QPen(QColor(180, 20, 20), 2.0))
                painter.setBrush(QBrush(QColor(255, 255, 250, 252)))

            painter.drawRoundedRect(bubble_rect, 8, 8)

            # Bubble pointer tail pointing down towards militants
            tail_x = 130 if self.state != 'fleeing' else 220
            tail = QPainterPath()
            tail.moveTo(tail_x - 7, self.bubble_h + 6)
            tail.lineTo(tail_x + 7, self.bubble_h + 6)
            tail.lineTo(tail_x, self.bubble_h + 6 + self.tail_h)
            tail.closeSubpath()
            painter.fillPath(tail, painter.brush())
            painter.strokePath(tail, painter.pen())

            # Text
            text_col = QColor(180, 20, 20) if self.state != 'countdown' else QColor(200, 15, 15)
            painter.setPen(text_col)
            painter.drawText(bubble_rect.adjusted(8, 4, -8, -4),
                             Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                             self.speech_text)

        # 3. Draw Countdown HUD badge when in countdown mode
        if self.state == 'countdown':
            hud_rect = QRectF(140, self.bubble_h + 16, 220, 28)
            painter.setPen(QPen(QColor(255, 255, 255), 1.5))
            painter.setBrush(QBrush(QColor(210, 20, 20, 235)))
            painter.drawRoundedRect(hud_rect, 14, 14)
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(hud_rect, Qt.AlignmentFlag.AlignCenter, f"🚓 POLÍCIA EM: {self.countdown_sec}s ⚠️")

        # 4. Draw Militants Sprite (Pitching or Panic Fleeing)
        frames = self.flee_frames if self.state == 'fleeing' else self.pitch_frames
        if frames:
            pix = frames[self.frame_index % len(frames)]
            draw_x = int((self.total_w - pix.width()) / 2)
            draw_y = self.bubble_h + self.tail_h + 8
            painter.drawPixmap(draw_x, draw_y, pix)
