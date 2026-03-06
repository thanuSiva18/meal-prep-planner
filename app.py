import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import re

# --------------------------------------
# LOAD MEALS FROM CSV DATABASE
# --------------------------------------
def load_meals_from_csv():
    """Load meal data from CSV file and group by meal_type."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "..", "meal_data.csv")

    if not os.path.exists(csv_path):
        csv_path = os.path.join(script_dir, "meal_data.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            "meal_data.csv not found. Place it in the project root or meal-prep-planner directory."
        )

    df = pd.read_csv(csv_path)

    required_cols = {"meal_type", "name", "calories", "protein", "carbs", "fat", "diet"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    df["meal_type"] = df["meal_type"].str.strip().str.lower()
    df["diet"] = df["diet"].str.strip()
    df["name"] = df["name"].str.strip()
    df["cuisine"] = df["cuisine"].str.strip() if "cuisine" in df.columns else "Indian"

    for col in ["calories", "protein", "carbs", "fat"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    meals = {}
    for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
        subset = df[df["meal_type"] == meal_type]
        meals[meal_type] = subset.to_dict("records")

    meals = {k: v for k, v in meals.items() if v}

    if not meals:
        raise ValueError("No valid meals found in CSV after parsing.")

    total = sum(len(v) for v in meals.values())
    print(f"✅ Loaded {total} meals from CSV: " + ", ".join(f"{k}={len(v)}" for k, v in meals.items()))
    return meals


try:
    meals = load_meals_from_csv()
except Exception as e:
    print(f"❌ Error loading meal data: {e}")
    meals = {}


# --------------------------------------
# SMART SERVING SIZE ESTIMATOR
# --------------------------------------
SERVING_RULES = [
    # Non-veg proteins
    (r"chicken breast|grilled chicken", lambda cal: f"{int(cal * 0.35)}g chicken breast"),
    (r"chicken tikka|tandoori chicken|chicken lollipop", lambda cal: f"{int(cal * 0.30)}g chicken"),
    (r"chicken curry|chicken korma|chicken masala|chicken saagwala|chicken stew|chicken biryani|butter chicken|kadai chicken|chicken shashlik|chicken shorba|chicken soup", lambda cal: f"{int(cal * 0.30)}g chicken + {int(cal * 0.15)}g gravy"),
    (r"keema|minced meat", lambda cal: f"{int(cal * 0.30)}g minced meat + 1 pav"),
    (r"fish|salmon|grilled fish", lambda cal: f"{int(cal * 0.35)}g fish fillet"),
    (r"prawn|prawns", lambda cal: f"{int(cal * 0.30)}g prawns (8-10 pcs)"),
    (r"egg salad|egg white|masala omelette wrap", lambda cal: f"2-3 eggs + {int(cal * 0.10)}g bread"),
    (r"masala omelette|omelette roll|omelette", lambda cal: "2-3 eggs"),

    # Paneer
    (r"paneer tikka|paneer bhurji", lambda cal: f"{int(cal * 0.35)}g paneer"),
    (r"paneer butter|paneer masala|paneer makhani|kadai paneer|palak paneer|matar paneer|paneer paratha|saag paneer", lambda cal: f"{int(cal * 0.30)}g paneer + {int(cal * 0.12)}g gravy"),
    (r"tofu", lambda cal: f"{int(cal * 0.35)}g tofu"),

    # Rice / biryani dishes
    (r"biryani|pulao|vegetable pulao", lambda cal: f"{int(cal * 0.40)}g cooked rice + {int(cal * 0.15)}g veggies"),
    (r"khichdi|rice and dal", lambda cal: f"{int(cal * 0.35)}g cooked khichdi (1 bowl)"),
    (r"lemon rice", lambda cal: f"{int(cal * 0.40)}g cooked rice"),

    # Dal / lentils
    (r"dal tadka|dal fry|dal makhani|dal palak|dal shorba|masoor dal|coconut dal|toor dal|lentil soup|coconut curry lentil", lambda cal: f"1 bowl ({int(cal * 0.40)}g)"),
    (r"chana masala|chana dal|chole|rajma", lambda cal: f"1 bowl ({int(cal * 0.40)}g)"),
    (r"sambar", lambda cal: f"1 large bowl ({int(cal * 0.45)}g)"),
    (r"rasam", lambda cal: f"1 large bowl ({int(cal * 0.50)}g)"),

    # Curries
    (r"peanut curry|green gram curry|mung bean|moong dal curry|moong sprout|pumpkin curry|vegetable curry|mixed vegetable|coconut curry|vegetable stew|cabbage curry|corn curry|bhindi masala|karela|tinda|gajar matar|ridge gourd", lambda cal: f"1 bowl ({int(cal * 0.40)}g) + 1 roti"),
    (r"pav bhaji", lambda cal: "1 bowl bhaji + 2 pav"),
    (r"veg hakka noodles", lambda cal: f"1 plate ({int(cal * 0.50)}g)"),
    (r"vegetable chili", lambda cal: f"1 bowl ({int(cal * 0.40)}g)"),
    (r"vegetable soup|spinach soup|tomato soup|lemon coriander soup|beetroot soup|tangy tomato soup", lambda cal: f"1 large bowl ({int(cal * 0.55)}g)"),
    (r"kadhi", lambda cal: "1 bowl + 1 roti"),

    # Breakfast items
    (r"idli", lambda cal: "3-4 pcs + chutney"),
    (r"dosa|rava dosa|pesarattu", lambda cal: "2 pcs + chutney"),
    (r"upma|vegetable upma|oats upma|vermicelli upma|vegetable oats upma", lambda cal: f"1 bowl ({int(cal * 0.45)}g)"),
    (r"poha", lambda cal: f"1 plate ({int(cal * 0.45)}g)"),
    (r"paratha|aloo paratha", lambda cal: "2 pcs + curd"),
    (r"besan chilla|cheela", lambda cal: "2-3 pcs + chutney"),
    (r"dalia|broken wheat porridge", lambda cal: f"1 bowl ({int(cal * 0.45)}g)"),
    (r"ragi porridge|millet porridge", lambda cal: f"1 bowl ({int(cal * 0.45)}g)"),
    (r"muesli|quinoa idli", lambda cal: f"1 serving ({int(cal * 0.40)}g)"),
    (r"sweet potato pancake", lambda cal: "2 pcs"),

    # Snacks
    (r"sprout|sundal", lambda cal: f"1 bowl ({int(cal * 0.40)}g)"),
    (r"roasted chickpeas", lambda cal: f"{int(cal * 0.25)}g (1 small bowl)"),
    (r"roasted makhana|fox\s*nut", lambda cal: f"{int(cal * 0.25)}g (1 bowl)"),
    (r"nuts.*seed|mixed nuts|dried fruit", lambda cal: f"{int(cal * 0.12)}g (1 handful)"),
    (r"dhokla|khaman", lambda cal: "3-4 pcs"),
    (r"oatmeal cookies", lambda cal: "3-4 cookies"),
    (r"masala corn", lambda cal: f"1 cup ({int(cal * 0.40)}g)"),
    (r"fruit salad|fruit bowl|papaya salad", lambda cal: f"1 bowl ({int(cal * 0.55)}g)"),
    (r"fruit smoothie|avocado smoothie", lambda cal: "1 glass (250ml)"),
    (r"coconut water", lambda cal: "1 glass (300ml)"),
    (r"raita", lambda cal: f"1 bowl ({int(cal * 0.40)}g)"),
    (r"vegetable salad", lambda cal: f"1 large bowl ({int(cal * 0.55)}g)"),
    (r"vegetable sandwich|egg salad sandwich", lambda cal: "1 sandwich (2 slices)"),
    (r"vegetable cutlet|samosa|baked samosa", lambda cal: "2-3 pcs"),
    (r"carrot.*sticks|cucumber.*sticks|cucumber.*hummus|vegetable sticks|cucumber slices", lambda cal: f"1 bowl sticks + {int(cal * 0.15)}g hummus"),
    (r"carrot laddoo|carrot halwa", lambda cal: "2 pcs"),
    (r"roasted sweet potato", lambda cal: f"{int(cal * 0.45)}g (1 medium)"),
    (r"corn chaat", lambda cal: f"1 bowl ({int(cal * 0.40)}g)"),
    (r"whole wheat pancake", lambda cal: "2 pcs"),
    (r"paneer paratha", lambda cal: "1-2 pcs"),
    (r"besan cookies", lambda cal: "4-5 cookies"),
    (r"lemon coriander soup", lambda cal: "1 bowl"),
    (r"chana dal.*split", lambda cal: f"1 bowl ({int(cal * 0.40)}g)"),
    (r"lettuce wraps|minced chicken", lambda cal: "3-4 wraps"),
    (r"bajra roti|jowar roti|ragi roti|chapati|roti|phulka", lambda cal: "2 pcs"),

    # Catch-all curries & generic
    (r"curry|sabzi|poriyal|masala", lambda cal: f"1 serving ({int(cal * 0.40)}g)"),
]


def estimate_serving_size(meal_name, calories):
    """Estimate a realistic serving size based on meal name and calorie content."""
    name_lower = meal_name.lower()
    for pattern, size_fn in SERVING_RULES:
        if re.search(pattern, name_lower):
            return size_fn(calories)
    # Default fallback based on calorie range
    if calories < 150:
        return "1 small serving"
    elif calories < 300:
        return "1 medium serving"
    else:
        return "1 large serving"


# --------------------------------------
# HEALTH TIPS BY GOAL
# --------------------------------------
HEALTH_TIPS = {
    "Lose Weight": [
        "🥤 Drink a glass of warm water with lemon first thing in the morning",
        "🍽️ Eat slowly — it takes 20 min for your brain to register fullness",
        "🚶 Walk for 15 min after lunch and dinner to aid digestion",
        "🌙 Finish dinner at least 2 hours before bed",
        "🥗 Fill half your plate with vegetables at every meal",
        "☕ Avoid sugary drinks — switch to green tea or buttermilk",
    ],
    "Gain Muscle": [
        "💪 Eat protein within 30 min of your workout",
        "🥚 Aim for 1.6–2.2g protein per kg body weight daily",
        "🍌 Have a banana or dates 30 min before exercise for energy",
        "💧 Drink at least 3–4 liters of water daily",
        "😴 Sleep 7–8 hours — muscles grow during rest",
        "🥛 Add a glass of milk or protein shake as an extra snack",
    ],
    "Maintain Weight": [
        "⚖️ Weigh yourself weekly to stay on track",
        "🍎 Keep healthy snacks ready to avoid junk food temptations",
        "🏃 Stay active — aim for at least 30 min of movement daily",
        "🧘 Practice mindful eating — avoid screens during meals",
        "💧 Drink 2–3 liters of water daily for optimal metabolism",
        "🕐 Try to eat meals at consistent times each day",
    ],
}

MEAL_TIMING = {
    "breakfast": "7:00 – 8:30 AM",
    "snack_morning": "10:30 – 11:00 AM",
    "lunch": "12:30 – 1:30 PM",
    "snack_evening": "4:00 – 5:00 PM",
    "dinner": "7:00 – 8:00 PM",
}


# --------------------------
# Meal Plan Generator
# --------------------------
def generate_meal_plan(name, age, gender, height, weight, activity_level, diet_preference, goal):
    """Calculates TDEE and generates a 4-week meal plan with daily macro totals."""

    # Validate inputs
    if not name or not name.strip():
        return "<div style='color:#DC2626;padding:20px;font-size:1.2em;'>❌ Please enter your name.</div>"
    if not gender:
        return "<div style='color:#DC2626;padding:20px;font-size:1.2em;'>❌ Please select your gender.</div>"
    if not activity_level:
        return "<div style='color:#DC2626;padding:20px;font-size:1.2em;'>❌ Please select your activity level.</div>"
    if not diet_preference:
        return "<div style='color:#DC2626;padding:20px;font-size:1.2em;'>❌ Please select your diet preference.</div>"
    if not goal:
        return "<div style='color:#DC2626;padding:20px;font-size:1.2em;'>❌ Please select your goal.</div>"
    if not meals:
        return "<div style='color:#DC2626;padding:20px;font-size:1.2em;'>❌ Meal database not loaded. Check meal_data.csv.</div>"

    try:
        age = int(age)
        height = float(height)
        weight = float(weight)
    except (TypeError, ValueError):
        return "<div style='color:#DC2626;padding:20px;font-size:1.2em;'>❌ Enter valid numbers for Age, Height, and Weight.</div>"

    if age <= 0 or height <= 0 or weight <= 0:
        return "<div style='color:#DC2626;padding:20px;font-size:1.2em;'>❌ Age, Height, and Weight must be positive.</div>"

    # 1. TDEE Calculation
    bmi = weight / ((height / 100) ** 2)
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    activity_multipliers = {
        "Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55,
        "Very Active": 1.725, "Extremely Active": 1.9,
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)

    # Apply goal multiplier
    if goal == "Lose Weight":
        daily_calories = tdee * 0.85
    elif goal == "Gain Muscle":
        daily_calories = tdee * 1.1
    else:
        daily_calories = tdee

    # BMI category
    if bmi < 18.5:
        bmi_category = "Underweight"
        bmi_color = "#F59E0B"
    elif bmi < 25:
        bmi_category = "Healthy"
        bmi_color = "#10B981"
    elif bmi < 30:
        bmi_category = "Overweight"
        bmi_color = "#F97316"
    else:
        bmi_category = "Obese"
        bmi_color = "#EF4444"

    # Macro targets (in grams)
    if goal == "Gain Muscle":
        protein_target = int(weight * 2.0)
        fat_target = int(daily_calories * 0.25 / 9)
        carb_target = int((daily_calories - protein_target * 4 - fat_target * 9) / 4)
    elif goal == "Lose Weight":
        protein_target = int(weight * 1.8)
        fat_target = int(daily_calories * 0.20 / 9)
        carb_target = int((daily_calories - protein_target * 4 - fat_target * 9) / 4)
    else:
        protein_target = int(weight * 1.2)
        fat_target = int(daily_calories * 0.25 / 9)
        carb_target = int((daily_calories - protein_target * 4 - fat_target * 9) / 4)

    # Water intake (ml)
    water_ml = int(weight * 35)
    water_liters = water_ml / 1000

    # 2. Filter meals by diet preference
    filtered = {}
    for meal_type, meal_list in meals.items():
        if diet_preference == "Any":
            filtered[meal_type] = meal_list.copy()
        elif diet_preference == "Vegetarian":
            filtered[meal_type] = [m for m in meal_list if m["diet"] in ("Vegetarian", "Vegan")]
        else:
            filtered[meal_type] = [m for m in meal_list if m["diet"] == diet_preference]

    for meal_type in meals:
        if meal_type not in filtered or not filtered[meal_type]:
            filtered[meal_type] = meals[meal_type].copy()

    # 3. Generate 4-week plan
    start = datetime.now() - timedelta(days=datetime.now().weekday())
    plan = []
    all_week_totals = []

    for week in range(4):
        week_days = []
        week_cal = []

        weekly_meal_options = {}
        for mtype in filtered:
            options = filtered[mtype].copy()
            random.shuffle(options)
            weekly_meal_options[mtype] = (options * (7 // len(options) + 1))[:7]
            random.shuffle(weekly_meal_options[mtype])

        meal_tracker = {mtype: 0 for mtype in filtered}

        for day in range(7):
            date = start + timedelta(weeks=week, days=day)
            day_meals = {}
            daily_totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

            for mtype in filtered:
                meal_index = meal_tracker[mtype] % len(weekly_meal_options[mtype])
                m = weekly_meal_options[mtype][meal_index]
                # Add serving size
                m_with_serving = m.copy()
                m_with_serving["serving"] = estimate_serving_size(m["name"], m["calories"])
                day_meals[mtype] = m_with_serving

                daily_totals["calories"] += int(m["calories"])
                daily_totals["protein"] += int(m["protein"])
                daily_totals["carbs"] += int(m["carbs"])
                daily_totals["fat"] += int(m["fat"])
                meal_tracker[mtype] += 1

            week_days.append({
                "day": date.strftime("%A"),
                "date": date.strftime("%b %d"),
                "meals": day_meals,
                "totals": daily_totals,
            })
            week_cal.append(daily_totals["calories"])

        plan.append({"week": week + 1, "days": week_days})
        all_week_totals.append(week_cal)

    return create_html(
        name.strip(), age, gender, height, weight, bmi, bmi_category, bmi_color,
        int(daily_calories), int(tdee), int(bmr), goal, diet_preference, activity_level,
        protein_target, carb_target, fat_target, water_liters, plan, all_week_totals,
    )


# --------------------------
# HTML Renderer (Premium)
# --------------------------
def create_html(name, age, gender, height, weight, bmi, bmi_cat, bmi_color,
                cal, tdee, bmr, goal, diet, activity, prot_t, carb_t, fat_t,
                water_l, plan, week_totals):

    tips = HEALTH_TIPS.get(goal, HEALTH_TIPS["Maintain Weight"])
    random.shuffle(tips)
    tips_html = "".join(f"<li>{t}</li>" for t in tips[:4])

    html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * {{ box-sizing: border-box; }}
    .mp {{
        font-family: 'Inter', sans-serif;
        background: #FFFFFF;
        color: #1E293B;
        max-width: 1300px;
        margin: auto;
        padding: 0;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    }}

    /* Header */
    .mp-header {{
        background: linear-gradient(135deg, #059669 0%, #0D9488 50%, #0891B2 100%);
        padding: 35px 40px;
        text-align: center;
    }}
    .mp-header h1 {{ color: #fff; font-size: 2em; margin: 0 0 5px 0; font-weight: 800; letter-spacing: -0.5px; }}
    .mp-header p {{ color: #D1FAE5; margin: 5px 0 0 0; font-size: 1em; font-weight: 300; }}

    /* Body */
    .mp-body {{ padding: 30px; background: #FAFAFA; }}

    /* Stats Grid */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 15px;
        margin-bottom: 25px;
    }}
    .stat-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .stat-card:hover {{ transform: translateY(-3px); border-color: #10B981; box-shadow: 0 4px 12px rgba(16,185,129,0.12); }}
    .stat-label {{ font-size: 0.75em; color: #64748B; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }}
    .stat-value {{ font-size: 1.5em; font-weight: 700; color: #0F172A; }}
    .stat-sub {{ font-size: 0.7em; color: #94A3B8; margin-top: 2px; }}

    /* Macro Targets */
    .macro-section {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 25px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .macro-section h3 {{ color: #059669; margin: 0 0 15px 0; font-size: 1em; }}
    .macro-bar-wrap {{ margin-bottom: 12px; }}
    .macro-bar-label {{ display: flex; justify-content: space-between; font-size: 0.8em; margin-bottom: 4px; }}
    .macro-bar-label span:first-child {{ color: #334155; }}
    .macro-bar-label span:last-child {{ color: #64748B; }}
    .macro-bar {{ height: 8px; background: #E2E8F0; border-radius: 4px; overflow: hidden; }}
    .macro-bar-fill {{ height: 100%; border-radius: 4px; transition: width 0.5s; }}

    /* Timing & Tips */
    .info-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-bottom: 25px;
    }}
    @media (max-width: 700px) {{ .info-grid {{ grid-template-columns: 1fr; }} }}
    .info-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .info-card h3 {{ color: #059669; margin: 0 0 12px 0; font-size: 1em; }}
    .info-card ul {{ margin: 0; padding-left: 18px; }}
    .info-card li {{ font-size: 0.85em; color: #475569; margin-bottom: 6px; line-height: 1.5; }}
    .timing-item {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #F1F5F9; font-size: 0.85em; }}
    .timing-item:last-child {{ border-bottom: none; }}
    .timing-meal {{ color: #475569; }}
    .timing-time {{ color: #059669; font-weight: 600; }}

    /* Week tables */
    .week-header {{
        color: #059669;
        font-size: 1.3em;
        font-weight: 700;
        margin: 30px 0 15px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #E2E8F0;
    }}
    .mp table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-bottom: 30px;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .mp th {{
        background: linear-gradient(135deg, #059669, #0D9488);
        color: #fff;
        padding: 12px 10px;
        font-size: 0.8em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .mp td {{
        padding: 12px 10px;
        vertical-align: top;
        font-size: 0.82em;
        border-bottom: 1px solid #F1F5F9;
        color: #334155;
        background: #FFFFFF;
    }}
    .mp tr:nth-child(even) td {{ background: #F8FAFC; }}
    .mp tr:hover td {{ background: #ECFDF5; }}

    /* Day column */
    .day-col {{
        background: linear-gradient(135deg, #ECFDF5, #D1FAE5) !important;
        color: #065F46 !important;
        font-weight: 600;
        min-width: 130px;
        text-align: center;
    }}
    .day-col .day-name {{ font-size: 1em; color: #065F46; }}
    .day-col .day-date {{ font-size: 0.8em; color: #059669; margin: 2px 0 8px 0; }}
    .day-col hr {{ border: none; border-top: 1px solid #A7F3D0; margin: 6px 0; }}
    .day-col .day-macro {{ font-size: 0.78em; color: #047857; line-height: 1.6; }}

    /* Meal cell */
    .meal-name {{ font-weight: 600; color: #0F172A; font-size: 0.92em; margin-bottom: 3px; }}
    .meal-serving {{
        display: inline-block;
        background: linear-gradient(135deg, #059669, #0D9488);
        color: #fff;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72em;
        font-weight: 600;
        margin: 3px 0;
    }}
    .meal-macros {{ font-size: 0.72em; color: #64748B; margin-top: 3px; }}
    .meal-cuisine {{
        display: inline-block;
        background: #EFF6FF;
        color: #2563EB;
        padding: 1px 6px;
        border-radius: 6px;
        font-size: 0.65em;
        margin-top: 3px;
        border: 1px solid #DBEAFE;
    }}
    .fat-highlight {{ color: #059669; font-weight: 600; }}

    /* Water */
    .water-badge {{
        display: inline-flex; align-items: center; gap: 6px;
        background: #EFF6FF;
        border: 1px solid #DBEAFE;
        padding: 8px 16px; border-radius: 10px; font-size: 0.85em; color: #1D4ED8;
    }}

    /* Footer */
    .mp-footer {{
        text-align: center;
        padding: 20px;
        border-top: 1px solid #E2E8F0;
        margin-top: 10px;
        background: #FFFFFF;
    }}
    .btn-download {{
        display: inline-block;
        background: linear-gradient(135deg, #059669, #0891B2);
        color: #fff;
        padding: 14px 32px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1em;
        cursor: pointer;
        border: none;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    .btn-download:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(5, 150, 105, 0.3); }}
    </style>

    <div class='mp'>
        <div class='mp-header'>
            <h1>🥗 Your Personalized Meal Plan</h1>
            <p>Hello <b>{name}</b> — here's your customized 4-week Indian meal plan</p>
        </div>

        <div class='mp-body'>
            <!-- Stats -->
            <div class='stats-grid'>
                <div class='stat-card'>
                    <div class='stat-label'>BMI</div>
                    <div class='stat-value' style='color:{bmi_color}'>{bmi:.1f}</div>
                    <div class='stat-sub'>{bmi_cat}</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-label'>Daily Calories</div>
                    <div class='stat-value' style='color:#10B981'>{cal}</div>
                    <div class='stat-sub'>kcal / day</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-label'>BMR</div>
                    <div class='stat-value'>{bmr}</div>
                    <div class='stat-sub'>kcal at rest</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-label'>TDEE</div>
                    <div class='stat-value'>{tdee}</div>
                    <div class='stat-sub'>{activity}</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-label'>Goal</div>
                    <div class='stat-value' style='font-size:1.1em; color:#0F172A;'>{goal}</div>
                    <div class='stat-sub'>{diet}</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-label'>Profile</div>
                    <div class='stat-value' style='font-size:1em;'>{gender}, {age}y</div>
                    <div class='stat-sub'>{height}cm • {weight}kg</div>
                </div>
            </div>

            <!-- Macro Targets -->
            <div class='macro-section'>
                <h3>📊 Daily Macro Targets</h3>
                <div class='macro-bar-wrap'>
                    <div class='macro-bar-label'><span>🥩 Protein</span><span>{prot_t}g / day</span></div>
                    <div class='macro-bar'><div class='macro-bar-fill' style='width:{min(100, int(prot_t/3))}%; background:linear-gradient(90deg,#EF4444,#F97316);'></div></div>
                </div>
                <div class='macro-bar-wrap'>
                    <div class='macro-bar-label'><span>🍚 Carbs</span><span>{carb_t}g / day</span></div>
                    <div class='macro-bar'><div class='macro-bar-fill' style='width:{min(100, int(carb_t/4))}%; background:linear-gradient(90deg,#3B82F6,#8B5CF6);'></div></div>
                </div>
                <div class='macro-bar-wrap'>
                    <div class='macro-bar-label'><span>🧈 Fat</span><span>{fat_t}g / day</span></div>
                    <div class='macro-bar'><div class='macro-bar-fill' style='width:{min(100, int(fat_t/1.5))}%; background:linear-gradient(90deg,#F59E0B,#EAB308);'></div></div>
                </div>
                <div style='margin-top:12px;'>
                    <span class='water-badge'>💧 Daily Water Intake: <b>{water_l:.1f} liters</b> ({int(water_l*1000)} ml)</span>
                </div>
            </div>

            <!-- Timing & Tips -->
            <div class='info-grid'>
                <div class='info-card'>
                    <h3>⏰ Recommended Meal Timing</h3>
                    <div class='timing-item'><span class='timing-meal'>🥣 Breakfast</span><span class='timing-time'>{MEAL_TIMING["breakfast"]}</span></div>
                    <div class='timing-item'><span class='timing-meal'>🍎 Morning Snack</span><span class='timing-time'>{MEAL_TIMING["snack_morning"]}</span></div>
                    <div class='timing-item'><span class='timing-meal'>🍛 Lunch</span><span class='timing-time'>{MEAL_TIMING["lunch"]}</span></div>
                    <div class='timing-item'><span class='timing-meal'>🍵 Evening Snack</span><span class='timing-time'>{MEAL_TIMING["snack_evening"]}</span></div>
                    <div class='timing-item'><span class='timing-meal'>🍲 Dinner</span><span class='timing-time'>{MEAL_TIMING["dinner"]}</span></div>
                </div>
                <div class='info-card'>
                    <h3>💡 Tips for "{goal}"</h3>
                    <ul>{tips_html}</ul>
                </div>
            </div>
    """

    # Week Tables
    meal_type_order = ["breakfast", "lunch", "dinner", "snack"]
    meal_type_headers = {"breakfast": "🥣 Breakfast", "lunch": "🍛 Lunch", "dinner": "🍲 Dinner", "snack": "🍎 Snack"}

    for week in plan:
        avg_cal = int(np.mean(week_totals[week["week"] - 1]))
        html += f"""<div class='week-header'>📅 Week {week['week']} <span style='font-size:0.6em;color:#94A3B8;font-weight:400;'>• Avg {avg_cal} kcal/day</span></div>"""
        html += "<table><tr><th>Day & Totals</th>"
        for mtype in meal_type_order:
            if mtype in week["days"][0]["meals"]:
                html += f"<th>{meal_type_headers.get(mtype, mtype.title())}</th>"
        html += "</tr>"

        for day in week["days"]:
            totals = day["totals"]
            day_info = f"""
            <td class='day-col'>
                <div class='day-name'>{day['day']}</div>
                <div class='day-date'>{day['date']}</div>
                <hr>
                <div class='day-macro'>
                    <b>{totals['calories']} kcal</b><br>
                    P: {totals['protein']}g<br>
                    C: {totals['carbs']}g<br>
                    <span class='fat-highlight'>F: {totals['fat']}g</span>
                </div>
            </td>
            """
            html += f"<tr>{day_info}"
            for mtype in meal_type_order:
                if mtype in day["meals"]:
                    m = day["meals"][mtype]
                    cuisine = m.get("cuisine", "")
                    serving = m.get("serving", "1 serving")
                    cuisine_tag = f"<span class='meal-cuisine'>{cuisine}</span>" if cuisine else ""
                    html += f"""<td>
                        <div class='meal-name'>{m['name']}</div>
                        <div class='meal-serving'>📏 {serving}</div>
                        <div class='meal-macros'>
                            {int(m['calories'])} kcal • P:{int(m['protein'])}g • C:{int(m['carbs'])}g • <span class='fat-highlight'>F:{int(m['fat'])}g</span>
                        </div>
                        {cuisine_tag}
                    </td>"""
            html += "</tr>"
        html += "</table>"

    html += """
        </div>
        <div class='mp-footer'>
            <a class='btn-download' href='javascript:void(0)' onclick="window.print()">📥 Download Meal Plan (PDF)</a>
            <p style='font-size:0.7em;color:#94A3B8;margin-top:10px;'>Generated by AI-Powered Indian Meal Planner • Consult a nutritionist for medical dietary needs</p>
        </div>
    </div>"""
    return html


# --------------------------
# Gradio Interface
# --------------------------
iface = gr.Interface(
    fn=generate_meal_plan,
    inputs=[
        gr.Textbox(label="👤 Name", placeholder="Enter your name"),
        gr.Number(label="🎂 Age", precision=0, minimum=10, maximum=100),
        gr.Radio(["Male", "Female"], label="⚧ Gender"),
        gr.Number(label="📏 Height (cm)", minimum=100, maximum=250),
        gr.Number(label="⚖️ Weight (kg)", minimum=30, maximum=200),
        gr.Radio(
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
            label="🏃 Activity Level",
        ),
        gr.Radio(["Vegetarian", "Non-Vegetarian", "Vegan", "Any"], label="🥗 Diet Preference"),
        gr.Radio(["Lose Weight", "Gain Muscle", "Maintain Weight"], label="🎯 Goal"),
    ],
    outputs=gr.HTML(label="Your Personalized 4-Week Meal Plan"),
    title="🌿 AI-Powered Indian Meal Planner",
    description=(
        "Generate a personalized **4-week Indian meal plan** from 500+ authentic recipes. "
        "Includes **serving sizes**, **macro targets**, **meal timing**, and **health tips** "
        "tailored to your body, activity, and goals."
    ),
    theme="soft",
)

if __name__ == "__main__":
    iface.launch()
