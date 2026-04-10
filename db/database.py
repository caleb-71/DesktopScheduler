import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="scheduler.db"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, db_name)
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        # ✨ [핵심] date 컬럼 추가 (예: '2026-04-10')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,  
                title TEXT NOT NULL,
                time TEXT NOT NULL,
                category TEXT
            )
        ''')
        conn.commit()
        conn.close()

    # 일정을 추가할 때 날짜(date_str)도 같이 받습니다.
    def add_schedule(self, date_str, title, time_str, category="Work"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (date, title, time, category)
            VALUES (?, ?, ?, ?)
        ''', (date_str, title, time_str, category))
        conn.commit()
        conn.close()

    # 특정 연/월의 일정만 쏙 뽑아옵니다.
    def get_month_schedules(self, year, month):
        conn = self.get_connection()
        cursor = conn.cursor()
        # LIKE 명령어: '2026-04-' 로 시작하는 모든 데이터를 찾아라!
        month_str = f"{year}-{month:02d}-%"
        cursor.execute('SELECT date, title, time FROM events WHERE date LIKE ?', (month_str,))
        rows = cursor.fetchall()
        conn.close()
        return rows