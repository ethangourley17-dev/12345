import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_FILE = "roofing_jobs.db"

def init_db():
    """Initialize the SQLite database with the jobs table."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            address TEXT,
            value REAL,
            status TEXT,
            created_at TIMESTAMP,
            notes TEXT,
            lead_source TEXT
        )
    ''')

    # Migration check: Check if 'lead_source' column exists
    c.execute("PRAGMA table_info(jobs)")
    columns = [info[1] for info in c.fetchall()]
    if 'lead_source' not in columns:
        print("Migrating DB: Adding lead_source column...")
        c.execute("ALTER TABLE jobs ADD COLUMN lead_source TEXT")

    conn.commit()
    conn.close()

class JobManager:
    def __init__(self):
        init_db()

    def add_job(self, customer_name, address, value, status="Lead", notes="", lead_source="Website"):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        created_at = datetime.now()
        c.execute('''
            INSERT INTO jobs (customer_name, address, value, status, created_at, notes, lead_source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (customer_name, address, value, status, created_at, notes, lead_source))
        conn.commit()
        conn.close()

    def get_jobs(self):
        conn = sqlite3.connect(DB_FILE)
        try:
            df = pd.read_sql_query("SELECT * FROM jobs", conn)
        except Exception:
            df = pd.DataFrame()
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
