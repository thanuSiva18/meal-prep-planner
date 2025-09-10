import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --------------------------
# Tamil Nadu Style Meals Dataset
# --------------------------
meals = {
    "breakfast": [
        {"name": "Idli with Sambar & Coconut Chutney", "calories": 320, "protein": 12, "carbs": 60, "fat": 5, "diet": "Vegetarian"},
        {"name": "Dosa with Potato Masala", "calories": 380, "protein": 10, "carbs": 55, "fat": 12, "diet": "Vegetarian"},
        {"name": "Pongal with Coconut Chutney", "calories": 340, "protein": 14, "carbs": 58, "fat": 8, "diet": "Vegetarian"},
        {"name": "Upma with Sambar", "calories": 290, "protein": 8, "carbs": 48, "fat": 6, "diet": "Vegetarian"},
        {"name": "Appam with Vegetable Stew", "calories": 330, "protein": 9, "carbs": 52, "fat": 9, "diet": "Vegetarian"},
        {"name": "Rava Kichadi with Coconut Chutney", "calories": 310, "protein": 11, "carbs": 46, "fat": 8, "diet": "Vegetarian"},
        {"name": "Poori with Potato Masala", "calories": 420, "protein": 12, "carbs": 68, "fat": 14, "diet": "Vegetarian"},
        {"name": "Adai Dosa with Avial", "calories": 360, "protein": 15, "carbs": 50, "fat": 10, "diet": "Vegetarian"},
        {"name": "Medu Vada with Sambar", "calories": 350, "protein": 14, "carbs": 42, "fat": 16, "diet": "Vegetarian"},
        {"name": "Rava Dosa with Tomato Chutney", "calories": 300, "protein": 8, "carbs": 45, "fat": 10, "diet": "Vegetarian"},
        {"name": "Kuzhi Paniyaram with Coconut Chutney", "calories": 280, "protein": 10, "carbs": 40, "fat": 8, "diet": "Vegetarian"},
        {"name": "Puttu with Kadala Curry", "calories": 340, "protein": 12, "carbs": 54, "fat": 7, "diet": "Vegetarian"}
    ],
    "lunch": [
        {"name": "Sambar Rice with Poriyal", "calories": 420, "protein": 14, "carbs": 70, "fat": 8, "diet": "Vegetarian"},
        {"name": "Curd Rice with Pickle & Papad", "calories": 380, "protein": 12, "carbs": 60, "fat": 10, "diet": "Vegetarian"},
        {"name": "Rasam Rice with Potato Fry", "calories": 350, "protein": 10, "carbs": 65, "fat": 6, "diet": "Vegetarian"},
        {"name": "Lemon Rice with Raita", "calories": 360, "protein": 8, "carbs": 58, "fat": 12, "diet": "Vegetarian"},
        {"name": "Coconut Rice with Mor Kuzhambu", "calories": 410, "protein": 11, "carbs": 64, "fat": 14, "diet": "Vegetarian"},
        {"name": "Veg Biryani with Raita", "calories": 450, "protein": 15, "carbs": 72, "fat": 12, "diet": "Vegetarian"},
        {"name": "Puliyodarai (Tamarind Rice) with Papad", "calories": 380, "protein": 9, "carbs": 60, "fat": 14, "diet": "Vegetarian"},
        {"name": "Kara Kuzhambu Rice with Thoran", "calories": 390, "protein": 12, "carbs": 68, "fat": 8, "diet": "Vegetarian"},
        {"name": "Tomato Rice with Potato Curry", "calories": 370, "protein": 10, "carbs": 62, "fat": 10, "diet": "Vegetarian"},
        {"name": "Chicken Biryani", "calories": 520, "protein": 28, "carbs": 65, "fat": 18, "diet": "Non-Vegetarian"},
        {"name": "Fish Curry Rice", "calories": 480, "protein": 25, "carbs": 60, "fat": 15, "diet": "Non-Vegetarian"},
        {"name": "Mutton Curry with Rice", "calories": 530, "protein": 30, "carbs": 58, "fat": 22, "diet": "Non-Vegetarian"}
    ],
    "dinner": [
        {"name": "Chapati with Vegetable Kurma", "calories": 380, "protein": 14, "carbs": 50, "fat": 12, "diet": "Vegetarian"},
        {"name": "Idiyappam with Vegetable Stew", "calories": 320, "protein": 10, "carbs": 52, "fat": 6, "diet": "Vegetarian"},
        {"name": "Dosa with Sambar", "calories": 310, "protein": 12, "carbs": 45, "fat": 8, "diet": "Vegetarian"},
        {"name": "Parotta with Salna", "calories": 460, "protein": 14, "carbs": 58, "fat": 18, "diet": "Vegetarian"},
        {"name": "Appam with Vegetable Curry", "calories": 350, "protein": 9, "carbs": 54, "fat": 10, "diet": "Vegetarian"},
        {"name": "Sevai (Rice Noodles) with Kurma", "calories": 330, "protein": 11, "carbs": 56, "fat": 8, "diet": "Vegetarian"},
        {"name": "Chapati with Dal Tadka", "calories": 340, "protein": 16, "carbs": 48, "fat": 7, "diet": "Vegetarian"},
        {"name": "Set Dosa with Vegetable Sagu", "calories": 360, "protein": 12, "carbs": 52, "fat": 10, "diet": "Vegetarian"},
        {"name": "Ragi Roti with Chutney", "calories": 290, "protein": 12, "carbs": 40, "fat": 8, "diet": "Vegetarian"},
        {"name": "Parotta with Chicken Curry", "calories": 520, "protein": 28, "carbs": 56, "fat": 22, "diet": "Non-Vegetarian"},
        {"name": "Kothu Parotta with Egg", "calories": 510, "protein": 24, "carbs": 58, "fat": 20, "diet": "Non-Vegetarian"},
        {"name": "Chepala Pulusu (Fish Curry) with Rice", "calories": 450, "protein": 26, "carbs": 50, "fat": 16, "diet": "Non-Vegetarian"}
    ],
    "snack": [
        {"name": "Murukku", "calories": 180, "protein": 4, "carbs": 28, "fat": 8, "diet": "Vegetarian"},
        {"name": "Thattai", "calories": 160, "protein": 3, "carbs": 24, "fat": 7, "diet": "Vegetarian"},
        {"name": "Vadai with Tea", "calories": 220, "protein": 8, "carbs": 26, "fat": 12, "diet": "Vegetarian"},
        {"name": "Sundal (Chickpea Salad)", "calories": 190, "protein": 9, "carbs": 28, "fat": 5, "diet": "Vegetarian"},
        {"name": "Bajji/Pakoda", "calories": 210, "protein": 6, "carbs": 22, "fat": 14, "diet": "Vegetarian"},
        {"name": "Kozhukkattai (Sweet/Savory)", "calories": 230, "protein": 5, "carbs": 35, "fat": 8, "diet": "Vegetarian"},
        {"name": "Verkadalai Urundai (Peanut Balls)", "calories": 240, "protein": 12, "carbs": 18, "fat": 16, "diet": "Vegetarian"},
        {"name": "Paruppu Vadai", "calories": 180, "protein": 10, "carbs": 20, "fat": 8, "diet": "Vegetarian"},
        {"name": "Ellu Urundai (Sesame Balls)", "calories": 200, "protein": 6, "carbs": 16, "fat": 15, "diet": "Vegetarian"},
        {"name": "Paniyaram with Chutney", "calories": 190, "protein": 7, "carbs": 28, "fat": 6, "diet": "Vegetarian"},
        {"name": "Filter Coffee", "calories": 70, "protein": 1, "carbs": 12, "fat": 2, "diet": "Vegetarian"},
        {"name": "Kamarkat (Jaggery Sweet)", "calories": 160, "protein": 2, "carbs": 32, "fat": 3, "diet": "Vegetarian"}
    ]
}

# --------------------------
# Meal Plan Generator
# --------------------------
def generate_meal_plan(name, age, gender, height, weight, activity_level, diet_preference, goal):
    # --- BMI & Calories ---
    bmi = weight / ((height/100) ** 2)
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    activity_multipliers = {
        "Sedentary": 1.2, "Lightly Active": 1.375,
        "Moderately Active": 1.55, "Very Active": 1.725,
        "Extremely Active": 1.9
    }
    daily_calories = bmr * activity_multipliers.get(activity_level, 1.55)

    if goal == "Lose Weight":
        daily_calories *= 0.8
    elif goal == "Gain Muscle":
        daily_calories *= 1.1

    meal_distribution = {
        'Breakfast': int(daily_calories * 0.25),
        'Lunch': int(daily_calories * 0.35),
        'Dinner': int(daily_calories * 0.30),
        'Snack': int(daily_calories * 0.10)
    }

    # --- Filter Meals ---
    filtered_meals = {
        "breakfast": [m for m in meals["breakfast"] if diet_preference == "Any" or m["diet"] == diet_preference],
        "lunch": [m for m in meals["lunch"] if diet_preference == "Any" or m["diet"] == diet_preference],
        "dinner": [m for m in meals["dinner"] if diet_preference == "Any" or m["diet"] == diet_preference],
        "snack": [m for m in meals["snack"] if diet_preference == "Any" or m["diet"] == diet_preference]
    }
    for meal_type in filtered_meals:
        if not filtered_meals[meal_type]:
            filtered_meals[meal_type] = meals[meal_type]

    # --- Weekly Plan ---
    start_date = datetime.now() - timedelta(days=datetime.now().weekday())
    structured_plan = []
    for week in range(4):
        week_plan, weekly_meal_tracking = [], {"breakfast": [], "lunch": [], "dinner": [], "snack": []}
        for day in range(7):
            day_date = start_date + timedelta(weeks=week, days=day)
            day_meals = {}
            for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
                available = [m for m in filtered_meals[meal_type] if m["name"] not in weekly_meal_tracking[meal_type]]
                if len(available) < 2:
                    available = filtered_meals[meal_type]
                selected = random.choice(available)
                weekly_meal_tracking[meal_type].append(selected["name"])
                day_meals[meal_type] = selected
            week_plan.append({"day": day_date.strftime("%A"), "date": day_date.strftime("%b %d"), "meals": day_meals})
        structured_plan.append({"week": week+1, "days": week_plan})

    # --- BMI Category ---
    if bmi < 18.5: bmi_category = "Underweight"
    elif bmi < 25: bmi_category = "Healthy Weight"
    elif bmi < 30: bmi_category = "Overweight"
    else: bmi_category = "Obese"

    # --- Macronutrients ---
    if goal == "Lose Weight":
        protein_ratio, carb_ratio, fat_ratio = 0.30, 0.40, 0.30
    elif goal == "Gain Muscle":
        protein_ratio, carb_ratio, fat_ratio = 0.35, 0.45, 0.20
    else:
        protein_ratio, carb_ratio, fat_ratio = 0.25, 0.50, 0.25

    health_profile = {
        "name": name, "bmi": round(bmi, 1), "bmi_category": bmi_category,
        "daily_calories": int(daily_calories), "goal": goal,
        "meal_distribution": meal_distribution,
        "macros": {
            "protein": int((daily_calories * protein_ratio) / 4),
            "carbs": int((daily_calories * carb_ratio) / 4),
            "fat": int((daily_calories * fat_ratio) / 9)
        }
    }

    return create_tamil_nadu_html(health_profile, structured_plan)

# --------------------------
# HTML Renderer
# --------------------------
def create_tamil_nadu_html(profile, meal_plan):
    meal_plan_html = ""
    for week in meal_plan:
        meal_plan_html += f"<h3 style='margin-top:40px;'>Week {week['week']}</h3><table><thead><tr><th>Day</th><th>Date</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th><th>Snack</th></tr></thead><tbody>"
        for day in week["days"]:
            meal_plan_html += f"<tr><td>{day['day']}</td><td>{day['date']}</td><td>{day['meals']['breakfast']['name']}</td><td>{day['meals']['lunch']['name']}</td><td>{day['meals']['dinner']['name']}</td><td>{day['meals']['snack']['name']}</td></tr>"
        meal_plan_html += "</tbody></table>"

    html = f"""
    <html><head><style>
    body {{ font-family: Poppins, sans-serif; margin:20px; background:#FFFBF5; }}
    table {{ width:100%; border-collapse:collapse; margin-bottom:40px; }}
    th,td {{ border:1px solid #D8B6A4; padding:10px; text-align:center; }}
    th {{ background:#FFC288; }}
    tr:nth-child(even) {{ background:#fafafa; }}
    </style></head><body>
    <div style="max-width:800px;margin:auto;padding:20px;background:#fff;border-radius:10px;">
        <h1>Tamil Nadu Style Meal Plan for {profile['name']}</h1>
        <p><b>BMI:</b> {profile['bmi']} ({profile['bmi_category']})</p>
        <p><b>Daily Calories:</b> {profile['daily_calories']}</p>
        <p><b>Goal:</b> {profile['goal']}</p>
        <h3>Meal Distribution</h3>
        <ul><li>Breakfast: {profile['meal_distribution']['Breakfast']} cal</li>
            <li>Lunch: {profile['meal_distribution']['Lunch']} cal</li>
            <li>Dinner: {profile['meal_distribution']['Dinner']} cal</li>
            <li>Snack: {profile['meal_distribution']['Snack']} cal</li></ul>
        <h3>Macros</h3>
        <ul><li>Protein: {profile['macros']['protein']} g</li>
            <li>Carbs: {profile['macros']['carbs']} g</li>
            <li>Fat: {profile['macros']['fat']} g</li></ul>
    </div>{meal_plan_html}</body></html>
    """
    return html

# --------------------------
# Gradio Interface
# --------------------------
iface = gr.Interface(
    fn=generate_meal_plan,
    inputs=[
        gr.Textbox(label="Name"),
        gr.Number(label="Age", precision=0),
        gr.Radio(choices=["Male", "Female"], label="Gender"),
        gr.Number(label="Height (cm)"),
        gr.Number(label="Weight (kg)"),
        gr.Radio(choices=["Sedentary","Lightly Active","Moderately Active","Very Active","Extremely Active"], label="Activity Level"),
        gr.Radio(choices=["Vegetarian","Non-Vegetarian","Any"], label="Diet Preference"),
        gr.Radio(choices=["Lose Weight","Gain Muscle","Maintain Weight"], label="Goal")
    ],
    outputs=gr.HTML(label="Meal Plan")
)

if __name__ == "__main__":
    iface.launch()
