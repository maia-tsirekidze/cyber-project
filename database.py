import sqlite3
import json
DB_NAME = "scanner.db"
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              url TEXT,
              ip TEXT,
              report_time TEXT,
              headers TEXT,
              warnings TEXT
        )''')
    conn.commit()
    conn.close()
    

def save_report(report):
    conn = sqlite3.connect(DB_NAME)
    c= conn.cursor()
    c.execute('INSERT INTO reports (url,ip, report_time,headers,warnings) VALUES (?,?,?,?,?)',(
        report.get('url'),
        report.get('ip'),
        report.get('report_time'),
        json.dumps(report.get('headers')),
        json.dumps(report.get("warnings"))
    ))
    conn.commit()
    conn.close()