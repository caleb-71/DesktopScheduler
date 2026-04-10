from db.database import DatabaseManager


class ScheduleManager:
    def __init__(self, ui_view):
        self.ui = ui_view
        self.db = DatabaseManager()

        # ✨ [핵심 1] 화면(UI)에서 '더블클릭' 무전이 오면, open_input_dialog 함수를 실행하라고 연결!
        self.ui.dateDoubleClicked.connect(self.open_input_dialog)

    # UI에 일정을 뿌려주는 함수
    def load_month_schedules(self):
        # 1. 화면에 있는 예전 일정을 깨끗이 지웁니다.
        self.ui.clear_schedules()

        year = self.ui.current_year
        month = self.ui.current_month

        # 2. DB에서 이번 달 일정을 모두 가져옵니다.
        real_data = self.db.get_month_schedules(year, month)

        for item in real_data:
            date_str = item[0]  # 예: '2026-04-10'
            title = item[1]  # 예: '회의'
            time_str = item[2]  # 예: '10:00 AM'

            # '2026-04-10' 에서 맨 뒤의 '10'만 잘라내서 숫자로 만듭니다.
            day = int(date_str.split('-')[2])
            display_text = f"[{time_str}] {title}"

            # 3. UI의 해당 날짜 칸에 일정을 넣습니다.
            self.ui.add_schedule_item(day, display_text)

        self.ui.finalize_layout()

    # ✨ [핵심 2] 팝업창을 띄우고 일정을 저장하는 함수
    def open_input_dialog(self, day):
        year = self.ui.current_year
        month = self.ui.current_month

        # 1. 위에서 만든 팝업창(ScheduleInputDialog)을 화면에 띄웁니다.
        from ui.main_window import ScheduleInputDialog
        dialog = ScheduleInputDialog(year, month, day, self.ui)

        # 2. 사용자가 '확인(Ok)'을 눌렀다면?
        if dialog.exec():
            title, time_str = dialog.get_data()

            if title:  # 제목이 비어있지 않은지 확인
                # DB에 넣기 위해 날짜를 'YYYY-MM-DD' 형태로 예쁘게 만듭니다.
                date_str = f"{year}-{month:02d}-{day:02d}"

                # 3. DB에 일정을 저장합니다!
                self.db.add_schedule(date_str, title, time_str)

                # 4. 저장했으니 화면을 새로고침하여 방금 쓴 일정을 띄웁니다.
                self.load_month_schedules()