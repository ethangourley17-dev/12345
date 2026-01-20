import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "roofing_jobs.db"

def init_db():
    """Initialize the SQLite database with the jobs table."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            address TEXT,
            value REAL,
            status TEXT,
            created_at TIMESTAMP,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

class JobManager:
    def __init__(self):
        init_db()

    def add_job(self, customer_name, address, value, status="Lead", notes=""):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        created_at = datetime.now()
        c.execute('''
            INSERT INTO jobs (customer_name, address, value, status, created_at, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_name, address, value, status, created_at, notes))
        conn.commit()
        conn.close()

    def get_jobs(self):
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM jobs", conn)
        conn.close()
        return df

    def update_job_status(self, job_id, new_status):
        # Ensure job_id is a native Python type (int), not numpy.int64
        if hasattr(job_id, 'item'):
            job_id = job_id.item()
            
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("UPDATE jobs SET status = ? WHERE id = ?", (new_status, job_id))
        conn.commit()
        conn.close()

    def delete_job(self, job_id):
        # Ensure job_id is a native Python type (int), not numpy.int64
        if hasattr(job_id, 'item'):
            job_id = job_id.item()

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        conn.close()
