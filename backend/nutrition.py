import pandas as pd
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "foods.csv")

def load_food_dataset() -> pd.DataFrame:
    """Loads foods.csv using Pandas."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Nutrition dataset not found at {CSV_PATH}")
    return pd.read_csv(CSV_PATH)

def generate_meal_plan(target_calories: float, target_protein: float, diet_preference: str) -> dict:
    """
    Uses Pandas to filter foods based on dietary preference and meal type,
    constructing a structured 5-meal daily nutrition plan.
    """
    df = load_food_dataset()
    diet = diet_preference.lower()

    # Filter by dietary preference using Pandas Boolean Indexing
    if "vegan" in diet:
        df_filtered = df[df['vegan'] == 1]
    elif "vegetarian" in diet or "veg" in diet:
        df_filtered = df[df['vegetarian'] == 1]
    else:  # Non-Vegetarian / Eggetarian
        df_filtered = df

    meal_order = ["Breakfast", "Snack", "Lunch", "Pre-Workout", "Dinner"]
    selected_meals = {}
    total_plan_calories = 0
    total_plan_protein = 0
    total_plan_carbs = 0
    total_plan_fat = 0

    for meal in meal_order:
        # Pandas filtering for specific meal_type
        meal_df = df_filtered[df_filtered['meal_type'] == meal]
        
        if meal_df.empty:
            # Fallback if no specific dietary match found
            meal_df = df[df['meal_type'] == meal]
            
        # Sample 1 random food item for variety using Pandas sample
        chosen_food = meal_df.sample(n=1).iloc[0]

        food_name = chosen_food['food_name']
        cals = float(chosen_food['calories'])
        prot = float(chosen_food['protein'])
        carbs = float(chosen_food['carbs'])
        fat = float(chosen_food['fat'])

        selected_meals[meal] = {
            "item": food_name,
            "calories": cals,
            "protein_g": prot,
            "carbs_g": carbs,
            "fat_g": fat
        }

        total_plan_calories += cals
        total_plan_protein += prot
        total_plan_carbs += carbs
        total_plan_fat += fat

    return {
        "diet_preference": diet_preference,
        "daily_targets": {
            "target_calories": target_calories,
            "target_protein": target_protein
        },
        "plan_totals": {
            "total_calories": round(total_plan_calories, 1),
            "total_protein": round(total_plan_protein, 1),
            "total_carbs": round(total_plan_carbs, 1),
            "total_fat": round(total_plan_fat, 1)
        },
        "meals": selected_meals
    }

if __name__ == "__main__":
    print("--- Testing Pandas Nutrition Meal Plan Generator ---")
    plan = generate_meal_plan(target_calories=2200, target_protein=130, diet_preference="Vegetarian")
    print(f"Diet Preference: {plan['diet_preference']}")
    print(f"Total Plan Calories: {plan['plan_totals']['total_calories']} kcal | Protein: {plan['plan_totals']['total_protein']} g")
    for meal_type, info in plan['meals'].items():
        print(f"  [{meal_type}] {info['item']} -> {info['calories']} kcal | {info['protein_g']}g P")