import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('warden_storage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            file_hash TEXT,
            scan_date TEXT,
            status TEXT,
            risk_score INTEGER,
            threat_details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_scan_result(filename, file_hash, status, risk_score=0, threat_details=""):
    conn = sqlite3.connect('warden_storage.db')
    cursor = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO scan_logs (filename, file_hash, scan_date, status, risk_score, threat_details)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (filename, file_hash, date_now, status, risk_score, threat_details))
    conn.commit()
    conn.close()