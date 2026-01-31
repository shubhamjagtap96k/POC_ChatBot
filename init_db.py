import sqlite3
import os

DB_FILE = "backend/chatbot.db"
SCHEMA_FILE = "backend/schema.sql"
SEED_FILE = "backend/seed.sql"

def init_db():
    # Remove existing DB to start fresh
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed existing database: {DB_FILE}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    with open(SCHEMA_FILE, 'r') as f:
        schema_script = f.read()
    
    print("Executing schema...")
    cursor.executescript(schema_script)

    with open(SEED_FILE, 'r') as f:
        seed_script = f.read()
    
    print("Executing seed data...")
    cursor.executescript(seed_script)

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {DB_FILE}")

if __name__ == "__main__":
    init_db()
