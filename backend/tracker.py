import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server generation
import matplotlib.pyplot as plt
import os
import io
import base64
try:
    from database import get_db_connection
except ImportError:
    from backend.database import get_db_connection

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "generated_charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

def log_daily_activity(user_id: int, date_str: str, weight: float = None, steps: int = None, 
                       sleep_hours: float = None, sleep_quality: int = None, 
                       water_liters: float = None, stress_level: int = None, 
                       workout_completed: int = None) -> dict:
    """
    Inserts or updates daily log entry for a specific user and date.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if entry already exists for this user and date
    cursor.execute("SELECT id FROM daily_logs WHERE user_id = ? AND date = ?", (user_id, date_str))
    existing = cursor.fetchone()

    if existing:
        log_id = existing['id']
        updates = []
        params = []
        if weight is not None:
            updates.append("weight = ?")
            params.append(weight)
        if steps is not None:
            updates.append("steps = ?")
            params.append(steps)
        if sleep_hours is not None:
            updates.append("sleep_hours = ?")
            params.append(sleep_hours)
        if sleep_quality is not None:
            updates.append("sleep_quality = ?")
            params.append(sleep_quality)
        if water_liters is not None:
            updates.append("water_liters = ?")
            params.append(water_liters)
        if stress_level is not None:
            updates.append("stress_level = ?")
            params.append(stress_level)
        if workout_completed is not None:
            updates.append("workout_completed = ?")
            params.append(workout_completed)

        if updates:
            query = f"UPDATE daily_logs SET {', '.join(updates)} WHERE id = ?"
            params.append(log_id)
            cursor.execute(query, params)
    else:
        cursor.execute('''
            INSERT INTO daily_logs (user_id, date, weight, steps, sleep_hours, sleep_quality, water_liters, stress_level, workout_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date_str, weight, steps or 0, sleep_hours or 0.0, sleep_quality or 0, water_liters or 0.0, stress_level or 0, workout_completed or 0))

    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Activity logged for user {user_id} on {date_str}"}

def get_user_activity_history(user_id: int) -> pd.DataFrame:
    """
    Fetches all daily activity logs for a user into a Pandas DataFrame.
    """
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM daily_logs WHERE user_id = ? ORDER BY date ASC", conn, params=(user_id,))
    conn.close()
    return df

def generate_weekly_progress_chart(user_id: int) -> str:
    """
    Generates a dark-themed Matplotlib progress chart showing Steps & Sleep over time.
    Returns the image as a base64 encoded string for easy web display.
    """
    df = get_user_activity_history(user_id)

    # If no logs exist, generate sample dummy data using numpy for initial rendering
    if df.empty or len(df) < 2:
        dates = pd.date_range(end=pd.Timestamp.today(), periods=7).strftime('%Y-%m-%d').tolist()
        steps = np.random.randint(6000, 11000, size=7)
        sleep = np.round(np.random.uniform(6.5, 8.5, size=7), 1)
        df = pd.DataFrame({"date": dates, "steps": steps, "sleep_hours": sleep})

    # Apply Dark Fitness Theme Styling to Matplotlib
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(8, 4), facecolor='#0d0d0d')
    ax1.set_facecolor('#141414')

    # Color definitions matching dark UI
    accent_green = '#10B981'
    accent_cyan = '#06B6D4'

    # Bar chart for Steps
    bars = ax1.bar(df['date'], df['steps'], color=accent_green, alpha=0.7, width=0.4, label='Steps')
    ax1.set_ylabel('Daily Steps', color=accent_green, fontsize=10, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=accent_green)
    ax1.tick_params(axis='x', rotation=30, labelsize=8)

    # Line chart overlay for Sleep Hours
    ax2 = ax1.twinx()
    ax2.plot(df['date'], df['sleep_hours'], color=accent_cyan, linewidth=2.5, marker='o', label='Sleep (hrs)')
    ax2.set_ylabel('Sleep Hours', color=accent_cyan, fontsize=10, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=accent_cyan)

    plt.title('7-Day Activity & Sleep Overview', color='white', fontsize=12, pad=12, fontweight='bold')
    fig.tight_layout()

    # Save chart to a base64 string buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

if __name__ == "__main__":
    print("--- Testing Tracker & Chart Generator ---")
    # Log sample activity
    log_daily_activity(user_id=1, date_str="2026-10-01", steps=8500, sleep_hours=7.5, water_liters=2.5, stress_level=4)
    log_daily_activity(user_id=1, date_str="2026-10-02", steps=10200, sleep_hours=8.0, water_liters=3.0, stress_level=3)
    
    chart_base64 = generate_weekly_progress_chart(user_id=1)
    print(f"Chart generated successfully! Base64 length: {len(chart_base64)} characters.")