import numpy as np

def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    """
    Calculates Body Mass Index (BMI) and returns the value along with category.
    Formula: BMI = weight (kg) / (height (m))^2
    """
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal Weight"
    elif 25.0 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
        
    return {"bmi": bmi, "category": category}

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculates Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation.
    Men:   BMR = 10 * weight + 6.25 * height - 5 * age + 5
    Women: BMR = 10 * weight + 6.25 * height - 5 * age - 161
    """
    gender_lower = gender.lower()
    if gender_lower in ["male", "m"]:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    return round(bmr, 2)

def calculate_tdee(bmr: float, training_days: int, avg_steps: int) -> float:
    """
    Estimates Total Daily Energy Expenditure (TDEE) based on exercise days and average daily steps.
    Uses numpy array lookup for activity multiplier.
    """
    # Activity multipliers: 1.2 (Sedentary), 1.375 (Light), 1.55 (Moderate), 1.725 (Very Active), 1.9 (Extra Active)
    multipliers = np.array([1.2, 1.375, 1.55, 1.725, 1.9])
    
    if training_days <= 1 and avg_steps < 5000:
        idx = 0
    elif training_days <= 3 or avg_steps < 8000:
        idx = 1
    elif training_days <= 4 or avg_steps < 10000:
        idx = 2
    elif training_days <= 6:
        idx = 3
    else:
        idx = 4
        
    tdee = bmr * multipliers[idx]
    return round(tdee, 2)

def calculate_calorie_target(tdee: float, fitness_goal: str) -> float:
    """
    Calculates daily calorie target safely based on goal.
    Avoids extreme deficit or surplus.
    """
    goal = fitness_goal.lower()
    
    if "weight loss" in goal or "fat loss" in goal:
        calorie_target = tdee - 400.0  # Safe moderate deficit
    elif "muscle gain" in goal or "bulk" in goal:
        calorie_target = tdee + 300.0  # Safe moderate surplus
    elif "lean bulk" in goal:
        calorie_target = tdee + 200.0
    else:  # Maintain, Endurance, General Fitness
        calorie_target = tdee
        
    return round(max(calorie_target, 1200.0), 2)  # Floor at 1200 kcal for safety

def calculate_macros(calorie_target: float, weight_kg: float, fitness_goal: str) -> dict:
    """
    Calculates macro targets (Protein, Carbs, Fats) in grams.
    Protein: 1.6g - 2.2g per kg based on goal.
    Fat: ~25% of total calories.
    Carbs: Remaining calories.
    """
    goal = fitness_goal.lower()
    
    if "muscle" in goal or "bulk" in goal or "strength" in goal:
        protein_g = weight_kg * 2.0
    elif "loss" in goal:
        protein_g = weight_kg * 1.8
    else:
        protein_g = weight_kg * 1.6
        
    protein_calories = protein_g * 4
    fat_calories = calorie_target * 0.25
    fat_g = fat_calories / 9.0
    
    carb_calories = max(calorie_target - (protein_calories + fat_calories), 0)
    carb_g = carb_calories / 4.0
    
    return {
        "protein_g": round(protein_g, 1),
        "fat_g": round(fat_g, 1),
        "carb_g": round(carb_g, 1)
    }

def calculate_lifestyle_targets(weight_kg: float, age: int, stress_level: int) -> dict:
    """
    Calculates recommended daily targets for water, steps, sleep, and stress tips.
    """
    # Water: ~35ml per kg of body weight
    water_liters = round((weight_kg * 0.035), 1)
    
    # Step target
    step_target = 10000 if weight_kg > 80 else 8000
    
    # Sleep target based on age
    sleep_target = 8.0 if age < 25 else 7.5
    
    # Non-medical stress tips based on self-reported stress level (1-10)
    stress_tips = []
    if stress_level >= 7:
        stress_tips = [
            "Take a 10-minute quiet walk outside without screen time.",
            "Practice box breathing: Inhale 4s, Hold 4s, Exhale 4s, Hold 4s.",
            "Prioritize 8 hours of sleep tonight to promote neural recovery."
        ]
    elif stress_level >= 4:
        stress_tips = [
            "Take short 5-minute stretch breaks every 2 hours.",
            "Stay hydrated and avoid high caffeine intake after 4 PM."
        ]
    else:
        stress_tips = ["Your stress level looks optimal! Maintain your current sleep and activity routine."]
        
    return {
        "water_liters": water_liters,
        "step_target": step_target,
        "sleep_target": sleep_target,
        "stress_tips": stress_tips
    }

def generate_full_metrics(user_data: dict) -> dict:
    """
    Master pipeline function that combines all calculations.
    """
    weight = float(user_data['weight'])
    height = float(user_data['height'])
    age = int(user_data['age'])
    gender = user_data['gender']
    days = int(user_data['training_days'])
    steps = int(user_data.get('avg_steps', 5000))
    goal = user_data['fitness_goal']
    stress = int(user_data.get('stress_level', 5))

    bmi_info = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, days, steps)
    calories = calculate_calorie_target(tdee, goal)
    macros = calculate_macros(calories, weight, goal)
    lifestyle = calculate_lifestyle_targets(weight, age, stress)

    return {
        "bmi": bmi_info['bmi'],
        "bmi_category": bmi_info['category'],
        "bmr": bmr,
        "tdee": tdee,
        "target_calories": calories,
        "target_protein": macros['protein_g'],
        "target_carbs": macros['carb_g'],
        "target_fat": macros['fat_g'],
        "target_water": lifestyle['water_liters'],
        "target_steps": lifestyle['step_target'],
        "target_sleep": lifestyle['sleep_target'],
        "stress_tips": lifestyle['stress_tips']
    }

if __name__ == "__main__":
    # Test script with sample user profile
    sample_user = {
        "name": "Alex",
        "age": 22,
        "gender": "male",
        "height": 175,
        "weight": 70,
        "training_days": 4,
        "avg_steps": 7000,
        "fitness_goal": "Muscle Gain",
        "stress_level": 6
    }
    results = generate_full_metrics(sample_user)
    print("--- Test Fitness Calculations ---")
    for k, v in results.items():
        print(f"{k}: {v}")