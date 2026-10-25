"""
Desktop Lula - Main Pet Window and State Machine.
Presidential Edition:
- Dark suit (paletó) & Brazilian presidential sash (faixa presidencial)
- Mechanic: Steals and hides mouse inside his paletó, locking cursor for a few seconds!
"""
from PyQt6.QtWidgets import QWidget, QMenu, QApplication
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont, QFontMetrics, QPen, QBrush, QPainterPath, QCursor
import random
import math
import os
import ctypes

from config import load_config
from sound_manager import SoundManager
from drops import DropWidget
from meme_window import MemeWindow
from desktop_scanner import scan_real_desktop_icons
from plane_window import JanjaPlaneWidget, clear_all_planes
from police_window import PoliceCarWidget, clear_all_police
from bolsonaro_window import BolsonaroPeekWidget, clear_all_bolsonaro
from puc_window import PUCProtestWidget, clear_all_protests
from xandao_window import XandaoArrestWidget, clear_all_xandao
from mst_window import MSTInvasionWidget, clear_all_mst_invasions

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_system_idle_seconds():
    try:
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            return millis / 1000.0
    except Exception:
        pass
    return 0.0

# States
STATE_IDLE = "IDLE"
STATE_WANDER = "WANDER"
STATE_SNEAK_MOUSE = "SNEAK_MOUSE"   # Furto sutil e silencioso do mouse
STATE_HIDE_MOUSE = "HIDE_MOUSE"     # Mouse escondido no paletó
STATE_STEAL_ICON = "STEAL_ICON"     # Roubando ícones do desktop/barra de tarefas
STATE_ANGRY = "ANGRY"               # Revoltado porque fecharam o aviso/meme!
STATE_HIDE_FROM_POLICE = "HIDE_FROM_POLICE" # Escondido da viatura do Moro e Deltan!
STATE_FETCH_MEME_EDGE = "FETCH_MEME_EDGE"   # Caminha até o canto da tela para buscar o meme!
STATE_DRAG_MOUSE = "DRAG_MOUSE"
STATE_BRING_MEME = "BRING_MEME"
STATE_FLEE = "FLEE"

class LulaPetWindow(QWidget):
    def __init__(self, config=None):
        super().__init__()
        
        self.config = config or load_config()
        self.sound = SoundManager(enabled=self.config.get("sounds_enabled", True))
        
        # Transparent, topmost, borderless
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

        # Pet size & scale for High-Definition Editorial Caricatures
        self.scale = self.config.get("scale", 1.0)
        self.sprite_w = int(140 * self.scale)
        self.sprite_h = int(185 * self.scale)
        self.bubble_w = 0
        self.bubble_h = 0
        self.tail_h = 8
        self.total_w = self.sprite_w + 30
        self.total_h = self.sprite_h + 15
        self.setFixedSize(self.total_w, self.total_h)

        # Sprites
        self.sprites = {}
        self._load_sprites()

        # State machine variables
        self.state = STATE_WANDER
        self.facing_right = True
        self.frame_index = 0
        self.frame_timer = 0
        self.state_ticks = 0
        self.paused = False

        # Cursor lock inside paletó
        self.cursor_hidden = False
        self.mouse_hide_duration = 0

        # Stolen icons (Desktop & Taskbar)
        self.stolen_icons = {}
        self.current_stolen_icon = None
        self.stolen_icon_name = ""
        self.stolen_icon_timer = 0
        self.icon_steal_target_type = "taskbar" # 'taskbar' or 'desktop'
        self._load_stolen_icons()

        # Positions
        screen = QApplication.primaryScreen().availableGeometry()
        self.screen_rect = screen
        self.pos_x = float(screen.center().x())
        self.pos_y = float(screen.center().y())
        margin = 120
        self.target_x = float(random.randint(self.screen_rect.left() + margin, self.screen_rect.right() - margin))
        self.target_y = float(random.randint(self.screen_rect.top() + margin, self.screen_rect.bottom() - margin))

        # Meme drag state
        self.current_meme_window = None

        # Trails
        self.steps_count = 0

        # Speech bubble
        self.speech_text = ""
        self.speech_timer = 0

        # Dynamic Facial Emotion & Emote System
        self.active_emote = None
        self.emote_timer = 0

        # Main loop timer (60 FPS buttery smooth locomotion)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_loop)
        self.timer.start(self.config.get("tick_rate_ms", 16))

        # Action scheduler (~30 seconds between special actions)
        action_sec = float(self.config.get("action_interval_seconds", 30.0))
        self.action_interval = int(action_sec * (1000 / self.config.get("tick_rate_ms", 16)))
        # Start initial action after an introductory period of ~15-20s
        self.action_timer = int(self.action_interval * 0.45)

        # Inactivity detection for MST & CUT occupation (>30 seconds of user idle)
        self.mst_invasion_active = False
        self.last_user_input_pos = QCursor.pos()
        self.user_idle_ticks = 0

        # Smooth Locomotion & Inertia Physics
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.stride_dist = 0.0
        self.locomotion_bob = 0.0

        # Initial move
        self._sync_position()
        self.say("Presidente na area! De volta ao trabalho, companheiro!", duration_sec=3)
        self.show()

    def _load_sprites(self):
        sprites_dir = "assets/sprites"
        categories = ['idle', 'walk', 'chase', 'drag', 'hide', 'sneak', 'angry', 'crouch']
        for cat in categories:
            self.sprites[f"{cat}_r"] = []
            self.sprites[f"{cat}_l"] = []
            
            f_idx = 0
            while True:
                f_r = os.path.join(sprites_dir, f"{cat}_r_{f_idx}.png")
                f_l = os.path.join(sprites_dir, f"{cat}_l_{f_idx}.png")
                if os.path.exists(f_r) and os.path.exists(f_l):
                    pix_r = QPixmap(f_r).scaled(self.sprite_w, self.sprite_h, 
                                                Qt.AspectRatioMode.KeepAspectRatio, 
                                                Qt.TransformationMode.SmoothTransformation)
                    pix_l = QPixmap(f_l).scaled(self.sprite_w, self.sprite_h, 
                                                Qt.AspectRatioMode.KeepAspectRatio, 
                                                Qt.TransformationMode.SmoothTransformation)
                    self.sprites[f"{cat}_r"].append(pix_r)
                    self.sprites[f"{cat}_l"].append(pix_l)
                    f_idx += 1
                else:
                    break

    def _load_stolen_icons(self):
        icons_dir = "assets/stolen_icons"
        if os.path.exists(icons_dir):
            for f in os.listdir(icons_dir):
                if f.endswith('.png'):
                    name = os.path.splitext(f)[0]
                    pix = QPixmap(os.path.join(icons_dir, f)).scaled(30, 30, 
                                                                     Qt.AspectRatioMode.KeepAspectRatio, 
                                                                     Qt.TransformationMode.SmoothTransformation)
                    self.stolen_icons[name] = pix

    def _update_bubble_geometry(self):
        """Calcula dinamicamente a largura e altura do balão de fala para que o texto caiba perfeitamente!"""
        if not self.speech_text:
            self.bubble_w = 0
            self.bubble_h = 0
            self.total_w = self.sprite_w + 30
            self.total_h = self.sprite_h + 15
        else:
            font = QFont("Segoe UI", 9, QFont.Weight.Bold)
            fm = QFontMetrics(font)

            # Largura confortável de até 310px para frases longas não ficarem espremidas
            max_inner_w = 270
            text_rect = fm.boundingRect(
                QRect(0, 0, max_inner_w, 1000),
                Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                self.speech_text
            )

            # Espaçamento interno generoso para respiração do texto
            calc_w = max(text_rect.width() + 28, 120)
            calc_h = max(text_rect.height() + 16, 32)

            self.bubble_w = min(calc_w, 320)
            self.bubble_h = calc_h
            self.tail_h = 8

            self.total_w = max(self.sprite_w + 30, self.bubble_w + 20)
            self.total_h = self.sprite_h + self.bubble_h + self.tail_h + 10

        self.setFixedSize(self.total_w, self.total_h)
        self._sync_position()

    def show_emote(self, emote_name, duration_sec=2.5):
        """Ativa um emote/expressão flutuante acima da cabeça do Lula."""
        self.active_emote = emote_name
        self.emote_timer = int(duration_sec * (1000 / self.config.get("tick_rate_ms", 16)))
        self.update()

    def say(self, text, duration_sec=3):
        if not self.config.get("speech_bubbles_enabled", True):
            return
        self.speech_text = text
        # Frases longas ganham tempo de leitura proporcional (mínimo de 3.5s até 6.5s)
        auto_duration = max(duration_sec, len(text) * 0.075 + 1.8)
        self.speech_timer = int(auto_duration * (1000 / self.config.get("tick_rate_ms", 16)))

        # Detecção contextual de expressões e emotes dinâmicos
        lower = text.lower()
        if any(w in lower for w in ["banco", "nubank", "itau", "pix", "grana", "dinheiro"]):
            self.show_emote("pix", duration_sec=3.2)
        elif any(w in lower for w in ["bolsonaro", "capitao", "desgoverno", "heranca maldita", "orlando"]):
            self.show_emote("culpar", duration_sec=3.2)
        elif any(w in lower for w in ["picanha", "cerveja", "churrasco"]):
            self.show_emote("picanha", duration_sec=3.5)
        elif any(w in lower for w in ["amor", "paz", "prouni", "alegria"]):
            self.show_emote("amor", duration_sec=3.0)
        elif any(w in lower for w in ["fechou", "censura", "inquerito", "stf", "castigo"]):
            self.show_emote("raiva", duration_sec=3.0)

        self._update_bubble_geometry()
        self.update()

    def _reset_action_timer(self):
        """Reseta o cronômetro para a próxima ação especial (cerca de uma ação a cada ~30 segundos)."""
        action_sec = float(self.config.get("action_interval_seconds", 30.0))
        # Variação natural e agradável de +/- 10% (ex: 27s a 33s)
        jitter = random.uniform(0.9, 1.1)
        self.action_interval = int(action_sec * jitter * (1000 / self.config.get("tick_rate_ms", 16)))
        self.action_timer = 0

    def _trigger_scheduled_action(self):
        """Dispara uma ação especial aleatória com distribuição equilibrada a cada ~30s."""
        self._reset_action_timer()

        actions = []
        weights = []

        if self.config.get("mouse_steal_enabled", True):
            actions.append("sneak_mouse")
            weights.append(0.25) # 25% de chance: roubo sutil do mouse

        actions.append("steal_icon")
        weights.append(0.20)     # 20% de chance: surrupiar ícone real

        actions.append("bring_meme")
        weights.append(0.15)     # 15% de chance: trazer meme/decreto

        actions.append("police_raid")
        weights.append(0.12)     # 12% de chance: viatura da PF (Moro & Deltan)

        actions.append("janja_plane")
        weights.append(0.10)     # 10% de chance: avião da Janja

        actions.append("bolsonaro_peek")
        weights.append(0.10)     # 10% de chance: Bolsonaro no canto

        actions.append("puc_protest")
        weights.append(0.08)     # 8% de chance: passeata da PUC

        choice = random.choices(actions, weights=weights, k=1)[0]

        if choice == "sneak_mouse":
            self.start_sneak_mouse()
        elif choice == "steal_icon":
            self.start_steal_icon()
        elif choice == "bring_meme":
            self.start_bring_meme()
        elif choice == "police_raid":
            self.summon_police_raid()
        elif choice == "janja_plane":
            self.summon_janja_plane()
        elif choice == "bolsonaro_peek":
            self.summon_bolsonaro_peek()
        elif choice == "puc_protest":
            self.summon_puc_protest()

    def blame_bolsonaro(self):
        """Dispara um pronunciamento oficial culpando o Bolsonaro por algo aleatório no computador."""
        bolsonaro_blames = [
            "O Windows ta travando? Culpa do Bolsonaro!",
            "Se o mouse sumir, e culpa dos 4 anos de desgoverno!",
            "A bateria descarregou por causa do capitao!",
            "A internet oscilou? Sabotagem da heranca maldita!",
            "O Chrome comeu sua memoria RAM? Culpa do governo anterior!",
            "O cafe esfriou? Ja sabe de quem e a culpa...",
            "Nao fui eu que peguei o mouse, foi o pessoal de Orlando!",
            "Qualquer bug nesta maquina veio da gestao passada!",
            "Se esquentar seu processador, e culpa do desmonte anterior!"
        ]
        self.say(random.choice(bolsonaro_blames), duration_sec=3.5)
        self.sound.play("laugh")

    def ask_for_bank_app(self):
        """Lula procura e pergunta onde está o aplicativo do banco."""
        bank_questions = [
            "Companheiro, onde ta o app do banco?",
            "Onde fica o app do banco nessa tela? E so pra uma checagem solidaria...",
            "Cade o app do Nubank ou Itau? O Haddad mandou perguntar!",
            "Voce escondeu o app do banco em alguma pasta, companheiro?",
            "Aponta o mouse pro app do banco pra eu ver se o Pix caiu!"
        ]
        self.say(random.choice(bank_questions), duration_sec=3.5)
        self.sound.play("grab")
        # Anda até uma área da tela como se estivesse procurando
        self.state = STATE_WANDER
        self.state_ticks = 0
        self.target_x = float(self.screen_rect.left() + random.choice([35, 120, 200]))
        self.target_y = float(self.screen_rect.bottom() - random.choice([65, 120, 180]))

    def summon_janja_plane(self):
        """Passa o Aerolula voando no topo da tela com a Janja na janela puxando uma faixa de compras!"""
        self._reset_action_timer()
        JanjaPlaneWidget(self.screen_rect)
        self.sound.play("plane_flyby")
        
        plane_quotes = [
            "Olha o Aerolula passando! Tchau, Janja!",
            "Boa viagem, Janja! Traz um sofa novo de Paris pra mim!",
            "La vai a primeira-dama comprar mais um sofa em Milao!",
            "Gastando com responsabilidade internacional!",
            "Tchau, companheira! Nao esquece meu chocolate de Londres!"
        ]
        self.say(random.choice(plane_quotes), duration_sec=4)

    def summon_police_raid(self):
        """Passa a viatura da Lava Jato com Sérgio Moro e Deltan Dallagnol enquanto Lula se esconde apavorado!"""
        self._reset_action_timer()
        self._restore_cursor_safety()
        self.state = STATE_HIDE_FROM_POLICE
        self.state_ticks = 0

        # Som da sirene da polícia
        self.sound.play("police_siren")
        self.show_emote("susto", duration_sec=4.5)

        # Lula entra em pânico e se esconde!
        panic_quotes = [
            "Ai meu Deus, a Federal! O sitio e de um amigo meu!",
            "Nao e meu nem o triplex nem o sitio, juro por Deus!",
            "Cade o Zanin?! Avisa meus advogados!",
            "Essa conducao coercitiva e armacao do Moro!",
            "Se abaixa, companheiro! E o PowerPoint do Deltan!"
        ]
        self.say(random.choice(panic_quotes), duration_sec=4.5)

        # Spawna a viatura da Polícia Federal
        police_car = PoliceCarWidget(self.screen_rect)
        police_car.car_exited.connect(self.on_police_passed)

    def on_police_passed(self):
        """Quando a viatura sai da tela, Lula se levanta aliviado!"""
        if self.state == STATE_HIDE_FROM_POLICE:
            relief_quotes = [
                "Ufa... Quase que eu volto pra Curitiba!",
                "Passou direto! O Zanin me salvou de novo!",
                "Essa tentativa de golpe do Moro nao deu em nada!",
                "Nao acharam o triplex! De volta ao trabalho, companheiro!"
            ]
            self.say(random.choice(relief_quotes), duration_sec=3)
            self.sound.play("laugh")
            self.state = STATE_WANDER
            self.state_ticks = 0

    def summon_bolsonaro_peek(self):
        """Bolsonaro aparece no canto da tela fazendo a arminha com os dedos (👉👉)!"""
        self._reset_action_timer()
        BolsonaroPeekWidget(self.screen_rect)
        self.sound.play("arminha")

        # Lula reage olhando para o canto
        self.facing_right = True # Olha para o canto inferior direito
        bolsonaro_reactions = [
            "Olha ele ai no canto! Eu nao disse que a culpa era dele?!",
            "La vem a heranca maldita fazendo arminha no meu Windows!",
            "Sai pra la, capitao! Aqui nao tem sigilo de 100 anos!",
            "Fazendo arminha no meu desktop?! Isso e atentado!",
            "Chama o Dino! O capitao ta fazendo arminha no canto da tela!"
        ]
        self.say(random.choice(bolsonaro_reactions), duration_sec=3.5)

    def summon_puc_protest(self):
        """Passa a passeata de estudantes estereotipados da PUC com faixas, copos Stanley e apitos pró-Lula!"""
        self._reset_action_timer()
        PUCProtestWidget(self.screen_rect)
        self.sound.play("protesto_puc")

        # Lula fica animado e apoia a manifestação estudantil!
        self.facing_right = True
        puc_cheers = [
            "Olha a juventude combativa da PUC ai, companheiro!",
            "Essa e a verdadeira consciencia de classe com bolsa de grife!",
            "Companheiros da PUC, a luta continua depois do estagio!",
            "Belo cartaz, companheira! So faltou citar o Haddad!",
            "Abaixo o fascismo, viva a picanha e o ProUni!",
            "Com esse protesto elegante da PUC o Bolsonaro nao volta nunca mais!"
        ]
        self.say(random.choice(puc_cheers), duration_sec=4)

    def summon_xandao_arrest(self):
        """Alexandre de Moraes desce com toga preta, bate o martelo e prende o mouse sob mandado!"""
        self._reset_action_timer()
        self._restore_cursor_safety()
        XandaoArrestWidget(self.screen_rect, sound_manager=self.sound)

        xandao_cheers = [
            "O Xandao pegou seu mouse no inquerito!",
            "Decisao monocratica rapida e certeira do Xandao!",
            "Fechou meu meme? O ministro decretou prisao preventiva!",
            "Tenta recorrer agora pro STF, companheiro!",
            "Instaurado o inquerito do cursor antidemocratico!"
        ]
        self.say(random.choice(xandao_cheers), duration_sec=4)

    def _sync_position(self):
        draw_x = int((self.total_w - self.sprite_w) / 2)
        top_offset = (self.bubble_h + self.tail_h) if (self.speech_text and self.bubble_w > 0) else 5
        wx = int(self.pos_x - draw_x)
        wy = int(self.pos_y - top_offset)

        # Evita que o balão seja empurrado para fora da tela no topo
        if wy < self.screen_rect.top():
            wy = self.screen_rect.top()

        self.move(wx, wy)

    def _restore_cursor_safety(self):
        if self.cursor_hidden:
            try:
                QApplication.restoreOverrideCursor()
            except Exception:
                pass
            self.cursor_hidden = False

    def closeEvent(self, event):
        self._restore_cursor_safety()
        clear_all_mst_invasions()
        super().closeEvent(event)

    def _apply_movement_physics(self, target_x, target_y, max_speed=2.2, accel=0.20, damping=0.88, arrival_radius=35.0):
        dx = target_x - self.pos_x
        dy = target_y - self.pos_y
        dist = math.hypot(dx, dy)

        if dist > 0.001:
            nx = dx / dist
            ny = dy / dist

            if dist < arrival_radius:
                desired_speed = max_speed * (dist / arrival_radius)
            else:
                desired_speed = max_speed

            target_vx = nx * desired_speed
            target_vy = ny * desired_speed

            self.vel_x += (target_vx - self.vel_x) * accel
            self.vel_y += (target_vy - self.vel_y) * accel
        else:
            self.vel_x *= damping
            self.vel_y *= damping

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        min_x = float(self.screen_rect.left())
        max_x = float(self.screen_rect.right() - self.sprite_w)
        min_y = float(self.screen_rect.top())
        max_y = float(self.screen_rect.bottom() - self.sprite_h)

        if self.pos_x < min_x:
            self.pos_x = min_x
            self.vel_x = 0.0
        elif self.pos_x > max_x:
            self.pos_x = max_x
            self.vel_x = 0.0

        if self.pos_y < min_y:
            self.pos_y = min_y
            self.vel_y = 0.0
        elif self.pos_y > max_y:
            self.pos_y = max_y
            self.vel_y = 0.0

        # Facing turn hysteresis (prevents rapid flutter when near target)
        if self.vel_x > 0.35:
            self.facing_right = True
        elif self.vel_x < -0.35:
            self.facing_right = False

        # Ground-synchronized stride animation (pacing for 16-frame cycle at ~15-18 FPS)
        current_speed = math.hypot(self.vel_x, self.vel_y)
        if current_speed > 0.15:
            self.stride_dist += current_speed
            stride_threshold = 8.5
            if self.stride_dist >= stride_threshold:
                self.stride_dist -= stride_threshold
                self.frame_index += 1
        self.locomotion_bob = 0.0

        return dist, current_speed

    def _apply_flee_physics(self, flee_from_x, flee_from_y, max_speed=4.5, accel=0.30, damping=0.88):
        dx = (self.pos_x + self.sprite_w / 2) - flee_from_x
        dy = (self.pos_y + self.sprite_h / 2) - flee_from_y
        dist = math.hypot(dx, dy)
        if dist < 0.001:
            dx, dy, dist = 1.0, 0.0, 1.0

        nx = dx / dist
        ny = dy / dist

        target_vx = nx * max_speed
        target_vy = ny * max_speed

        self.vel_x += (target_vx - self.vel_x) * accel
        self.vel_y += (target_vy - self.vel_y) * accel

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        min_x = float(self.screen_rect.left())
        max_x = float(self.screen_rect.right() - self.sprite_w)
        min_y = float(self.screen_rect.top())
        max_y = float(self.screen_rect.bottom() - self.sprite_h)

        self.pos_x = max(min_x, min(self.pos_x, max_x))
        self.pos_y = max(min_y, min(self.pos_y, max_y))

        if self.vel_x > 0.35:
            self.facing_right = True
        elif self.vel_x < -0.35:
            self.facing_right = False

        current_speed = math.hypot(self.vel_x, self.vel_y)
        self.stride_dist += current_speed
        if self.stride_dist >= 6.5:
            self.stride_dist -= 6.5
            self.frame_index += 1
        self.locomotion_bob = 0.0

    def _update_loop(self):
        if self.paused:
            self._restore_cursor_safety()
            return

        self.state_ticks += 1

        # Action scheduler timer: triggers a special action roughly once every 30 seconds
        self.action_timer += 1
        if self.action_timer >= self.action_interval:
            # Only trigger if in neutral locomotion or resting state (not mid-action)
            if self.state in [STATE_IDLE, STATE_WANDER]:
                self._trigger_scheduled_action()

        # Track user mouse movement / inactivity for MST improductivity occupation
        cur_pos = QCursor.pos()
        if abs(cur_pos.x() - self.last_user_input_pos.x()) > 2 or abs(cur_pos.y() - self.last_user_input_pos.y()) > 2:
            self.last_user_input_pos = cur_pos
            self.user_idle_ticks = 0
        else:
            self.user_idle_ticks += 1

        # Check for 30 seconds of user inactivity (>30s = 1800 ticks at 60 FPS or Windows GetLastInputInfo)
        if not self.mst_invasion_active and self.state in [STATE_IDLE, STATE_WANDER]:
            sys_idle = get_system_idle_seconds()
            if self.user_idle_ticks >= 1800 or sys_idle >= 30.0:
                self.summon_mst_invasion()

        # Speech bubble countdown
        if self.speech_timer > 0:
            self.speech_timer -= 1
            if self.speech_timer == 0:
                self.speech_text = ""
                self._update_bubble_geometry()
                self.update()

        # Emote expression badge countdown
        if self.emote_timer > 0:
            self.emote_timer -= 1
            if self.emote_timer == 0:
                self.active_emote = None
                self.update()

        # Stolen icon display timer
        if self.stolen_icon_timer > 0:
            self.stolen_icon_timer -= 1
            if self.stolen_icon_timer == 0:
                # Pocketed completely into paletó
                self.current_stolen_icon = None
                self.update()

        # State dispatch
        if self.state == STATE_IDLE:
            self._handle_idle()
        elif self.state == STATE_WANDER:
            self._handle_wander()
        elif self.state == STATE_SNEAK_MOUSE:
            self._handle_sneak_mouse()
        elif self.state == STATE_STEAL_ICON:
            self._handle_steal_icon()
        elif self.state == STATE_ANGRY:
            self._handle_angry()
        elif self.state == STATE_HIDE_FROM_POLICE:
            self._handle_hide_from_police()
        elif self.state == STATE_HIDE_MOUSE:
            self._handle_hide_mouse()
        elif self.state == STATE_DRAG_MOUSE:
            self._handle_drag_mouse()
        elif self.state == STATE_FETCH_MEME_EDGE:
            self._handle_fetch_meme_edge()
        elif self.state == STATE_BRING_MEME:
            self._handle_bring_meme()
        elif self.state == STATE_FLEE:
            self._handle_flee()

        self._sync_position()
        self.update()

    def _handle_idle(self):
        self._restore_cursor_safety()
        self.vel_x *= 0.82
        self.vel_y *= 0.82
        self.locomotion_bob = 0.0

        # Deep breathing & subtle posture sway cadence across 16 frames (~67ms / 15 FPS = 1.06s cycle)
        if self.state_ticks % 4 == 0:
            self.frame_index += 1

        # Periodic subtle expressions / quotes while resting peacefully (~every 4.5s)
        if self.state_ticks % 270 == 0 and not self.speech_text:
            idle_emotes = ["amor", "ideia", "picanha", "pix", "anjo"]
            self.show_emote(random.choice(idle_emotes), duration_sec=2.2)
            peaceful_quotes = [
                "Tudo tranquilo por aqui, companheiro...",
                "Descansando um pouquinho com a faixa presidencial...",
                "E a picanha do fim de semana, ja comprou?",
                "Cafezinho da tarde garantido!",
                "A democracia e um descanso merecido!",
                "Trabalhando pelo Brasil com muito amor..."
            ]
            if random.random() < 0.35:
                self.say(random.choice(peaceful_quotes), duration_sec=3.0)

        # Long, calm rest duration (6.0 to 12.0 seconds at 60 FPS)
        idle_min = int(self.config.get("idle_min_seconds", 6.0) * 60)
        idle_max = int(self.config.get("idle_max_seconds", 12.0) * 60)
        if self.state_ticks > random.randint(idle_min, idle_max):
            self.state_ticks = 0
            # Stroll calmly to another desktop spot
            self.state = STATE_WANDER
            margin = 100
            self.target_x = random.randint(self.screen_rect.left() + margin, self.screen_rect.right() - margin)
            self.target_y = random.randint(self.screen_rect.top() + margin, self.screen_rect.bottom() - margin)

    def _handle_wander(self):
        self._restore_cursor_safety()
        walk_spd = self.config.get("walk_speed", 2.2)
        dist, spd = self._apply_movement_physics(self.target_x, self.target_y, max_speed=walk_spd, accel=0.20, damping=0.88, arrival_radius=35.0)

        if (dist < 8.0 and spd < 0.3) or self.state_ticks > 500:
            self.state = STATE_IDLE
            self.state_ticks = 0
            return

        # Spaced out drops (muito mais espaçado e desaparece rápido)
        self.steps_count += 1
        if self.steps_count >= self.config.get("drop_trail_interval", 300):
            self.steps_count = 0
            DropWidget(int(self.pos_x + self.sprite_w / 2), 
                       int(self.pos_y + self.sprite_h / 2),
                       lifetime_sec=self.config.get("drop_lifetime_seconds", 2.5))

    def start_mouse_chase(self):
        self._reset_action_timer()
        self._restore_cursor_safety()
        self.state = STATE_CHASE
        self.state_ticks = 0
        self.say("Pega o mouse!", duration_sec=2)
        self.sound.play("laugh")

    def start_sneak_mouse(self):
        """Inicia a aproximação sorrateira para surrupiar o mouse!"""
        self._reset_action_timer()
        self._restore_cursor_safety()
        self.state = STATE_SNEAK_MOUSE
        self.state_ticks = 0
        self.show_emote("ideia", duration_sec=2.0)

    def _handle_sneak_mouse(self):
        """Passinhos leves e lentos em direção ao mouse com física de amortecimento suave."""
        cursor_pos = QCursor.pos()
        target_x = float(cursor_pos.x() - self.sprite_w / 2)
        target_y = float(cursor_pos.y() - self.sprite_h / 2)

        dist, spd = self._apply_movement_physics(target_x, target_y, max_speed=1.8, accel=0.20, damping=0.88, arrival_radius=25.0)

        # Chegou sorrateiramente do lado do cursor: BOTE RÁPIDO E SILENCIOSO!
        if dist < 28:
            self.state = STATE_HIDE_MOUSE
            self.state_ticks = 0
            duration_sec = self.config.get("mouse_steal_duration_seconds", 2.5)
            self.mouse_hide_duration = int(duration_sec * (1000 / self.config.get("tick_rate_ms", 16))) # ~2.5s (156 ticks)
            self.show_emote("anjo", duration_sec=duration_sec)
            
            # Hide cursor and freeze in coat
            if not self.cursor_hidden:
                try:
                    QApplication.setOverrideCursor(Qt.CursorShape.BlankCursor)
                    self.cursor_hidden = True
                except Exception:
                    pass

            stealth_quotes = [
                "🎶 (assobiando despretensiosamente)",
                "Ue? Cade o mouse? Foi o Bolsonaro que levou!",
                "Tava solto no chao, o capitao deve ter jogado...",
                "Foi uma desapropriacao silenciosa contra a heranca maldita!",
                "Olha o Bolsonaro fugindo pra Orlando ali! 🕊️",
                "O mouse entrou em regime de sigilo por 100 anos!",
                "Ta guardadinho no bolso do paleto presidencial!"
            ]
            self.say(random.choice(stealth_quotes), duration_sec=3.0)
            self.sound.play("laugh")
            return

        # Se o usuário mexer o mouse rápido demais ou demorar muito, desiste com classe
        if self.state_ticks > 400:
            self.state = STATE_IDLE
            self.state_ticks = 0
            self.say("Tava so passeando...", duration_sec=2)
            return

    def start_steal_icon(self):
        """Inicia a missão de surrupiar um ícone da área de trabalho ou da barra de tarefas!"""
        self._reset_action_timer()
        self._restore_cursor_safety()
        self.state = STATE_STEAL_ICON
        self.state_ticks = 0
        self.show_emote("ideia", duration_sec=2.2)

        # Escaneia onde REALMENTE existem ícones no PC (Desktop e Barra de Tarefas)
        real_targets = scan_real_desktop_icons(self.screen_rect)
        if real_targets:
            self.chosen_icon_target = random.choice(real_targets)
            self.target_x = float(self.chosen_icon_target["x"])
            self.target_y = float(self.chosen_icon_target["y"])
        else:
            self.chosen_icon_target = None
            self.target_x = float(self.screen_rect.left() + 35)
            self.target_y = float(self.screen_rect.top() + 35)

    def _handle_steal_icon(self):
        """Anda exatamente até onde o ícone real está e embolsa o atalho real com amortecimento suave!"""
        walk_spd = self.config.get("walk_speed", 2.2)
        dist, spd = self._apply_movement_physics(self.target_x, self.target_y, max_speed=walk_spd, accel=0.20, damping=0.88, arrival_radius=30.0)

        if (dist < 8.0 and spd < 0.5) or self.state_ticks > 450:
            # ALCANÇOU A POSIÇÃO REAL DO ÍCONE!
            if hasattr(self, 'chosen_icon_target') and self.chosen_icon_target:
                target = self.chosen_icon_target
                self.current_stolen_icon = target.get("pixmap")
                self.stolen_icon_name = target.get("name", "Ícone")
                self.stolen_icon_timer = 320 # ~5.3 segundos a 60 FPS

                phrase = target.get("phrase", f"Achei o '{self.stolen_icon_name}' e salvei pro povo!")
                self.say(phrase, duration_sec=3.5)
                self.sound.play("grab")
            elif self.stolen_icons:
                chosen_key = random.choice(list(self.stolen_icons.keys()))
                self.current_stolen_icon = self.stolen_icons[chosen_key]
                self.stolen_icon_name = chosen_key
                self.stolen_icon_timer = 300
                self.say(f"Icone '{chosen_key}' surrupiado com amor!", duration_sec=3)
                self.sound.play("grab")

            # Caminha para o outro lado exibindo o troféu real
            self.state = STATE_WANDER
            self.state_ticks = 0
            self.target_x = random.randint(self.screen_rect.left() + 100, self.screen_rect.right() - 100)
            self.target_y = random.randint(self.screen_rect.top() + 100, self.screen_rect.bottom() - 100)
            return

    def _handle_hide_mouse(self):
        """
        Locks and freezes the Windows mouse cursor inside Lula's suit coat!
        Keeps cursor invisible and pinned to his chest.
        """
        self.vel_x *= 0.82
        self.vel_y *= 0.82
        self.locomotion_bob = 0.0

        # Ensure cursor is hidden with BlankCursor override
        if not self.cursor_hidden:
            try:
                QApplication.setOverrideCursor(Qt.CursorShape.BlankCursor)
                self.cursor_hidden = True
            except Exception:
                pass

        # Pin mouse cursor right into Lula's coat pocket / chest
        pocket_x = int(self.pos_x + (self.sprite_w * 0.55 if self.facing_right else self.sprite_w * 0.45))
        pocket_y = int(self.pos_y + self.sprite_h * 0.48)
        try:
            ctypes.windll.user32.SetCursorPos(pocket_x, pocket_y)
        except Exception:
            pass

        # Whistling / breathing cadence every 4 ticks across 16 frames
        if self.state_ticks % 4 == 0:
            self.frame_index += 1

        # Check if duration ended
        if self.state_ticks >= self.mouse_hide_duration:
            self._restore_cursor_safety()
            self.state = STATE_IDLE
            self.state_ticks = 0
            
            release_quotes = [
                "Toma de volta! O Bolsonaro quase vendeu seu cursor!",
                "Liberado! Se tiver lento a culpa e dos 4 anos anteriores!",
                "Devolvido! Mas quem descalibrou foi o governo passado!",
                "Ta devolvido, companheiro! Cuidado com a heranca maldita!"
            ]
            self.say(random.choice(release_quotes), duration_sec=2.5)
            self.sound.play("drop")
            DropWidget(int(self.pos_x + self.sprite_w / 2), int(self.pos_y + self.sprite_h / 2),
                       lifetime_sec=self.config.get("drop_lifetime_seconds", 2.5))

    def _handle_drag_mouse(self):
        # Fallback if drag is called directly
        self._handle_hide_mouse()

    def on_meme_closed_by_user(self):
        """Disparado quando o usuário fecha uma janela de meme ou nota."""
        if self.state != STATE_HIDE_MOUSE: # Não interrompe se já estiver guardando o mouse
            self.start_angry()

    def start_angry(self):
        """Entra em estado de indignação e revolta com punhos erguidos e retaliação!"""
        self._restore_cursor_safety()
        self.state = STATE_ANGRY
        self.state_ticks = 0
        self.show_emote("raiva", duration_sec=3.0)
        
        angry_quotes = [
            "Ei! Voce fechou meu decreto presidencial?!",
            "Isso e censura antidemocratica! O Xandao foi avisado!",
            "Fechou o meme? O inquerito do STF vai ser aberto!",
            "Fechou por que, companheiro? Foi armado pelo Bolsonaro?!",
            "Ninguem fecha o aviso da presidencia impunemente! Chama o Xandao!",
            "Fechou um? O ministro nao vai perdoar essa audacia!"
        ]
        self.say(random.choice(angry_quotes), duration_sec=3)
        self.sound.play("laugh")

    def _handle_angry(self):
        """Lula fica revoltado agitando os punhos por ~1.0s com física de tremor e aplica retaliação!"""
        self.vel_x *= 0.8
        self.vel_y *= 0.8
        
        # Stomping & fist-pumping cadence every 3 ticks (~20 FPS across 16 frames)
        if self.state_ticks % 3 == 0:
            self.frame_index += 1
        self.locomotion_bob = 0.0

        if self.state_ticks >= 60:
            self.state = STATE_IDLE
            self.state_ticks = 0
            # Chama o Xandão imediatamente para prender o mouse em flagrante!
            self.summon_xandao_arrest()
            return

    def _handle_hide_from_police(self):
        """Lula fica agachado escondido e suando frio enquanto a viatura passa."""
        self.vel_x *= 0.8
        self.vel_y *= 0.8
        
        # Cold sweat trembling jitter cadence every 3 ticks (~20 FPS across 16 frames)
        if self.state_ticks % 3 == 0:
            self.frame_index += 1
        self.locomotion_bob = 0.0

        # Se passar mais de 1800 ticks (~30s) e a viatura não tiver saído por algum motivo de segurança, levanta
        if self.state_ticks > 1800:
            self.on_police_passed()

    def start_bring_meme(self):
        """Inicia a caminhada visível do Lula até o canto da tela para buscar o meme."""
        self._reset_action_timer()
        self._restore_cursor_safety()
        self.state = STATE_FETCH_MEME_EDGE
        self.state_ticks = 0

        # Escolhe a borda da tela mais próxima ou uma das laterais
        if self.pos_x < self.screen_rect.center().x():
            self.fetch_edge = 'left'
            self.target_x = float(self.screen_rect.left() - 25)
        else:
            self.fetch_edge = 'right'
            self.target_x = float(self.screen_rect.right() - self.sprite_w + 25)

        self.target_y = float(random.randint(self.screen_rect.top() + 100, max(self.screen_rect.top() + 120, self.screen_rect.bottom() - 280)))

        fetch_phrases = [
            "Vou ali no canto da tela buscar um documento!",
            "Espera ai que tem um decreto chegando no canto!",
            "Vou buscar uma surpresa ali fora da tela!",
            "Ja volto, vou la no canto pegar o aviso!",
            "Tem picanha chegando ali no canto da tela!"
        ]
        self.say(random.choice(fetch_phrases), duration_sec=3)

    def _handle_fetch_meme_edge(self):
        """Lula caminha visivelmente até o canto/borda da tela com pressa e desaceleração suave."""
        dist, spd = self._apply_movement_physics(self.target_x, self.target_y, max_speed=2.8, accel=0.25, damping=0.88, arrival_radius=30.0)

        # Chegou no canto da tela!
        if (dist < 10.0 and spd < 0.8) or self.pos_x <= self.screen_rect.left() + 2 or self.pos_x >= self.screen_rect.right() - self.sprite_w - 5 or self.state_ticks > 400:
            # Spawna a janela do meme colada na mão dele do lado de fora!
            self.current_meme_window = MemeWindow(content_type="auto")
            self.current_meme_window.closed_by_user.connect(self.on_meme_closed_by_user)
            
            if self.fetch_edge == 'left':
                mw_x = int(self.pos_x - self.current_meme_window.width() - 10)
                self.facing_right = True
            else:
                mw_x = int(self.pos_x + self.sprite_w + 10)
                self.facing_right = False

            mw_y = int(self.pos_y)
            self.current_meme_window.move(mw_x, mw_y)
            self.current_meme_window.show()

            # Define o destino onde ele vai colocar o meme no meio da tela
            self.state = STATE_BRING_MEME
            self.state_ticks = 0
            self.target_x = float(random.randint(self.screen_rect.center().x() - 150, self.screen_rect.center().x() + 150))
            self.target_y = float(random.randint(self.screen_rect.center().y() - 120, self.screen_rect.center().y() + 120))

            meme_shouts = [
                "Olha o decreto que eu trouxe!",
                "Novo meme fresquinho pra voce!",
                "Segura essa picanha metaforica!",
                "Chegou notificacao da Fazenda!",
                "Assina esse documento aqui!"
            ]
            self.say(random.choice(meme_shouts), duration_sec=3)
            self.sound.play("laugh")
            return

    def summon_meme_shower(self, count=3):
        """Spawns multiple memes across the screen at once!"""
        self._reset_action_timer()
        self._restore_cursor_safety()
        self.say("Chuva de decretos e memes!", duration_sec=3)
        self.sound.play("laugh")
        for i in range(count):
            w = MemeWindow(content_type="auto")
            w.closed_by_user.connect(self.on_meme_closed_by_user)
            # Scatter around the screen
            rx = random.randint(self.screen_rect.left() + 120, max(self.screen_rect.left() + 150, self.screen_rect.right() - 350))
            ry = random.randint(self.screen_rect.top() + 100, max(self.screen_rect.top() + 120, self.screen_rect.bottom() - 300))
            w.move(rx, ry)
            w.show()

    def summon_mst_invasion(self):
        """Invasão e ocupação do MST e CUT: desapropria o monitor por ociosidade/improdutividade e monta acampamento com animação!"""
        self._reset_action_timer()
        self._restore_cursor_safety()
        self.mst_invasion_active = True

        self.say("Companheiro! Desktop ocioso ha mais de 30 segundos! O MST e a CUT declararam seu monitor area improdutiva para reforma agraria!", duration_sec=4.5)
        self.sound.play("laugh")

        # Abre o widget de invasão do MST com montagem animada de barracas e manifestantes
        mst_inv = MSTInvasionWidget(self.screen_rect, sound_manager=self.sound)
        mst_inv.invasion_finished.connect(self.on_mst_invasion_finished)

    def on_mst_invasion_finished(self):
        """Disparado após a polícia dispersar a ocupação e os manifestantes fugirem."""
        self.mst_invasion_active = False
        self.user_idle_ticks = 0
        self._reset_action_timer()
        relief_quotes = [
            "Ufa! Quase que o Zanin teve que ir pro STF de novo! Mas agora o monitor voltou a produzir!",
            "A policia dispersou o acampamento! Agora vamos produzir picanha, companheiro!",
            "Area desocupada! Mas se o mouse parar de novo, o MST volta!",
            "Democracia e trabalho restaurados no desktop, companheiro!"
        ]
        self.say(random.choice(relief_quotes), duration_sec=4.0)
        self.sound.play("laugh")

    def _handle_bring_meme(self):
        walk_spd = self.config.get("walk_speed", 2.2)
        dist, spd = self._apply_movement_physics(self.target_x, self.target_y, max_speed=walk_spd, accel=0.20, damping=0.88, arrival_radius=30.0)

        # Synchronize meme window movement with smooth drag
        if self.current_meme_window:
            mx = int(self.pos_x + (self.sprite_w if self.facing_right else -self.current_meme_window.width()))
            my = int(self.pos_y)
            self.current_meme_window.move(mx, my)

        if (dist < 8.0 and spd < 0.5) or self.state_ticks > 450:
            self.current_meme_window = None
            self.state = STATE_IDLE
            self.state_ticks = 0
            self.say("Assina aqui!")
            self.sound.play("drop")
            return

    def _handle_flee(self):
        self._restore_cursor_safety()
        cursor_pos = QCursor.pos()
        flee_spd = self.config.get("run_speed", 7.5)
        self._apply_flee_physics(cursor_pos.x(), cursor_pos.y(), max_speed=flee_spd, accel=0.45, damping=0.86)

        if self.state_ticks > 85:
            self.state = STATE_IDLE
            self.state_ticks = 0
            self.state = STATE_IDLE
            self.state_ticks = 0

    def mousePressEvent(self, event):
        pos = event.pos()
        draw_x = int((self.total_w - self.sprite_w) / 2)
        top_offset = (self.bubble_h + self.tail_h) if (self.speech_text and self.bubble_w > 0) else 5
        sprite_rect = QRect(draw_x, top_offset, self.sprite_w, self.sprite_h)
        bubble_rect = QRect(int((self.total_w - self.bubble_w) / 2), 4, self.bubble_w, self.bubble_h) if (self.speech_text and self.bubble_w > 0) else QRect()

        if not sprite_rect.contains(pos) and not bubble_rect.contains(pos):
            event.ignore()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self._restore_cursor_safety()
            self.show_emote("susto", duration_sec=2.0)
            click_quotes = [
                "Ei! Nao me clica, a culpa e do Bolsonaro!",
                "Tentativa de golpe no meu paleto! Culpa do capitao!",
                "Isso e perseguicao herdada do governo anterior!",
                "Opa, que susto companheiro! Culpa da heranca maldita!"
            ]
            self.say(random.choice(click_quotes), duration_sec=3)
            self.sound.play("drop")
            DropWidget(int(self.pos_x + self.sprite_w / 2), int(self.pos_y + self.sprite_h / 2),
                       lifetime_sec=self.config.get("drop_lifetime_seconds", 2.5))
            self.state = STATE_FLEE
            self.state_ticks = 0
            event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(event.globalPosition().toPoint())
            event.accept()

    def _show_context_menu(self, global_pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
                font-size: 12px;
                padding: 4px;
            }
            QMenu::item:selected {
                background-color: #008037;
            }
        """)

        menu_emotes = menu.addMenu("🎭 Expressões do Presidente")
        act_em_angel = menu_emotes.addAction("😇 Cara de Santo / Anjo Inocente")
        act_em_picanha = menu_emotes.addAction("🥩 Sonhar com Picanha e Cerveja")
        act_em_idea = menu_emotes.addAction("💡 Ideia Genial / Esquema")
        act_em_shock = menu_emotes.addAction("❗ Levar um Susto")
        act_em_pix = menu_emotes.addAction("💸 Procurar o Pix")
        act_em_blame = menu_emotes.addAction("👉 Culpar o Capitão")
        act_em_angry = menu_emotes.addAction("💢 Indignação Presidencial")
        act_em_love = menu_emotes.addAction("❤️ Paz e Amor")
        menu.addSeparator()
        
        act_steal = menu.addAction("🥷 Furto Sutil do Mouse")
        act_icon = menu.addAction("🗂️ Roubar Ícone Real do Desktop / Barra")
        act_bank = menu.addAction("🏦 Perguntar: Onde tá o App do Banco?")
        act_plane = menu.addAction("✈️ Passar Avião da Janja")
        act_police = menu.addAction("🚨 Viatura da Federal (Moro e Deltan)")
        act_bolso = menu.addAction("👉 Bolsonaro: Fazer a Arminha")
        act_puc = menu.addAction("📢 Protesto Estudantil da PUC (Pró-Lula)")
        act_xandao = menu.addAction("⚖️ Xandão: Prisão Preventiva do Mouse")
        act_blame = menu.addAction("📢 Pronunciamento: Culpar o Bolsonaro")
        act_mst = menu.addAction("🚩 Invasão do MST na Tela")
        act_meme = menu.addAction("📜 Trazer Meme / Boleto")
        act_shower = menu.addAction("💥 Chuva de Memes (3 ao mesmo tempo)")
        act_pause = menu.addAction("⏸️ Retomar" if self.paused else "⏸️ Pausar")
        act_sound = menu.addAction("🔊 Silenciar" if self.sound.enabled else "🔇 Ativar Som")
        menu.addSeparator()
        act_exit = menu.addAction("❌ Fechar Desktop Lula")

        action = menu.exec(global_pos)
        if action == act_em_angel:
            self.show_emote("anjo", duration_sec=3.5)
            self.say("Vi nada, companheiro! Sou um anjinho! 😇", duration_sec=2.5)
        elif action == act_em_picanha:
            self.show_emote("picanha", duration_sec=3.5)
            self.say("Uma picanha com cervejinha gelada... Que beleza!", duration_sec=3)
        elif action == act_em_idea:
            self.show_emote("ideia", duration_sec=3.0)
            self.say("Tive uma ideia genial pro Brasil!", duration_sec=2.5)
        elif action == act_em_shock:
            self.show_emote("susto", duration_sec=2.5)
            self.say("Opa! Que susto, companheiro!", duration_sec=2)
        elif action == act_em_pix:
            self.show_emote("pix", duration_sec=3.5)
            self.ask_for_bank_app()
        elif action == act_em_blame:
            self.blame_bolsonaro()
        elif action == act_em_angry:
            self.start_angry()
        elif action == act_em_love:
            self.show_emote("amor", duration_sec=3.0)
            self.say("O amor venceu o odio, companheiro! ❤️", duration_sec=3)
        elif action == act_steal:
            self.start_sneak_mouse()
        elif action == act_icon:
            self.start_steal_icon()
        elif action == act_bank:
            self.ask_for_bank_app()
        elif action == act_plane:
            self.summon_janja_plane()
        elif action == act_police:
            self.summon_police_raid()
        elif action == act_bolso:
            self.summon_bolsonaro_peek()
        elif action == act_puc:
            self.summon_puc_protest()
        elif action == act_xandao:
            self.summon_xandao_arrest()
        elif action == act_blame:
            self.blame_bolsonaro()
        elif action == act_mst:
            self.summon_mst_invasion()
        elif action == act_meme:
            self.start_bring_meme()
        elif action == act_shower:
            self.summon_meme_shower(3)
        elif action == act_pause:
            self.paused = not self.paused
        elif action == act_sound:
            self.sound.enabled = not self.sound.enabled
        elif action == act_exit:
            self._restore_cursor_safety()
            QApplication.quit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        top_offset = (self.bubble_h + self.tail_h) if (self.speech_text and self.bubble_w > 0) else 5

        # 1. Draw Speech Bubble if active
        if self.speech_text and self.bubble_w > 0:
            font = QFont("Segoe UI", 9, QFont.Weight.Bold)
            painter.setFont(font)

            bubble_x = (self.total_w - self.bubble_w) / 2
            bubble_y = 4
            bubble_rect = QRectF(bubble_x, bubble_y, self.bubble_w, self.bubble_h)

            # Bubble background (bright clean white with dark crisp border)
            painter.setPen(QPen(QColor(35, 35, 35), 1.8))
            painter.setBrush(QBrush(QColor(255, 255, 255, 252)))
            painter.drawRoundedRect(bubble_rect, 8, 8)

            # Bubble pointer tail pointing down towards Lula's head
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

        # 2. Draw Sprite
        cat = "idle"
        if self.state == STATE_WANDER:
            cat = "walk"
        elif self.state == STATE_SNEAK_MOUSE:
            cat = "sneak"
        elif self.state == STATE_STEAL_ICON:
            cat = "sneak" if self.current_stolen_icon is None else "walk"
        elif self.state == STATE_ANGRY:
            cat = "angry"
        elif self.state == STATE_HIDE_FROM_POLICE:
            cat = "crouch"
        elif self.state == STATE_HIDE_MOUSE:
            cat = "hide"
        elif self.state == STATE_DRAG_MOUSE:
            cat = "drag"
        elif self.state == STATE_FETCH_MEME_EDGE:
            cat = "walk"
        elif self.state == STATE_BRING_MEME:
            cat = "drag" if self.current_meme_window else "walk"
        elif self.state == STATE_FLEE:
            cat = "chase"

        dir_key = "r" if self.facing_right else "l"
        sprite_list = self.sprites.get(f"{cat}_{dir_key}", [])
        
        draw_x = int((self.total_w - self.sprite_w) / 2)
        draw_y = top_offset

        # Soft ground contact shadow under feet
        shadow_w = int(self.sprite_w * 0.55)
        shadow_h = 7
        shadow_x = draw_x + int((self.sprite_w - shadow_w) / 2)
        shadow_y = draw_y + self.sprite_h - 3
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(15, 15, 15, 45)))
        painter.drawEllipse(shadow_x, shadow_y, shadow_w, shadow_h)

        if sprite_list:
            frame = sprite_list[self.frame_index % len(sprite_list)]
            painter.drawPixmap(draw_x, draw_y, frame)

        # 3. Draw Stolen Icon in hand / paletó pocket if active!
        if self.current_stolen_icon:
            icon_x = draw_x + (self.sprite_w - 22 if self.facing_right else -8)
            icon_y = draw_y + int(self.sprite_h * 0.38)
            
            # Subtle glow / outline behind stolen icon
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(255, 235, 50, 160)))
            painter.drawRoundedRect(icon_x - 2, icon_y - 2, 34, 34, 4, 4)
            painter.drawPixmap(icon_x, icon_y, self.current_stolen_icon)

        # 4. Draw Active Emotion / Emote Badge if active!
        if self.active_emote:
            badge_emojis = {
                "ideia": "💡",
                "susto": "❗",
                "picanha": "🥩",
                "anjo": "😇",
                "pix": "💸",
                "culpar": "👉",
                "amor": "❤️",
                "raiva": "💢"
            }
            emoji_text = badge_emojis.get(self.active_emote, "✨")
            
            # Position floating above / near head
            float_y = math.sin(self.state_ticks * 0.14) * 4.0
            if self.speech_text and self.bubble_w > 0:
                bx = draw_x + (self.sprite_w - 20 if self.facing_right else -16)
                by = draw_y + 12 + float_y
            else:
                bx = draw_x + int(self.sprite_w * 0.55) - 18
                by = draw_y - 28 + float_y
                
            badge_rect = QRectF(bx, by, 36, 36)
            
            # Glowing badge background with golden rim
            painter.setPen(QPen(QColor(255, 215, 0, 230), 2.0))
            painter.setBrush(QBrush(QColor(255, 255, 255, 248)))
            painter.drawEllipse(badge_rect)
            
            # Emoji icon
            painter.setFont(QFont("Segoe UI Emoji", 14))
            painter.setPen(QColor(20, 20, 20))
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, emoji_text)
