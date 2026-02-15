import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE
)
""")

# PROGRESS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    language TEXT,
    level INTEGER
)
""")

# BADGES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    badge_name TEXT
)
""")

# CERTIFICATES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    language TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully")
