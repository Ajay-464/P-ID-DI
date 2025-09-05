import sqlite3
import os

DB_FILE = os.path.join("data", "pid_database.db")

def setup_database():
    """Creates the database and the equipment table if they don't exist."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_image TEXT NOT NULL,
            tag TEXT,
            type TEXT,
            iso_class TEXT,
            iso_subclass TEXT,
            description TEXT,
            connections TEXT,
            status TEXT DEFAULT 'pending_review'
        )
    """)
    conn.commit()
    conn.close()
    print("Database setup complete.")

def save_to_db(data, image_name):
    """Saves the extracted equipment data to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    equipment_list = data.get("equipment", [])
    for item in equipment_list:
        cursor.execute("""
            INSERT INTO equipment (source_image, tag, type, iso_class, iso_subclass, description, connections)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            image_name, 
            item.get('tag'), 
            item.get('type'), 
            item.get('iso_class'), 
            item.get('iso_subclass'),
            item.get('description'), 
            item.get('connections')
        ))
    
    conn.commit()
    conn.close()
    print(f"Saved {len(equipment_list)} items to the database.")