import calendar
from datetime import datetime, date
import holidays
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QSizePolicy, QSizeGrip,
                             QDialog, QLineEdit, QFormLayout, QDialogButtonBox,
                             QSlider)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal


class DateFrame(QFrame):
    doubleClicked = pyqtSignal(int)

    def __init__(self, day):
        super().__init__()
        self.day = day

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.doubleClicked.emit(self.day)


class ScheduleInputDialog(QDialog):
    def __init__(self, year, month, day, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"일정 추가")
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        layout = QFormLayout()
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("예: 10:00 AM")
        self.time_input.setStyleSheet("background-color: #3b3b3b; padding: 5px; border-radius: 3px;")

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("일정 내용을 입력하세요")
        self.title_input.setStyleSheet("background-color: #3b3b3b; padding: 5px; border-radius: 3px;")

        layout.addRow("시간:", self.time_input)
        layout.addRow("내용:", self.title_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.setStyleSheet("QPushButton { background-color: #555; padding: 5px 15px; border-radius: 3px; }")

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_data(self):
        return self.title_input.text(), self.time_input.text()


class TransparentScheduler(QWidget):
    dateDoubleClicked = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.oldPos = self.pos()
        self.layout = QVBoxLayout()
        self.day_layouts = {}
        self.schedule_widgets = []

        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month

        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setWindowOpacity(0.85)
        self.setStyleSheet("background-color: #2b2b2b; border-radius: 15px;")
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(10, 5, 5, 10)
        title_text = f"{self.current_year}년 {self.current_month}월 일정"
        title_label = QLabel(title_text, self)
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; background: transparent;")
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()

        btn_style = """
            QPushButton { background-color: transparent; color: white; font-size: 14px; font-weight: bold; border-radius: 5px; padding: 5px 10px; border: none; }
            QPushButton:hover { background-color: #555555; }
        """
        min_btn = QPushButton("─", self)
        min_btn.setStyleSheet(btn_style)
        min_btn.clicked.connect(self.showMinimized)
        title_bar_layout.addWidget(min_btn)

        self.max_btn = QPushButton("□", self)
        self.max_btn.setStyleSheet(btn_style)
        self.max_btn.clicked.connect(self.toggle_maximize)
        title_bar_layout.addWidget(self.max_btn)

        close_btn = QPushButton("✕", self)
        close_btn.setStyleSheet(btn_style.replace("#555555", "#d9534f"))
        close_btn.clicked.connect(self.close)
        title_bar_layout.addWidget(close_btn)

        self.layout.addLayout(title_bar_layout)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(6)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days):
            day_label = QLabel(day)
            if col == 5:
                day_label.setStyleSheet("color: #6699ff; font-weight: bold; background: transparent;")
            elif col == 6:
                day_label.setStyleSheet("color: #ff6666; font-weight: bold; background: transparent;")
            else:
                day_label.setStyleSheet("color: #aaaaaa; font-weight: bold; background: transparent;")
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid_layout.addWidget(day_label, 0, col)

        cal = calendar.monthcalendar(self.current_year, self.current_month)
        today = datetime.now()
        kr_holidays = holidays.KR(years=self.current_year)

        weekday_colors = ["#FFF9C4", "#FFF59D", "#FFF176", "#FFEE58", "#FFEB3B"]

        for row, week in enumerate(cal):
            for col, day in enumerate(week):
                if day != 0:
                    cell_frame = DateFrame(day)
                    cell_frame.doubleClicked.connect(self.dateDoubleClicked.emit)

                    current_date = date(self.current_year, self.current_month, day)

                    if current_date in kr_holidays or col == 6:
                        bg_style = "background-color: #ff6b6b;"
                        text_color = "white"
                    elif col == 5:
                        bg_style = "background-color: #5c9aff;"
                        text_color = "white"
                    else:
                        bg_style = f"background-color: {weekday_colors[col]};"
                        text_color = "#333333"

                    border_3d = """
                        border-top: 2px solid rgba(255, 255, 255, 0.6); 
                        border-left: 2px solid rgba(255, 255, 255, 0.6); 
                        border-bottom: 2px solid rgba(0, 0, 0, 0.4); 
                        border-right: 2px solid rgba(0, 0, 0, 0.4); 
                        border-radius: 5px;
                    """

                    cell_frame.setStyleSheet(f"{bg_style} {border_3d}")
                    cell_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

                    cell_layout = QVBoxLayout()
                    cell_layout.setContentsMargins(5, 5, 5, 5)

                    date_label = QLabel(str(day))

                    # ✨ [변경점] 숫자를 더 크고 진하게 만듭니다.
                    if day == today.day and self.current_month == today.month:
                        highlight_color = "#d32f2f" if text_color == "#333333" else "#FFD700"
                        # 오늘 날짜: 18px 로 가장 크게
                        date_label.setStyleSheet(
                            f"color: {highlight_color}; font-weight: bold; font-size: 18px; background: transparent; border: none;")
                    else:
                        # 일반 날짜: 14px -> 16px 로 키우고, font-weight: bold 추가
                        date_label.setStyleSheet(
                            f"color: {text_color}; font-weight: bold; font-size: 16px; background: transparent; border: none;")

                    date_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
                    cell_layout.addWidget(date_label)

                    self.day_layouts[day] = cell_layout
                    cell_layout.addStretch()
                    cell_frame.setLayout(cell_layout)
                    grid_layout.addWidget(cell_frame, row + 1, col)

        self.layout.addLayout(grid_layout)

    def add_schedule_item(self, day, text):
        if day in self.day_layouts:
            schedule_label = QLabel(text)
            schedule_label.setStyleSheet(
                "color: #F0F0F0; font-size: 11px; background-color: #444444; border-radius: 3px; padding: 2px 4px; margin-top: 2px; border: none;")
            schedule_label.setWordWrap(True)

            layout = self.day_layouts[day]
            layout.insertWidget(layout.count() - 1, schedule_label)
            self.schedule_widgets.append(schedule_label)

    def clear_schedules(self):
        for widget in self.schedule_widgets:
            widget.deleteLater()
        self.schedule_widgets.clear()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.max_btn.setText("□")
        else:
            self.showMaximized()
            self.max_btn.setText("❐")

    def change_opacity(self, value):
        self.setWindowOpacity(value / 100.0)

    def finalize_layout(self):
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(10, 5, 0, 0)

        opacity_label = QLabel("투명도:")
        opacity_label.setStyleSheet("color: #aaaaaa; font-size: 12px; font-weight: bold; background: transparent;")
        bottom_layout.addWidget(opacity_label)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(20, 100)
        self.opacity_slider.setValue(85)
        self.opacity_slider.setFixedWidth(100)

        self.opacity_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #555555; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: #FFD700; width: 12px; margin: -4px 0; border-radius: 6px; }
        """)

        self.opacity_slider.valueChanged.connect(self.change_opacity)
        bottom_layout.addWidget(self.opacity_slider)

        bottom_layout.addStretch()

        size_grip = QSizeGrip(self)
        bottom_layout.addWidget(size_grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.layout.addLayout(bottom_layout)
        self.resize(800, 600)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.oldPos.isNull() and not self.isMaximized():
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = QPoint()