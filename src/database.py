import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("game_data.db")
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS high_scores (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               username TEXT NOT NULL,
                               score INTEGER NOT NULL)''')
        self.conn.commit()

    def save_score(self, username, score):
        self.cursor.execute("SELECT * FROM high_scores ORDER BY score DESC LIMIT 1")
        result = self.cursor.fetchone()

        if result is None or score > result[2]:
            self.cursor.execute("INSERT INTO high_scores (username, score) VALUES (?, ?)", (username, score))
            self.conn.commit()

    def get_high_score(self):
        self.cursor.execute("SELECT username, score FROM high_scores ORDER BY score DESC LIMIT 1")
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()













    """
    def __init__(self, db_name="highscores.db"):
        '''Initialize the database connection and create the table if it doesn't exist.'''
        self.db_name = db_name
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self._create_table()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            self.conn = None
            self.cursor = None

    def _create_table(self):
        '''Create the highscores table if it doesn't exist'''
        if self.cursor:
            try:
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS highscores (
                        username TEXT NOT NULL,
                        score INTEGER NOT NULL
                    )
                ''')
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error creating table: {e}")

    def save_highscore(self, username, score):
        '''Save the high score for a given username.'''
        if not self.cursor:
            print("Database not initialized properly.")
            return
        try:
            self.cursor.execute("SELECT MAX(score) FROM highscores WHERE username=?", (username,))
            result = self.cursor.fetchone()
            max_score = result[0] if result[0] else 0
            if score > max_score:
                self.cursor.execute("INSERT INTO highscores (username, score) VALUES (?, ?)", (username, score))
                self.conn.commit()
                print(f"High score for {username} saved: {score}")
            else:
                print(f"Current score {score} is not higher than the previous high score.")
        except sqlite3.Error as e:
            print(f"Error saving high score: {e}")

    def get_max_score_for_user(self, username):
        '''Get the highest score for a given username.'''
        if not self.cursor:
            print("Database not initialized properly.")
            return 0
        try:
            self.cursor.execute("SELECT MAX(score) FROM highscores WHERE username=?", (username,))
            result = self.cursor.fetchone()
            return result[0] if result[0] else 0
        except sqlite3.Error as e:
            print(f"Error retrieving max score for {username}: {e}")
            return 0

    def get_all_highscores(self):
        '''Get top 10 high scores from the database'''
        if not self.cursor:
            print("Database not initialized properly.")
            return []
        try:
            self.cursor.execute("SELECT username, MAX(score) FROM highscores GROUP BY username ORDER BY score DESC LIMIT 10")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving all high scores: {e}")
            return []

    def close(self):
        '''Closes the database connection'''
        if self.conn:
            try:
                self.conn.commit() 
                self.conn.close()
                print("Database connection closed.")
            except sqlite3.Error as e:
                print(f"Error closing the database connection: {e}")
"""