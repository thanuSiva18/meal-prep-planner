import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --------------------------------------
# ULTRA-HEALTHY LOW-FAT HIGH-PROTEIN SOUTH INDIAN MEALS
# --------------------------------------
meals = {
    "breakfast": [
        {"name": "Steamed Idli (4 pcs) with Sambar & Coconut Chutney", "calories": 240, "protein": 12, "carbs": 42, "fat": 3, "diet": "Vegetarian"},
        {"name": "Ragi Idli (4 pcs) with Mint Chutney", "calories": 230, "protein": 11, "carbs": 40, "fat": 2.5, "diet": "Vegetarian"},
        {"name": "Oats Idli (4 pcs) with Dal Sambar", "calories": 235, "protein": 13, "carbs": 38, "fat": 3.5, "diet": "Vegetarian"},
        {"name": "Vegetable Upma with Moong Dal (oil-free)", "calories": 220, "protein": 11, "carbs": 40, "fat": 2, "diet": "Vegetarian"},
        {"name": "Ragi Dosa (2 pcs) with Tomato Chutney", "calories": 245, "protein": 10, "carbs": 44, "fat": 3, "diet": "Vegetarian"},
        {"name": "Moong Dal Cheela (2 pcs) with Low-fat Curd", "calories": 260, "protein": 18, "carbs": 32, "fat": 4, "diet": "Vegetarian"},
        {"name": "Egg White Omelette (4 whites) with Whole Wheat Toast", "calories": 210, "protein": 20, "carbs": 25, "fat": 2, "diet": "Non-Vegetarian"},
        {"name": "Quinoa Upma with Vegetables (minimal oil)", "calories": 255, "protein": 12, "carbs": 42, "fat": 4, "diet": "Vegetarian"},
        {"name": "Steamed Rava Idli (3 pcs) with Vegetable Sambar", "calories": 225, "protein": 10, "carbs": 40, "fat": 2.5, "diet": "Vegetarian"},
        {"name": "Pesarattu (Moong Dal Dosa 2 pcs) with Ginger Chutney", "calories": 250, "protein": 15, "carbs": 38, "fat": 3.5, "diet": "Vegetarian"},
        {"name": "Vermicelli Upma with Vegetables (oil-free)", "calories": 215, "protein": 9, "carbs": 42, "fat": 2, "diet": "Vegetarian"},
        {"name": "Poha with Sprouted Moong & Peanuts (10g)", "calories": 240, "protein": 11, "carbs": 40, "fat": 4.5, "diet": "Vegetarian"},
        {"name": "Whole Wheat Dosa (2 pcs) with Protein-rich Sambar", "calories": 235, "protein": 14, "carbs": 40, "fat": 3, "diet": "Vegetarian"},
        {"name": "Adai (Lentil Pancake 2 pcs) with Avial (low coconut)", "calories": 270, "protein": 16, "carbs": 42, "fat": 5, "diet": "Vegetarian"},
    ],
    "lunch": [
        {"name": "Brown Rice (1 cup) with Sambar & Cabbage Poriyal", "calories": 380, "protein": 16, "carbs": 65, "fat": 4, "diet": "Vegetarian"},
        {"name": "Red Rice with Rasam, Beans Poriyal & Buttermilk", "calories": 365, "protein": 15, "carbs": 62, "fat": 4.5, "diet": "Vegetarian"},
        {"name": "Barnyard Millet with Dal & Vegetable Curry", "calories": 360, "protein": 14, "carbs": 60, "fat": 5, "diet": "Vegetarian"},
        {"name": "Grilled Chicken Breast (150g) with Brown Rice & Salad", "calories": 420, "protein": 38, "carbs": 45, "fat": 6, "diet": "Non-Vegetarian"},
        {"name": "Baked Fish (150g) with Steamed Red Rice & Curry", "calories": 400, "protein": 35, "carbs": 48, "fat": 5, "diet": "Non-Vegetarian"},
        {"name": "Mixed Dal Khichdi with Vegetables & Curd", "calories": 340, "protein": 18, "carbs": 58, "fat": 3.5, "diet": "Vegetarian"},
        {"name": "Quinoa Pulao with Chickpeas & Raita", "calories": 410, "protein": 20, "carbs": 62, "fat": 7, "diet": "Vegetarian"},
        {"name": "Foxtail Millet Biryani (vegetable, minimal oil)", "calories": 375, "protein": 14, "carbs": 65, "fat": 5, "diet": "Vegetarian"},
        {"name": "Masoor Dal with Brown Rice & Carrot Poriyal", "calories": 355, "protein": 17, "carbs": 60, "fat": 4, "diet": "Vegetarian"},
        {"name": "Moong Dal Curry with Millet Rice & Salad", "calories": 350, "protein": 16, "carbs": 58, "fat": 4.5, "diet": "Vegetarian"},
        {"name": "Rajma (Kidney Beans) with Brown Rice & Cucumber Raita", "calories": 395, "protein": 19, "carbs": 68, "fat": 5, "diet": "Vegetarian"},
        {"name": "Chicken Pepper Dry (grilled 150g) with Chapati & Salad", "calories": 430, "protein": 40, "carbs": 42, "fat": 8, "diet": "Non-Vegetarian"},
        {"name": "Chana Masala with Jowar Roti (2 pcs) & Onion Salad", "calories": 405, "protein": 21, "carbs": 65, "fat": 6, "diet": "Vegetarian"},
        {"name": "Egg White Curry (4 whites) with Brown Rice", "calories": 340, "protein": 24, "carbs": 50, "fat": 4, "diet": "Non-Vegetarian"},
    ],
    "dinner": [
        {"name": "Whole Wheat Chapati (2) with Toor Dal & Salad", "calories": 290, "protein": 16, "carbs": 48, "fat": 4, "diet": "Vegetarian"},
        {"name": "Ragi Roti (2 pcs) with Vegetable Kurma (low-fat)", "calories": 280, "protein": 12, "carbs": 46, "fat": 4.5, "diet": "Vegetarian"},
        {"name": "Millet Dosa (2 pcs) with Sambar", "calories": 265, "protein": 11, "carbs": 45, "fat": 3.5, "diet": "Vegetarian"},
        {"name": "Grilled Fish (120g) with Steamed Vegetables & Lemon", "calories": 320, "protein": 32, "carbs": 18, "fat": 6, "diet": "Non-Vegetarian"},
        {"name": "Vegetable Stew with Appam (2 pcs, oil-free)", "calories": 295, "protein": 10, "carbs": 52, "fat": 4, "diet": "Vegetarian"},
        {"name": "Moong Dal Curry with Phulka (2 pcs) & Salad", "calories": 305, "protein": 17, "carbs": 50, "fat": 3.5, "diet": "Vegetarian"},
        {"name": "Chicken Soup (clear) with Whole Wheat Roll", "calories": 275, "protein": 28, "carbs": 30, "fat": 4, "diet": "Non-Vegetarian"},
        {"name": "Tofu & Spinach Curry with Roti (2 pcs)", "calories": 315, "protein": 20, "carbs": 42, "fat": 6, "diet": "Vegetarian"},
        {"name": "Mixed Vegetable Sambar with Brown Rice (small portion)", "calories": 270, "protein": 12, "carbs": 48, "fat": 3, "diet": "Vegetarian"},
        {"name": "Beetroot & Carrot Poriyal with Chapati (2)", "calories": 285, "protein": 11, "carbs": 50, "fat": 4, "diet": "Vegetarian"},
        {"name": "Prawn Masala (100g, low-oil) with Millet Roti", "calories": 340, "protein": 30, "carbs": 35, "fat": 7, "diet": "Non-Vegetarian"},
        {"name": "Cabbage & Peas Poriyal with Ragi Mudde", "calories": 260, "protein": 10, "carbs": 46, "fat": 3.5, "diet": "Vegetarian"},
        {"name": "Egg White Bhurji (4 whites) with Chapati (1)", "calories": 245, "protein": 22, "carbs": 28, "fat": 3, "diet": "Non-Vegetarian"},
        {"name": "Clear Vegetable Soup with Steamed Idli (2 pcs)", "calories": 220, "protein": 9, "carbs": 40, "fat": 2.5, "diet": "Vegetarian"},
    ],
    "snack": [
        {"name": "Sprout Salad (1 bowl) with Lemon", "calories": 150, "protein": 10, "carbs": 22, "fat": 2, "diet": "Vegetarian"},
        {"name": "Buttermilk (1 glass) with Roasted Chana (30g)", "calories": 140, "protein": 8, "carbs": 20, "fat": 2.5, "diet": "Vegetarian"},
        {"name": "Fresh Fruit Bowl (Apple, Papaya, Orange)", "calories": 120, "protein": 2, "carbs": 28, "fat": 0.5, "diet": "Vegetarian"},
        {"name": "Steamed Sundal (Chickpea/Green Gram)", "calories": 160, "protein": 9, "carbs": 24, "fat": 2, "diet": "Vegetarian"},
        {"name": "Low-fat Curd (1 cup) with Cucumber", "calories": 110, "protein": 8, "carbs": 12, "fat": 2, "diet": "Vegetarian"},
        {"name": "Boiled Egg Whites (3 pcs)", "calories": 60, "protein": 12, "carbs": 1, "fat": 0, "diet": "Non-Vegetarian"},
        {"name": "Vegetable Sticks with Mint Chutney", "calories": 80, "protein": 3, "carbs": 15, "fat": 1, "diet": "Vegetarian"},
        {"name": "Roasted Makhana (Fox Nuts 40g)", "calories": 145, "protein": 4, "carbs": 20, "fat": 3, "diet": "Vegetarian"},
        {"name": "Green Tea with Rusk (1 pc)", "calories": 50, "protein": 2, "carbs": 10, "fat": 0.5, "diet": "Vegetarian"},
        {"name": "Fruit Smoothie (Banana, Curd, no sugar)", "calories": 180, "protein": 8, "carbs": 32, "fat": 2.5, "diet": "Vegetarian"},
        {"name": "Roasted Chana Dal (50g)", "calories": 175, "protein": 10, "carbs": 25, "fat": 3, "diet": "Vegetarian"},
        {"name": "Watermelon (2 cups)", "calories": 90, "protein": 2, "carbs": 22, "fat": 0.5, "diet": "Vegetarian"},
        {"name": "Steamed Corn (1 cup) with Lemon & Pepper", "calories": 135, "protein": 5, "carbs": 28, "fat": 2, "diet": "Vegetarian"},
        {"name": "Whey Protein Shake (1 scoop with water)", "calories": 120, "protein": 24, "carbs": 3, "fat": 1, "diet": "Any"},
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
    body {{font-family: 'Poppins', sans-serif; background:#F0F8F5; color:#333;}}
    .container {{max-width:1100px;margin:auto;background:#fff;padding:30px;border-radius:15px;box-shadow:0 4px 20px rgba(0,0,0,0.1);}}
    h1,h2,h3 {{color:#059669;text-align:center;}}
    .health-badge {{background:#D1FAE5;padding:8px 15px;border-radius:20px;display:inline-block;margin:5px;font-size:0.85em;}}
    table {{width:100%;border-collapse:collapse;margin-bottom:30px;}}
    th,td {{border:1px solid #ddd;padding:10px;text-align:center;vertical-align:top;}}
    th {{background:#6EE7B7;color:#065F46;}}
    tr:nth-child(even){{background:#F0FDF4;}}
    .daily-total {{ background: #D1FAE5; font-weight: bold; font-size: 0.9em; color:#065F46;}}
    .low-fat {{color:#059669; font-weight:600;}}
    .btn-download {{
        display:inline-block;background:#059669;color:#fff;padding:10px 20px;
        border-radius:8px;text-decoration:none;font-weight:bold;margin:10px auto;display:block;width:fit-content;
    }}
    .info-box {{background:#ECFDF5;padding:15px;border-left:4px solid #059669;margin:20px 0;}}
    </style>
    <div class='container'>
        <h1>🥗 Ultra-Healthy Low-Fat South Indian Meal Plan</h1>
        <h2>{name}</h2>
        <div style='text-align:center;margin:20px 0;'>
            <span class='health-badge'><b>BMI:</b> {bmi:.1f} ({bmi_cat})</span>
            <span class='health-badge'><b>Daily Calories:</b> {cal} kcal</span>
            <span class='health-badge'><b>Goal:</b> {goal}</span>
        </div>
        <div class='info-box'>
            <b>✨ Plan Features:</b> All meals are designed with <span class='low-fat'>LOW FAT (2-8g per meal)</span>, 
            high protein, whole grains (millets/brown rice), minimal oil cooking, and authentic South Indian preparations. 
            Perfect for healthy weight management!
        </div>
    """
    for week in plan:
        html += f"<h2>📅 Week {week['week']}</h2><table><tr><th>Day & Daily Totals</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th><th>Snack</th></tr>" 
        for day in week["days"]:
            totals = day['totals']
            
            # Daily Totals Column with fat highlighting
            day_info = f"""
            <td class='daily-total'>
                <b>{day['day']}</b><br>{day['date']}
                <hr style='border-top: 1px solid #10B981; margin: 5px 0;'>
                <b>Total:</b> {totals['calories']} kcal<br>
                Protein: {totals['protein']}g<br>
                Carbs: {totals['carbs']}g<br>
                <span class='low-fat'>Fat: {totals['fat']}g</span>
            </td>
            """
            
            html += f"<tr>{day_info}"
            for meal in ["breakfast", "lunch", "dinner", "snack"]:
                m = day['meals'][meal]
                html += f"<td><b>{m['name']}</b><br><small>{m['calories']} kcal | P: {m['protein']}g | C: {m['carbs']}g | <span class='low-fat'>F: {m['fat']}g</span></small></td>"
            html += "</tr>"
        html += "</table>"
    html += """<a class='btn-download' href='javascript:void(0)' onclick="window.print()">📥 Download Meal Plan (PDF)</a></div>"""
    return html

# --------------------------
# Gradio Interface
# --------------------------
iface = gr.Interface(
    fn=generate_meal_plan,
    inputs=[
        gr.Textbox(label="Name", placeholder="Enter your name"),
        gr.Number(label="Age", precision=0, minimum=10, maximum=100),
        gr.Radio(["Male", "Female"], label="Gender"),
        gr.Number(label="Height (cm)", minimum=100, maximum=250),
        gr.Number(label="Weight (kg)", minimum=30, maximum=200),
        gr.Radio(["Sedentary","Lightly Active","Moderately Active","Very Active","Extremely Active"], label="Activity Level"),
        gr.Radio(["Vegetarian","Non-Vegetarian","Any"], label="Diet Preference"),
        gr.Radio(["Lose Weight","Gain Muscle","Maintain Weight"], label="Goal")
    ],
    outputs=gr.HTML(label="Your Personalized 4-Week Healthy Meal Plan"),
    title="🌿 Ultra-Healthy South Indian Meal Planner",
    description="Generate a 4-week **low-fat, high-protein** South Indian meal plan with authentic healthy preparations. All meals feature minimal oil, whole grains, and lean proteins.",
    theme="soft"
)

if __name__ == "__main__":
    iface.launch()
