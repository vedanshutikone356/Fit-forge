def generate_workout_plan(training_days: int, experience: str, equipment: str, fitness_goal: str) -> dict:
    """
    Generates a structured weekly workout plan based on user equipment, 
    available days, experience level, and primary fitness goal.
    """
    eq = equipment.lower()
    exp = experience.lower()
    goal = fitness_goal.lower()
    
    # Adjust reps/rest based on goal & experience
    if "strength" in goal:
        default_reps = "5-6"
        default_rest = "2-3 min"
    elif "muscle" in goal or "bulk" in goal:
        default_reps = "8-12"
        default_rest = "60-90 sec"
    else: # Weight Loss, Endurance, General Fitness
        default_reps = "12-15"
        default_rest = "45-60 sec"

    sets = "3" if exp == "beginner" else "4"

    # Select Routine Split
    if "bodyweight" in eq or "home" in eq:
        split_type = "Home Bodyweight & Functional Split"
        weekly_schedule = {
            "Monday": {
                "focus": "Upper Body Push & Core",
                "exercises": [
                    {"name": "Standard/Incline Push-Ups", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Chest/Triceps"},
                    {"name": "Pike Push-Ups", "sets": sets, "reps": "8-10", "rest": default_rest, "target": "Shoulders"},
                    {"name": "Chair / Bench Dips", "sets": sets, "reps": "10-12", "rest": default_rest, "target": "Triceps"},
                    {"name": "Plank Hold", "sets": "3", "reps": "45-60 sec", "rest": "60 sec", "target": "Core"}
                ]
            },
            "Wednesday": {
                "focus": "Lower Body & Legs",
                "exercises": [
                    {"name": "Bodyweight Squats", "sets": sets, "reps": "15-20", "rest": default_rest, "target": "Quads/Glutes"},
                    {"name": "Walking Lunges", "sets": sets, "reps": "12 per leg", "rest": default_rest, "target": "Quads/Hamstrings"},
                    {"name": "Glute Bridges", "sets": sets, "reps": "15-20", "rest": default_rest, "target": "Glutes/Lower Back"},
                    {"name": "Single-Leg Calf Raises", "sets": "3", "reps": "20", "rest": "45 sec", "target": "Calves"}
                ]
            },
            "Friday": {
                "focus": "Full Body Conditioning",
                "exercises": [
                    {"name": "Burpees", "sets": "3", "reps": "10-12", "rest": "60 sec", "target": "Full Body/Cardio"},
                    {"name": "Mountain Climbers", "sets": "3", "reps": "30 sec", "rest": "45 sec", "target": "Core/Cardio"},
                    {"name": "Doorway / Towel Rows", "sets": sets, "reps": "12-15", "rest": default_rest, "target": "Back/Biceps"},
                    {"name": "Superman Hold", "sets": "3", "reps": "12-15", "rest": "45 sec", "target": "Lower Back"}
                ]
            }
        }
    elif training_days >= 5:
        split_type = "Push / Pull / Legs (PPL) Split"
        weekly_schedule = {
            "Monday": {
                "focus": "Push (Chest, Shoulders, Triceps)",
                "exercises": [
                    {"name": "Barbell / Dumbbell Bench Press", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Chest"},
                    {"name": "Incline Dumbbell Press", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Upper Chest"},
                    {"name": "Overhead Shoulder Press", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Shoulders"},
                    {"name": "Dumbbell Lateral Raises", "sets": "4", "reps": "12-15", "rest": "45 sec", "target": "Side Delts"},
                    {"name": "Triceps Cable Pushdowns", "sets": sets, "reps": "10-12", "rest": "60 sec", "target": "Triceps"}
                ]
            },
            "Tuesday": {
                "focus": "Pull (Back, Biceps, Rear Delts)",
                "exercises": [
                    {"name": "Lat Pulldown / Pull-ups", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Upper Back/Lats"},
                    {"name": "Bent-Over Barbell/DB Row", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Mid Back"},
                    {"name": "Face Pulls", "sets": "4", "reps": "15", "rest": "45 sec", "target": "Rear Delts"},
                    {"name": "Bicep Barbell Curls", "sets": sets, "reps": "10-12", "rest": "60 sec", "target": "Biceps"},
                    {"name": "Hammer Curls", "sets": "3", "reps": "12", "rest": "60 sec", "target": "Brachialis"}
                ]
            },
            "Wednesday": {
                "focus": "Legs & Abs",
                "exercises": [
                    {"name": "Barbell Squats / Leg Press", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Quads"},
                    {"name": "Romanian Deadlifts", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Hamstrings"},
                    {"name": "Leg Extension Machine", "sets": "3", "reps": "12-15", "rest": "60 sec", "target": "Quads"},
                    {"name": "Standing Calf Raises", "sets": "4", "reps": "15", "rest": "45 sec", "target": "Calves"},
                    {"name": "Hanging Knee Raises", "sets": "3", "reps": "15", "rest": "45 sec", "target": "Abs"}
                ]
            },
            "Thursday": {
                "focus": "Upper Body Focus",
                "exercises": [
                    {"name": "Dumbbell Incline Flyes", "sets": sets, "reps": "12", "rest": default_rest, "target": "Chest"},
                    {"name": "Seated Cable Rows", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Back"},
                    {"name": "Arnold Press", "sets": sets, "reps": "10-12", "rest": default_rest, "target": "Shoulders"},
                    {"name": "Preacher Curls", "sets": "3", "reps": "12", "rest": "60 sec", "target": "Biceps"},
                    {"name": "Skullcrushers", "sets": "3", "reps": "10-12", "rest": "60 sec", "target": "Triceps"}
                ]
            },
            "Friday": {
                "focus": "Lower Body & Core Focus",
                "exercises": [
                    {"name": "Goblet Squats", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Quads"},
                    {"name": "Lying Hamstring Curls", "sets": sets, "reps": "12-15", "rest": default_rest, "target": "Hamstrings"},
                    {"name": "Bulgarian Split Squats", "sets": "3", "reps": "10 per leg", "rest": "60 sec", "target": "Glutes/Quads"},
                    {"name": "Ab Crunch Machine / Cable Crunch", "sets": "3", "reps": "15", "rest": "45 sec", "target": "Abs"}
                ]
            }
        }
    else:
        split_type = "Full Body / 3-Day Compound Split"
        weekly_schedule = {
            "Monday": {
                "focus": "Full Body A",
                "exercises": [
                    {"name": "Barbell / DB Squats", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Quads/Glutes"},
                    {"name": "Flat Bench Press", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Chest"},
                    {"name": "Bent-Over DB Rows", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Back"},
                    {"name": "Overhead DB Press", "sets": "3", "reps": "10-12", "rest": "60 sec", "target": "Shoulders"},
                    {"name": "Plank", "sets": "3", "reps": "60 sec", "rest": "45 sec", "target": "Core"}
                ]
            },
            "Wednesday": {
                "focus": "Full Body B",
                "exercises": [
                    {"name": "Conventional Deadlifts", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Posterior Chain"},
                    {"name": "Incline DB Press", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Upper Chest"},
                    {"name": "Lat Pulldowns", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Lats/Back"},
                    {"name": "Dumbbell Lateral Raises", "sets": "3", "reps": "12-15", "rest": "45 sec", "target": "Shoulders"},
                    {"name": "Bicep Curls / Triceps Extensions Superset", "sets": "3", "reps": "12", "rest": "60 sec", "target": "Arms"}
                ]
            },
            "Friday": {
                "focus": "Full Body C",
                "exercises": [
                    {"name": "Leg Press / Goblet Squats", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Legs"},
                    {"name": "Dumbbell Shoulder Press", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Shoulders"},
                    {"name": "Seated Cable Rows", "sets": sets, "reps": default_reps, "rest": default_rest, "target": "Back"},
                    {"name": "Dips or Push-Ups", "sets": "3", "reps": "12-15", "rest": "60 sec", "target": "Chest/Triceps"},
                    {"name": "Hanging Leg Raises", "sets": "3", "reps": "12-15", "rest": "45 sec", "target": "Abs"}
                ]
            }
        }

    return {
        "split_name": split_type,
        "experience_level": experience,
        "equipment": equipment,
        "schedule": weekly_schedule
    }

if __name__ == "__main__":
    plan = generate_workout_plan(training_days=4, experience="Intermediate", equipment="Full Gym", fitness_goal="Muscle Gain")
    print(f"Generated Split: {plan['split_name']}")
    for day, data in plan['schedule'].items():
        print(f"\n[{day}] {data['focus']}")
        for ex in data['exercises']:
            print(f" - {ex['name']}: {ex['sets']} sets x {ex['reps']} reps (Rest: {ex['rest']})")