from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
import sys

class CompactBulletWidget(QWidget):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.state = 'unknown'
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)
        
        self.num_label = QLabel(f"{self.index + 1}")
        self.num_label.setFont(QFont('Consolas', 10, QFont.Weight.Bold))
        self.num_label.setFixedWidth(25)
        self.num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.num_label)
        
        self.status_label = QLabel("?")
        self.status_label.setFont(QFont('Consolas', 9, QFont.Weight.Bold))
        self.status_label.setFixedWidth(50)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.btn_hot = QPushButton("H")
        self.btn_hot.setFixedSize(30, 24)
        self.btn_hot.setFont(QFont('Consolas', 9, QFont.Weight.Bold))
        self.btn_hot.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_hot)
        
        self.btn_cold = QPushButton("C")
        self.btn_cold.setFixedSize(30, 24)
        self.btn_cold.setFont(QFont('Consolas', 9, QFont.Weight.Bold))
        self.btn_cold.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_cold)
        
        self.update_style()
        
    def set_state(self, state):
        self.state = state
        self.update_style()
        
    def update_style(self):
        if self.state == 'hot':
            widget_bg = "rgba(255, 60, 60, 0.15)"
            border = "#ff3c3c"
            num_color = "#ff3c3c"
            status_bg = "#ff3c3c"
            status_text = "HOT"
        elif self.state == 'cold':
            widget_bg = "rgba(60, 160, 255, 0.15)"
            border = "#3ca0ff"
            num_color = "#3ca0ff"
            status_bg = "#3ca0ff"
            status_text = "CLD"
        else:
            widget_bg = "rgba(100, 100, 100, 0.1)"
            border = "rgba(150, 150, 150, 0.3)"
            num_color = "#888888"
            status_bg = "rgba(100, 100, 100, 0.3)"
            status_text = "?"
        
        self.setStyleSheet(f"""
            QWidget {{
                background: {widget_bg};
                border: 1px solid {border};
                border-radius: 6px;
            }}
        """)
        
        self.num_label.setStyleSheet(f"color: {num_color}; background: transparent; border: none;")
        self.status_label.setStyleSheet(f"""
            color: #000000;
            background: {status_bg};
            border: none;
            border-radius: 4px;
            padding: 2px;
        """)
        self.status_label.setText(status_text)
        
        self.btn_hot.setStyleSheet("""
            QPushButton {
                background: rgba(255, 60, 60, 0.7);
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 60, 60, 1);
            }
            QPushButton:pressed {
                background: rgba(200, 40, 40, 1);
            }
        """)
        
        self.btn_cold.setStyleSheet("""
            QPushButton {
                background: rgba(60, 160, 255, 0.7);
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(60, 160, 255, 1);
            }
            QPushButton:pressed {
                background: rgba(40, 120, 200, 1);
            }
        """)


class RouletteResolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Roulette Resolver')
        
        screen = QApplication.primaryScreen().geometry()
        window_width = 220
        window_height = 520
        pos_x = screen.width() - window_width - 10
        pos_y = 10
        
        self.setGeometry(pos_x, pos_y, window_width, window_height)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.hot_rounds = 0
        self.cold_rounds = 0
        self.bullet_states = []
        self.bullet_widgets = []
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(8)
        
        header = QHBoxLayout()
        header.setSpacing(8)
        
        title = QLabel("ROULETTE")
        title.setFont(QFont('Consolas', 11, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff; background: transparent;")
        header.addWidget(title)
        
        header.addStretch()
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)
        close_btn.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 60, 60, 0.7);
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 60, 60, 1);
            }
        """)
        header.addWidget(close_btn)
        
        container_layout.addLayout(header)
        
        self.entry_hot = QLineEdit()
        self.entry_hot.setPlaceholderText("HOT")
        self.entry_hot.setFont(QFont('Consolas', 9))
        self.entry_hot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entry_hot.setFixedHeight(28)
        container_layout.addWidget(self.entry_hot)
        
        self.entry_cold = QLineEdit()
        self.entry_cold.setPlaceholderText("COLD")
        self.entry_cold.setFont(QFont('Consolas', 9))
        self.entry_cold.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entry_cold.setFixedHeight(28)
        container_layout.addWidget(self.entry_cold)
        
        self.init_button = QPushButton("FILL")
        self.init_button.setFont(QFont('Consolas', 9, QFont.Weight.Bold))
        self.init_button.setFixedHeight(32)
        self.init_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.init_button.clicked.connect(self.fill_rounds)
        container_layout.addWidget(self.init_button)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)
        
        self.hot_button = QPushButton("REM H")
        self.hot_button.setFont(QFont('Consolas', 8, QFont.Weight.Bold))
        self.hot_button.setFixedHeight(28)
        self.hot_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hot_button.clicked.connect(self.remove_hot)
        btn_layout.addWidget(self.hot_button)
        
        self.cold_button = QPushButton("REM C")
        self.cold_button.setFont(QFont('Consolas', 8, QFont.Weight.Bold))
        self.cold_button.setFixedHeight(28)
        self.cold_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cold_button.clicked.connect(self.remove_cold)
        btn_layout.addWidget(self.cold_button)
        
        container_layout.addLayout(btn_layout)
        
        self.stats = QFrame()
        stats_layout = QVBoxLayout(self.stats)
        stats_layout.setContentsMargins(8, 6, 8, 6)
        stats_layout.setSpacing(3)
        
        self.label_hot = QLabel("H: 0")
        self.label_hot.setFont(QFont('Consolas', 9, QFont.Weight.Bold))
        self.label_hot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.label_hot)
        
        self.label_cold = QLabel("C: 0")
        self.label_cold.setFont(QFont('Consolas', 9, QFont.Weight.Bold))
        self.label_cold.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.label_cold)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet("background: rgba(255, 255, 255, 0.2);")
        stats_layout.addWidget(line)
        
        self.label_chance = QLabel("0%")
        self.label_chance.setFont(QFont('Consolas', 14, QFont.Weight.Bold))
        self.label_chance.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.label_chance)
        
        container_layout.addWidget(self.stats)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.bullets_container = QWidget()
        self.bullets_layout = QVBoxLayout(self.bullets_container)
        self.bullets_layout.setSpacing(4)
        self.bullets_layout.setContentsMargins(2, 2, 2, 2)
        self.bullets_layout.addStretch()
        
        scroll.setWidget(self.bullets_container)
        container_layout.addWidget(scroll, 1)
        
        main_layout.addWidget(container)
        
        self.apply_styles(container)
    
    def apply_styles(self, container):
        container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(25, 25, 35, 0.95),
                    stop:1 rgba(35, 25, 45, 0.95));
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)
        
        self.entry_hot.setStyleSheet("""
            QLineEdit {
                background: rgba(0, 0, 0, 0.3);
                color: #ffffff;
                border: 1px solid rgba(255, 100, 100, 0.4);
                border-radius: 6px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 100, 100, 0.8);
                background: rgba(0, 0, 0, 0.4);
            }
        """)
        
        self.entry_cold.setStyleSheet("""
            QLineEdit {
                background: rgba(0, 0, 0, 0.3);
                color: #ffffff;
                border: 1px solid rgba(100, 180, 255, 0.4);
                border-radius: 6px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(100, 180, 255, 0.8);
                background: rgba(0, 0, 0, 0.4);
            }
        """)
        
        self.init_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 200, 100, 0.7),
                    stop:1 rgba(100, 255, 150, 0.7));
                color: #000000;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 200, 100, 0.9),
                    stop:1 rgba(100, 255, 150, 0.9));
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(80, 160, 80, 1),
                    stop:1 rgba(80, 200, 120, 1));
            }
        """)
        
        self.hot_button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 60, 60, 0.6);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 60, 60, 0.8);
            }
            QPushButton:pressed {
                background: rgba(200, 40, 40, 1);
            }
        """)
        
        self.cold_button.setStyleSheet("""
            QPushButton {
                background: rgba(60, 160, 255, 0.6);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(60, 160, 255, 0.8);
            }
            QPushButton:pressed {
                background: rgba(40, 120, 200, 1);
            }
        """)
        
        self.stats.setStyleSheet("""
            QFrame {
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            QLabel {
                color: #ffffff;
                background: transparent;
            }
        """)
        
        self.findChild(QScrollArea).setStyleSheet("""
            QScrollArea {
                background: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.2);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.5);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.bullets_container.setStyleSheet("background: transparent;")
    
    def fill_rounds(self):
        try:
            self.hot_rounds = int(self.entry_hot.text())
            self.cold_rounds = int(self.entry_cold.text())
            
            if self.hot_rounds < 0 or self.cold_rounds < 0:
                raise ValueError
            
            self.bullet_states = ['unknown'] * (self.hot_rounds + self.cold_rounds)
            self.update_display()
        except ValueError:
            self.label_chance.setText("ERR")
            self.label_chance.setStyleSheet("color: #ff3c3c; background: transparent;")
    
    def remove_hot(self):
        if self.hot_rounds > 0 and self.bullet_states:
            self.hot_rounds -= 1
            self.bullet_states.pop(0)
            self.update_display()
    
    def remove_cold(self):
        if self.cold_rounds > 0 and self.bullet_states:
            self.cold_rounds -= 1
            self.bullet_states.pop(0)
            self.update_display()
    
    def update_display(self):
        marked_hot = sum(1 for s in self.bullet_states if s == 'hot')
        marked_cold = sum(1 for s in self.bullet_states if s == 'cold')
        unknown = sum(1 for s in self.bullet_states if s == 'unknown')
        
        total = len(self.bullet_states)
        
        if total > 0:
            remaining_hot = max(0, self.hot_rounds - marked_hot)
            remaining_cold = max(0, self.cold_rounds - marked_cold)
            
            if unknown > 0 and (remaining_hot + remaining_cold) > 0:
                chance = (remaining_hot / (remaining_hot + remaining_cold)) * 100
            elif total > 0:
                chance = (marked_hot / total) * 100
            else:
                chance = 0
        else:
            chance = 0
        
        self.label_hot.setText(f"H: {marked_hot}/{self.hot_rounds}")
        self.label_hot.setStyleSheet("color: #ff6666; background: transparent;")
        
        self.label_cold.setText(f"C: {marked_cold}/{self.cold_rounds}")
        self.label_cold.setStyleSheet("color: #66b3ff; background: transparent;")
        
        self.label_chance.setText(f"{chance:.0f}%")
        
        if chance >= 70:
            color = "#ff3c3c"
        elif chance >= 40:
            color = "#ffaa44"
        else:
            color = "#66ff88"
        
        self.label_chance.setStyleSheet(f"color: {color}; background: transparent;")
        
        self.update_bullets()
    
    def update_bullets(self):
        for widget in self.bullet_widgets:
            widget.deleteLater()
        self.bullet_widgets.clear()
        
        for idx, state in enumerate(self.bullet_states):
            widget = CompactBulletWidget(idx)
            widget.set_state(state)
            widget.btn_hot.clicked.connect(lambda checked, i=idx: self.set_hot(i))
            widget.btn_cold.clicked.connect(lambda checked, i=idx: self.set_cold(i))
            
            self.bullets_layout.insertWidget(len(self.bullet_widgets), widget)
            self.bullet_widgets.append(widget)
    
    def set_hot(self, idx):
        if idx < len(self.bullet_states):
            self.bullet_states[idx] = 'hot'
            self.update_display()
    
    def set_cold(self, idx):
        if idx < len(self.bullet_states):
            self.bullet_states[idx] = 'cold'
            self.update_display()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(25, 25, 35))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = RouletteResolver()
    window.show()
    sys.exit(app.exec())
