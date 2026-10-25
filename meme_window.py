"""
Floating meme and note windows dragged onto the screen by Desktop Lula.
Styled like retro desktop utility windows with draggable header and close button.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QCursor
import random
import os

ACTIVE_MEMES = []

def clear_all_memes():
    global ACTIVE_MEMES
    for m in list(ACTIVE_MEMES):
        m.close()
    ACTIVE_MEMES.clear()

class MemeWindow(QWidget):
    # Signal emitted when the user closes the window
    closed_by_user = pyqtSignal()

    def __init__(self, content_type="auto"):
        """
        content_type: 'image', 'note', or 'auto'
        """
        super().__init__()
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        
        self.drag_position = None
        self.being_dragged_by_pet = False

        self._setup_ui(content_type)
        ACTIVE_MEMES.append(self)

    def _setup_ui(self, content_type):
        self.setStyleSheet("""
            QWidget#MainContainer {
                background-color: #ECE9D8;
                border: 2px solid #0A246A;
                border-radius: 4px;
            }
            QWidget#TitleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0A246A, stop:1 #A6CAF0);
                border-top-left-radius: 2px;
                border-top-right-radius: 2px;
            }
            QLabel#TitleLabel {
                color: white;
                font-weight: bold;
                font-size: 11px;
                padding-left: 4px;
            }
            QPushButton#CloseBtn {
                background-color: #D63939;
                color: white;
                font-weight: bold;
                border: 1px solid #700;
                border-radius: 2px;
                width: 16px;
                height: 14px;
                font-size: 10px;
                margin-right: 2px;
            }
            QPushButton#CloseBtn:hover {
                background-color: #FF5555;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        container = QWidget()
        container.setObjectName("MainContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(3, 3, 3, 3)
        container_layout.setSpacing(4)

        # Title Bar
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar.setFixedHeight(22)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(4, 0, 2, 0)

        titles = [
            "Lula Desktop - Mensagem Oficial",
            "Ministério da Zoeira - Notificação",
            "Fundo Soberano da Picanha",
            "Receita Federal do Humor",
            "Aviso Sindical de Trabalho"
        ]
        self.title_label = QLabel(random.choice(titles))
        self.title_label.setObjectName("TitleLabel")
        
        close_btn = QPushButton("✕")
        close_btn.setObjectName("CloseBtn")
        close_btn.clicked.connect(self.close_window)

        tb_layout.addWidget(self.title_label)
        tb_layout.addStretch()
        tb_layout.addWidget(close_btn)

        container_layout.addWidget(title_bar)

        # Content (Image or Note)
        memes_dir = "assets/memes"
        notes_dir = "assets/notes"

        is_image = False
        if content_type == 'image':
            is_image = True
        elif content_type == 'note':
            is_image = False
        else:
            # Auto choose
            is_image = random.random() > 0.4

        if is_image and os.path.exists(memes_dir):
            images = [os.path.join(memes_dir, f) for f in os.listdir(memes_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if images:
                chosen = random.choice(images)
                pix = QPixmap(chosen)
                if pix.width() > 320:
                    pix = pix.scaledToWidth(320, Qt.TransformationMode.SmoothTransformation)
                img_label = QLabel()
                img_label.setPixmap(pix)
                img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                container_layout.addWidget(img_label)
            else:
                is_image = False

        if not is_image:
            # Load note
            notes = []
            if os.path.exists(notes_dir):
                notes = [os.path.join(notes_dir, f) for f in os.listdir(notes_dir) if f.endswith('.txt')]

            content_text = "Companheiro, seu computador foi contemplado com o Programa Mais Memes!"
            if notes:
                chosen_note = random.choice(notes)
                try:
                    with open(chosen_note, 'r', encoding='utf-8') as f:
                        content_text = f.read()
                except Exception:
                    pass

            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setPlainText(content_text)
            text_edit.setStyleSheet("background: #FFFDE8; border: 1px solid #CCC; font-family: 'Segoe UI', sans-serif; font-size: 12px; color: #111;")
            text_edit.setFixedSize(280, 140)
            container_layout.addWidget(text_edit)

        layout.addWidget(container)
        self.adjustSize()

    def close_window(self):
        try:
            self.closed_by_user.emit()
        except Exception:
            pass
        if self in ACTIVE_MEMES:
            ACTIVE_MEMES.remove(self)
        self.close()

    # User dragging window by clicking
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None
