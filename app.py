import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --------------------------------------
# EXPANDED HEALTHY HIGH PROTEIN SOUTH INDIAN MEALS DATASET
# --------------------------------------
meals = {
    "breakfast": [
        {"name": "Oats Idli (4 pcs) with Sambar", "calories": 250, "protein": 14, "carbs": 38, "fat": 5, "diet": "Vegetarian"},
        {"name": "Ragi Dosa (2 pcs) with Groundnut Chutney", "calories": 270, "protein": 12, "carbs": 42, "fat": 6, "diet": "Vegetarian"},
        {"name": "Vegetable Upma with Peanuts (low oil)", "calories": 280, "protein": 10, "carbs": 44, "fat": 7, "diet": "Vegetarian"},
        {"name": "Moong Dal Cheela (2 pcs) with Curd", "calories": 300, "protein": 18, "carbs": 32, "fat": 8, "diet": "Vegetarian"},
        {"name": "Egg White Omelette (3 whites) with Millet Toast", "calories": 320, "protein": 22, "carbs": 28, "fat": 7, "diet": "Non-Vegetarian"},
        {"name": "Millet Pongal with Dal & Ghee (1 tsp)", "calories": 290, "protein": 13, "carbs": 40, "fat": 8, "diet": "Vegetarian"},
        {"name": "Protein Smoothie (Curd/Whey, Banana, Nuts)", "calories": 350, "protein": 30, "carbs": 35, "fat": 9, "diet": "Any"},
        {"name": "Whole Wheat Dosa (2) with high-protein Sambar", "calories": 260, "protein": 15, "carbs": 40, "fat": 4, "diet": "Vegetarian"},
        {"name": "Scrambled Tofu (South Indian style) with 1 Chapati", "calories": 310, "protein": 25, "carbs": 30, "fat": 10, "diet": "Vegetarian"},
        {"name": "Podi Idli (4) with Sesame/Flax Seed Podi & Curd", "calories": 280, "protein": 16, "carbs": 35, "fat": 9, "diet": "Vegetarian"},
        {"name": "Besan (Chickpea Flour) Cheela (2) with Veggies", "calories": 290, "protein": 18, "carbs": 34, "fat": 8, "diet": "Vegetarian"},
        {"name": "Chicken Mince Keema (100g) with 1 Whole Wheat Parotta", "calories": 400, "protein": 35, "carbs": 30, "fat": 15, "diet": "Non-Vegetarian"},
        {"name": "Vegetable & Oats Porridge (Savory)", "calories": 240, "protein": 12, "carbs": 36, "fat": 6, "diet": "Vegetarian"},
        {"name": "2 Boiled Eggs with 1 slice Brown Bread", "calories": 280, "protein": 18, "carbs": 25, "fat": 10, "diet": "Non-Vegetarian"},
    ],
    "lunch": [
        {"name": "Brown Rice with Sambar & Vegetable Poriyal (generous portion)", "calories": 380, "protein": 18, "carbs": 60, "fat": 7, "diet": "Vegetarian"},
        {"name": "Foxtail Millet Vegetable Biryani (low oil)", "calories": 400, "protein": 16, "carbs": 58, "fat": 10, "diet": "Vegetarian"},
        {"name": "Grilled Chicken (150g) with Red Rice & Salad", "calories": 430, "protein": 32, "carbs": 45, "fat": 10, "diet": "Non-Vegetarian"},
        {"name": "Fish Curry (2 pcs) with Steamed Brown Rice & Veg Curry", "calories": 420, "protein": 28, "carbs": 50, "fat": 10, "diet": "Non-Vegetarian"},
        {"name": "Mixed Dal with Brown Rice & Large Salad", "calories": 390, "protein": 20, "carbs": 55, "fat": 7, "diet": "Vegetarian"},
        {"name": "Tofu Curry (150g Tofu) with Red Rice", "calories": 410, "protein": 22, "carbs": 52, "fat": 8, "diet": "Vegetarian"},
        {"name": "Quinoa with Chana Masala (Chickpea) Curry", "calories": 450, "protein": 25, "carbs": 65, "fat": 10, "diet": "Vegetarian"},
        {"name": "Vegetable & Paneer Pulao with Raita (Curd)", "calories": 420, "protein": 20, "carbs": 55, "fat": 12, "diet": "Vegetarian"},
        {"name": "Chicken Chettinad (less gravy) with 1 Wheat Chapati & Salad", "calories": 480, "protein": 40, "carbs": 40, "fat": 15, "diet": "Non-Vegetarian"},
        {"name": "Rajma (Kidney Bean) Curry with Jowar Roti (2)", "calories": 440, "protein": 24, "carbs": 65, "fat": 9, "diet": "Vegetarian"},
        {"name": "Egg Bhurji (3 eggs) with Brown Rice", "calories": 400, "protein": 28, "carbs": 45, "fat": 12, "diet": "Non-Vegetarian"},
        {"name": "Lentil (Masoor Dal) Kichadi with mixed vegetables", "calories": 390, "protein": 20, "carbs": 58, "fat": 8, "diet": "Vegetarian"},
        {"name": "Fish Fry (150g) with Steamed Vegetables", "calories": 380, "protein": 35, "carbs": 15, "fat": 15, "diet": "Non-Vegetarian"},
        {"name": "Vegetable Salad (Large) with 1/2 cup Moong Dal", "calories": 350, "protein": 18, "carbs": 45, "fat": 10, "diet": "Vegetarian"},
    ],
    "dinner": [
        {"name": "Chapati (2) with Moong Dal & Raw Salad", "calories": 310, "protein": 18, "carbs": 42, "fat": 6, "diet": "Vegetarian"},
        {"name": "Ragi Roti (2) with Vegetable Kurma (low coconut)", "calories": 320, "protein": 14, "carbs": 40, "fat": 7, "diet": "Vegetarian"},
        {"name": "Grilled Fish (150g) with Steamed Vegetables", "calories": 350, "protein": 30, "carbs": 20, "fat": 8, "diet": "Non-Vegetarian"},
        {"name": "Egg Curry (2 eggs) with 1 Chapati & Cucumber Salad", "calories": 360, "protein": 24, "carbs": 36, "fat": 9, "diet": "Non-Vegetarian"},
        {"name": "Vegetable Stew with Millet Appam (2) (light dinner)", "calories": 330, "protein": 13, "carbs": 46, "fat": 8, "diet": "Vegetarian"},
        {"name": "Paneer Bhurji (100g) with 1 Phulka", "calories": 340, "protein": 22, "carbs": 38, "fat": 9, "diet": "Vegetarian"},
        {"name": "Chicken Stir-fry (150g) with minimal soy sauce", "calories": 380, "protein": 38, "carbs": 15, "fat": 18, "diet": "Non-Vegetarian"},
        {"name": "Tofu & Spinach Curry with 2 Whole Wheat Roti", "calories": 370, "protein": 25, "carbs": 40, "fat": 12, "diet": "Vegetarian"},
        {"name": "Lentil Soup (thick) with a side of mixed vegetables", "calories": 280, "protein": 16, "carbs": 35, "fat": 6, "diet": "Vegetarian"},
        {"name": "Low-fat Curd Rice with Grilled Vegetables", "calories": 300, "protein": 12, "carbs": 45, "fat": 5, "diet": "Vegetarian"},
        {"name": "Prawn Masala (120g) with 1 Ragi Roti", "calories": 390, "protein": 32, "carbs": 28, "fat": 14, "diet": "Non-Vegetarian"},
        {"name": "Oats Dosa (2) with Raw Vegetable Salad", "calories": 270, "protein": 15, "carbs": 40, "fat": 5, "diet": "Vegetarian"},
        {"name": "Mushroom Pepper Fry with 2 Chapati", "calories": 340, "protein": 15, "carbs": 45, "fat": 10, "diet": "Vegetarian"},
        {"name": "Clear Vegetable Soup (Large) with 1 Wheat Rusk", "calories": 180, "protein": 10, "carbs": 25, "fat": 4, "diet": "Vegetarian"},
    ],
    "snack": [
        {"name": "Sprout Salad (1 bowl)", "calories": 180, "protein": 10, "carbs": 22, "fat": 5, "diet": "Vegetarian"},
        {"name": "Buttermilk with Roasted Chana (50g)", "calories": 150, "protein": 8, "carbs": 18, "fat": 3, "diet": "Vegetarian"},
        {"name": "Fruit (Apple/Orange) & Curd Bowl", "calories": 160, "protein": 7, "carbs": 28, "fat": 3, "diet": "Vegetarian"},
        {"name": "Peanut Sundal (boiled)", "calories": 190, "protein": 10, "carbs": 22, "fat": 6, "diet": "Vegetarian"},
        {"name": "Green Gram Sundal (high fiber)", "calories": 170, "protein": 9, "carbs": 20, "fat": 4, "diet": "Vegetarian"},
        {"name": "Roasted Almonds (1 oz/28g)", "calories": 170, "protein": 6, "carbs": 6, "fat": 15, "diet": "Vegetarian"},
        {"name": "Vegetable Sticks with Hummus (50g)", "calories": 140, "protein": 5, "carbs": 15, "fat": 7, "diet": "Vegetarian"},
        {"name": "Boiled Egg Whites (3 pcs)", "calories": 60, "protein": 12, "carbs": 1, "fat": 0, "diet": "Non-Vegetarian"},
        {"name": "Protein Bar (Homemade/Mock)", "calories": 220, "protein": 15, "carbs": 20, "fat": 10, "diet": "Any"},
        {"name": "Whey Protein Shake (1 scoop)", "calories": 130, "protein": 25, "carbs": 5, "fat": 2, "diet": "Any"},
        {"name": "Fruit Salad with Chia Seeds", "calories": 150, "protein": 4, "carbs": 30, "fat": 2, "diet": "Vegetarian"},
        {"name": "Black Coffee/Tea (Zero Calories) with 1 Rusk", "calories": 50, "protein": 2, "carbs": 8, "fat": 1, "diet": "Vegetarian"},
        {"name": "Paneer Cubes (50g) grilled with mint chutney", "calories": 160, "protein": 12, "carbs": 3, "fat": 11, "diet": "Vegetarian"},
        {"name": "Watermelon/Melon (Large bowl)", "calories": 80, "protein": 2, "carbs": 18, "fat": 1, "diet": "Vegetarian"},
    ]
}

# --------------------------
# Meal Plan Generator
# --------------------------
def generate_meal_plan(name, age, gender, height, weight, activity_level, diet_preference, goal):
    """Calculates TDEE and generates a 4-week meal plan with daily macro totals."""
    
    # 1. TDEE Calculation
    bmi = weight / ((height/100) ** 2)
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    activity = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725, "Extremely Active": 1.9}
    daily_calories = bmr * activity.get(activity_level, 1.55)
    
    # Apply goal multiplier
    if goal == "Lose Weight": daily_calories *= 0.85
    elif goal == "Gain Muscle": daily_calories *= 1.1

    # BMI category
    bmi_category = "Underweight" if bmi < 18.5 else "Healthy" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"

    # 2. Filter meals
    filtered = {k: [m for m in v if diet_preference == "Any" or m["diet"] == diet_preference] for k, v in meals.items()}
    
    # Fallback: If filtering resulted in empty list, use all meals for that category
    for meal_type, filtered_list in filtered.items():
        if not filtered_list:
            filtered[meal_type] = meals[meal_type]

    # 3. Generate 4-week plan with less repetition and daily totals
    start = datetime.now() - timedelta(days=datetime.now().weekday())
    plan = []
    
    for week in range(4):
        week_days = []
        
        # Create shuffled meal lists for the week (double length for variety over 7 days)
        weekly_meal_options = {}
        for mtype in filtered:
            # Shuffle the filtered list and extend it to at least 7 items for the week
            options = filtered[mtype].copy()
            random.shuffle(options)
            # Ensure there are enough unique or semi-unique meals for 7 days
            weekly_meal_options[mtype] = (options * (7 // len(options) + 1))[:7] 
            random.shuffle(weekly_meal_options[mtype]) # Shuffle again for less predictable order

        meal_tracker = {mtype: 0 for mtype in filtered}

        for day in range(7):
            date = start + timedelta(weeks=week, days=day)
            day_meals = {}
            daily_totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

            for mtype in filtered:
                # Select the next meal from the shuffled, weekly pool using a circular index
                meal_index = meal_tracker[mtype] % len(weekly_meal_options[mtype])
                m = weekly_meal_options[mtype][meal_index]
                
                day_meals[mtype] = m
                
                # Calculate daily totals
                daily_totals["calories"] += m["calories"]
                daily_totals["protein"] += m["protein"]
                daily_totals["carbs"] += m["carbs"]
                daily_totals["fat"] += m["fat"]
                
                meal_tracker[mtype] += 1
                
            week_days.append({
                "day": date.strftime("%A"), 
                "date": date.strftime("%b %d"), 
                "meals": day_meals, 
                "totals": daily_totals
            })
        plan.append({"week": week+1, "days": week_days})

    return create_html(name, bmi, bmi_category, int(daily_calories), goal, plan)

# --------------------------
# HTML Renderer + Download
# --------------------------
def create_html(name, bmi, bmi_cat, cal, goal, plan):
    """Generates the HTML output displaying the meal plan and daily totals."""
    
    html = f"""
    <style>
    body {{font-family: 'Poppins', sans-serif; background:#F7F6F2; color:#333;}}
    .container {{max-width:1100px;margin:auto;background:#fff;padding:30px;border-radius:15px;box-shadow:0 4px 20px rgba(0,0,0,0.1);}}
    h1,h2,h3 {{color:#2E8B57;text-align:center;}}
    table {{width:100%;border-collapse:collapse;margin-bottom:30px;}}
    th,td {{border:1px solid #ddd;padding:10px;text-align:center;vertical-align:top;}}
    th {{background:#A7DCA9;}}
    tr:nth-child(even){{background:#F3FFF3;}}
    .daily-total {{ background: #e0f2e0; font-weight: bold; font-size: 0.9em; }}
    .btn-download {{
        display:inline-block;background:#2E8B57;color:#fff;padding:10px 20px;
        border-radius:8px;text-decoration:none;font-weight:bold;margin:10px auto;display:block;width:fit-content;
    }}
    </style>
    <div class='container'>
        <h1> Healthy South Indian Meal Plan for {name}</h1>
        <p><b>BMI:</b> {bmi:.1f} ({bmi_cat}) | <b>Daily Calorie Goal:</b> {cal} kcal | <b>Goal:</b> {goal}</p>
        <p style="text-align: center; font-style: italic; font-size: 0.9em;">
            Daily totals reflect the nutrition of the meals generated.
        </p>
    """
    for week in plan:
        # Updated header to reflect the new totals column
        html += f"<h2>Week {week['week']}</h2><table><tr><th>Day & Daily Totals</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th><th>Snack</th></tr>" 
        for day in week["days"]:
            totals = day['totals']
            
            # Daily Totals Column
            day_info = f"""
            <td class='daily-total'>
                <b>{day['day']}</b><br>{day['date']}
                <hr style='border-top: 1px solid #ccc; margin: 5px 0;'>
                Total Cal: {totals['calories']} kcal<br>
                Protein: {totals['protein']}g | Carbs: {totals['carbs']}g | Fat: {totals['fat']}g
            </td>
            """
            
            html += f"<tr>{day_info}"
            for meal in ["breakfast", "lunch", "dinner", "snack"]:
                m = day['meals'][meal]
                # Display individual meal macros using a more compact format (P/C/F)
                html += f"<td><b>{m['name']}</b><br><small> {m['calories']} kcal |  {m['protein']}g P |  {m['carbs']}g C |  {m['fat']}g F</small></td>"
            html += "</tr>"
        html += "</table>"
    html += """<a class='btn-download' href='javascript:void(0)' onclick="window.print()"> Download Meal Plan (PDF)</a></div>"""
    return html

# --------------------------
# Gradio Interface
# --------------------------
iface = gr.Interface(
    fn=generate_meal_plan,
    inputs=[
        gr.Textbox(label="Name"),
        gr.Number(label="Age", precision=0),
        gr.Radio(["Male", "Female"], label="Gender"),
        gr.Number(label="Height (cm)"),
        gr.Number(label="Weight (kg)"),
        gr.Radio(["Sedentary","Lightly Active","Moderately Active","Very Active","Extremely Active"], label="Activity Level"),
        gr.Radio(["Vegetarian","Non-Vegetarian","Any"], label="Diet Preference"),
        gr.Radio(["Lose Weight","Gain Muscle","Maintain Weight"], label="Goal")
    ],
    outputs=gr.HTML(label="Your Personalized 4-Week Meal Plan"),
    title=" South Indian Healthy Meal Planner",
    description="Generate a 4-week healthy, high-protein, low-fat South Indian meal plan based on your profile. Click 'Download' to save as PDF."
)

if __name__ == "__main__":
    iface.launch()