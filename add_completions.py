import sqlite3

db = sqlite3.connect("database.db")
db.execute("DROP TABLE IF EXISTS completions")
db.execute("""
    CREATE TABLE completions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        quest_id INTEGER REFERENCES sidequests(id),
        completed_at TEXT NOT NULL,
        UNIQUE(user_id, quest_id)
    )
""")
db.commit()
db.close()
print("Completions table created!")