import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import TransparentScheduler
from core.manager import ScheduleManager


def main():
    app = QApplication(sys.argv)

    # 1. UI 인스턴스 생성
    ui = TransparentScheduler()

    # 2. 비즈니스 로직 매니저 생성 및 UI 의존성 주입
    manager = ScheduleManager(ui)

    # 3. 매니저에게 일정 로드 지시
    manager.load_month_schedules()

    # 4. 화면 출력
    ui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()