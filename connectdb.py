import sqlite3

db = sqlite3.connect('pc_data.db')
cursor = db.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS pc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT,
        model TEXT,
        year TEXT,
        price TEXT
    )
''')
db.commit() 