import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("feedbacks.db")
cur = conn.cursor()

# Create the feedback table
cur.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    lang TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ feedbacks.db created successfully.")
