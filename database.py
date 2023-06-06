import sqlite3

class DatabaseHandler:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER
            )
        ''')
        self.conn.commit()

    def insert_score(self, score):
        self.cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
        self.conn.commit()

    def get_top_scores(self, limit=3):
        self.cursor.execute("SELECT score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
