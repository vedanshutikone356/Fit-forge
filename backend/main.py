from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
import os

# Import local backend modules
try:
    from database import get_db_connection, init_db
    from calculations import generate_full_metrics
    from workout_generator import generate_workout_plan
    from nutrition import generate_meal_plan
    from tracker import log_daily_activity, generate_weekly_progress_chart, get_user_activity_history
except ImportError:
    from backend.database import get_db_connection, init_db
    from backend.calculations import generate_full_metrics
    from backend.workout_generator import generate_workout_plan
    from backend.nutrition import generate_meal_plan
    from backend.tracker import log_daily_activity, generate_weekly_progress_chart, get_user_activity_history

# Initialize Database on Startup
init_db()

app = FastAPI(
    title="FitForge API",
    description="AI-Powered Personal Fitness & Lifestyle Planner Backend",
    version="1.0.0"
)

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Frontend Static Directory
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# --- Pydantic Request Models ---

class UserProfileSchema(BaseModel):
    name: str = Field(..., example="Alex")
    age: int = Field(..., example=22)
    gender: str = Field(..., example="Male")
    height: float = Field(..., example=175.0)
    weight: float = Field(..., example=70.0)
    body_type: str = Field(..., example="Average")
    experience: str = Field(..., example="Intermediate")
    training_days: int = Field(..., example=4)
    fitness_goal: str = Field(..., example="Muscle Gain")
    target_weight: float = Field(..., example=75.0)
    timeline_weeks: int = Field(..., example=12)
    avg_steps: int = Field(default=8000, example=8000)
    avg_sleep: float = Field(default=7.5, example=7.5)
    stress_level: int = Field(default=5, example=5)
    work_hours: float = Field(default=8.0, example=8.0)
    workout_time: str = Field(default="Evening", example="Evening")
    diet_preference: str = Field(..., example="Vegetarian")
    food_allergies: Optional[str] = Field(default="", example="None")
    equipment: str = Field(..., example="Full Gym")


class ActivityLogSchema(BaseModel):
    user_id: int
    date: Optional[str] = None
    weight: Optional[float] = None
    steps: Optional[int] = None
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None
    water_liters: Optional[float] = None
    stress_level: Optional[int] = None
    workout_completed: Optional[int] = None


class ProductivityGoalSchema(BaseModel):
    user_id: int
    title: str
    completed: int = 0
    date: Optional[str] = None


# --- Static Frontend File Server ---

@app.get("/")
def read_root():
    """Serves the Landing Page."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to FitForge API. Visit /docs for API documentation."}


@app.get("/dashboard")
def read_dashboard():
    """Serves the main Dashboard Page."""
    dashboard_path = os.path.join(FRONTEND_DIR, "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# --- REST API Endpoints ---

@app.post("/api/user", summary="Create User Profile & Generate Initial Fitness Plan")
def create_user_profile(user: UserProfileSchema):
    """
    Receives user onboarding parameters, calculates all health metrics,
    stores profile in SQLite database, and returns generated targets.
    """
    user_dict = user.model_dump()
    metrics = generate_full_metrics(user_dict)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (
            name, age, gender, height, weight, body_type, experience, training_days,
            fitness_goal, target_weight, timeline_weeks, avg_steps, avg_sleep,
            stress_level, work_hours, workout_time, diet_preference, food_allergies,
            equipment, bmi, bmr, tdee, target_calories, target_protein, target_carbs,
            target_fat, target_water
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user.name, user.age, user.gender, user.height, user.weight, user.body_type,
        user.experience, user.training_days, user.fitness_goal, user.target_weight,
        user.timeline_weeks, user.avg_steps, user.avg_sleep, user.stress_level,
        user.work_hours, user.workout_time, user.diet_preference, user.food_allergies,
        user.equipment, metrics['bmi'], metrics['bmr'], metrics['tdee'],
        metrics['target_calories'], metrics['target_protein'], metrics['target_carbs'],
        metrics['target_fat'], metrics['target_water']
    ))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "status": "success",
        "user_id": user_id,
        "name": user.name,
        "metrics": metrics
    }


@app.get("/api/user/{user_id}", summary="Get User Profile & Current Metrics")
def get_user_profile(user_id: int):
    """Fetches user details and calculated targets by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = dict(user)
    # Recalculate full metrics including stress tips
    metrics = generate_full_metrics(user_dict)
    user_dict["metrics"] = metrics
    return user_dict


@app.get("/api/workout/{user_id}", summary="Get Personalized Workout Plan")
def get_workout_plan(user_id: int):
    """Generates and returns personalized weekly workout split."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT training_days, experience, equipment, fitness_goal FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        # Default fallback
        return generate_workout_plan(4, "Intermediate", "Full Gym", "Muscle Gain")

    return generate_workout_plan(
        training_days=user['training_days'],
        experience=user['experience'],
        equipment=user['equipment'],
        fitness_goal=user['fitness_goal']
    )


@app.get("/api/nutrition/{user_id}", summary="Get Personalized Pandas Meal Plan")
def get_nutrition_plan(user_id: int):
    """Generates daily meal plan matching user's calorie/protein targets using Pandas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT target_calories, target_protein, diet_preference FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    cals = user['target_calories'] if user else 2000.0
    prot = user['target_protein'] if user else 120.0
    diet = user['diet_preference'] if user else "Vegetarian"

    return generate_meal_plan(target_calories=cals, target_protein=prot, diet_preference=diet)


@app.post("/api/track", summary="Log Daily Activity & Health Metrics")
def log_activity(log: ActivityLogSchema):
    """Logs or updates steps, sleep, water, stress, weight, and workout status."""
    today_str = log.date if log.date else datetime.date.today().isoformat()
    result = log_daily_activity(
        user_id=log.user_id,
        date_str=today_str,
        weight=log.weight,
        steps=log.steps,
        sleep_hours=log.sleep_hours,
        sleep_quality=log.sleep_quality,
        water_liters=log.water_liters,
        stress_level=log.stress_level,
        workout_completed=log.workout_completed
    )
    return result


@app.get("/api/progress/{user_id}", summary="Get Progress History & Matplotlib Chart")
def get_progress(user_id: int):
    """Returns activity log history and base64 encoded Matplotlib weekly chart."""
    history_df = get_user_activity_history(user_id)
    chart_base64 = generate_weekly_progress_chart(user_id)

    return {
        "user_id": user_id,
        "history": history_df.to_dict(orient="records"),
        "chart_base64": chart_base64
    }


@app.post("/api/goals", summary="Add Productivity Goal")
def add_productivity_goal(goal: ProductivityGoalSchema):
    """Adds a new daily task/goal to the productivity checklist."""
    today_str = goal.date if goal.date else datetime.date.today().isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productivity_goals (user_id, title, completed, date)
        VALUES (?, ?, ?, ?)
    ''', (goal.user_id, goal.title, goal.completed, today_str))
    goal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"status": "success", "goal_id": goal_id}


@app.get("/api/goals/{user_id}", summary="Get Daily Productivity Goals")
def get_productivity_goals(user_id: int):
    """Fetches all productivity goals for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productivity_goals WHERE user_id = ? ORDER BY id DESC", (user_id,))
    goals = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"user_id": user_id, "goals": goals}


@app.put("/api/goals/{goal_id}", summary="Toggle Goal Completion")
def update_productivity_goal(goal_id: int, completed: int = Body(..., embed=True)):
    """Marks a goal as completed or incomplete."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productivity_goals SET completed = ? WHERE id = ?", (completed, goal_id))
    conn.commit()
    conn.close()
    return {"status": "success", "goal_id": goal_id, "completed": completed}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
@app.get("/api/grocery-list")
def get_grocery_list(user_id: int = 1):
    # Fetch meal plan for user from SQLite / calculation engine
    meal_plan = fetch_user_weekly_meals(user_id)  # Helper retrieving 7-day meal dict
    
    if not meal_plan:
        raise HTTPException(status_code=404, detail="No active meal plan found.")
        
    grocery_data = generate_weekly_grocery_list(meal_plan)
    return {"status": "success", "grocery_list": grocery_data}
from backend.nutrition import generate_weekly_grocery_list

@app.get("/api/grocery-list")
def get_grocery_list(user_id: int = 1):
    try:
        # Get the active meal plan (or pass your meal plan generator function)
        meal_plan = fetch_user_weekly_meals(user_id)  
        if not meal_plan:
            return {"status": "success", "grocery_list": []}
            
        grocery_data = generate_weekly_grocery_list(meal_plan)
        return {"status": "success", "grocery_list": grocery_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
from backend.nutrition import generate_weekly_grocery_list

@app.get("/api/grocery-list")
def get_grocery_list(user_id: int = 1):
    try:
        # Fetch meal plan safely
        meal_plan = fetch_user_weekly_meals(user_id)  # or your helper function
        
        if not meal_plan:
            return {"status": "success", "grocery_list": []}
            
        grocery_data = generate_weekly_grocery_list(meal_plan)
        return {"status": "success", "grocery_list": grocery_data}
    except Exception as e:
        # Return empty list on error instead of throwing a 500 crash
        return {"status": "success", "grocery_list": []}