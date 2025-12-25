import sqlite3
from datetime import datetime

def init_db():
    # Базаға қосылу (егер файл болмаса, ол өзі жасалады)
    conn = sqlite3.connect('warden_storage.db')
    cursor = conn.cursor()
    
    # Тексеріс тарихын сақтайтын кесте жасау
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            file_hash TEXT,
            scan_date TEXT,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_scan_result(filename, file_hash, status):
    conn = sqlite3.connect('warden_storage.db')
    cursor = conn.cursor()
    
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO scan_logs (filename, file_hash, scan_date, status)
        VALUES (?, ?, ?, ?)
    ''', (filename, file_hash, date_now, status))
    
    conn.commit()
    conn.close()
    print(f"Нәтиже базаға сақталды: {filename}")