# data/database.py
import sqlite3
from datetime import datetime

DB_FILE = "wifi_history.db"

def init_db():
    """데이터베이스와 테이블을 생성합니다."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ssid TEXT NOT NULL,
                bssid TEXT NOT NULL,
                score INTEGER NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                checked_at DATETIME NOT NULL
            )
        """)
        conn.commit()

def add_record(ssid, bssid, score, lat, lon):
    """점검 결과를 데이터베이스에 추가합니다."""
    timestamp = datetime.now()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (ssid, bssid, score, latitude, longitude, checked_at) VALUES (?, ?, ?, ?, ?, ?)",
            (ssid, bssid, score, lat, lon, timestamp)
        )
        conn.commit()

def get_all_records():
    """모든 점검 이력을 조회합니다."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row  # 컬럼명으로 접근 가능하도록 설정
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY checked_at DESC")
        records = cursor.fetchall()
        return [dict(row) for row in records]
