import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "fitforge.db")

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn

def init_db():
    """Creates the necessary database tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # User Profile & Plan Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            height REAL NOT NULL,
            weight REAL NOT NULL,
            body_type TEXT NOT NULL,
            experience TEXT NOT NULL,
            training_days INTEGER NOT NULL,
            fitness_goal TEXT NOT NULL,
            target_weight REAL NOT NULL,
            timeline_weeks INTEGER NOT NULL,
            avg_steps INTEGER NOT NULL,
            avg_sleep REAL NOT NULL,
            stress_level INTEGER NOT NULL,
            work_hours REAL NOT NULL,
            workout_time TEXT NOT NULL,
            diet_preference TEXT NOT NULL,
            food_allergies TEXT,
            equipment TEXT NOT NULL,
            bmi REAL,
            bmr REAL,
            tdee REAL,
            target_calories REAL,
            target_protein REAL,
            target_carbs REAL,
            target_fat REAL,
            target_water REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Daily Tracking Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            weight REAL,
            steps INTEGER DEFAULT 0,
            sleep_hours REAL DEFAULT 0,
            sleep_quality INTEGER DEFAULT 0,
            water_liters REAL DEFAULT 0,
            stress_level INTEGER DEFAULT 0,
            workout_completed INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Productivity Goals Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productivity_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully at fitforge.db")

if __name__ == "__main__":
    init_db()