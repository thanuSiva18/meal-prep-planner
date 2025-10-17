High-Protein South Indian Meal Planner
A Gradio web app that generates a 4‑week, high‑protein, South Indian–style meal plan personalized by BMI, TDEE, activity level, goal, and diet preference, with daily macro totals per day and minimal repetition across weeks.​

Features
BMI calculation and category labeling, plus gender‑specific BMR and activity‑based TDEE.​

Goals: Lose Weight (−15%), Maintain, Gain Muscle (+10%) applied to daily calories.​

Diet filter: Any, Vegetarian, Non‑Vegetarian; safe fallback if a category would be empty.​

4‑week plan with weekly shuffled pools to reduce repetition across breakfast, lunch, dinner, and snacks.​

Daily totals (calories, protein, carbs, fat) displayed with each day’s meals.​

Tech stack
Python with Gradio for the web UI and HTML rendering.​

pandas, numpy, matplotlib listed in requirements for environment completeness.​

Project structure
text
.
├── app.py              # Dataset, BMI/TDEE logic, plan generator, HTML renderer
└── requirements.txt    # gradio, pandas, numpy, matplotlib
Installation
Create a virtual environment and install dependencies:

python -m venv .venv && source .venv/bin/activate (macOS/Linux)​

py -m venv .venv && .venv\Scripts\activate (Windows)​

pip install -r requirements.txt​

Running locally
Ensure the app exposes a Gradio Interface bound to the function generate_meal_plan(...) returning the HTML from create_html(...), then launch it.​

If not present yet, append this pattern to the bottom of app.py:

Define input components for: name, age, gender, height (cm), weight (kg), activity level, diet preference, goal.​

Map them to generate_meal_plan and call launch().​

Start:

python app.py and open the local URL (typically http://127.0.0.1:7860).[11]

Usage
Provide inputs: Name, Age, Gender, Height (cm), Weight (kg), Activity Level, Diet Preference, Goal.​

Click generate to produce a 4‑week schedule that starts from the current week’s Monday.​

Review daily totals and selected meals for breakfast, lunch, dinner, and snack for each day.​

Data and assumptions
Meals are curated high‑protein South Indian options with approximate per‑serving macros for planning purposes.​

Activity multipliers: Sedentary 1.2, Lightly Active 1.375, Moderately Active 1.55, Very Active 1.725, Extremely Active 1.9.​

Goal multipliers: Lose 0.85×TDEE, Maintain 1.0×TDEE, Gain 1.1×TDEE.​

Known limitations
The create_html snippet needs proper Markdown table assembly: ensure header row, separator row, and rows are fully formatted and concatenated correctly for Gradio to render tables.​

Ensure a proper Gradio Interface and launch() call exist; otherwise the app won’t serve a UI.​

Macro values are estimates and not medical advice.​

Troubleshooting
Blank page or no server:

Wrap the launch() call in if __name__ == "__main__": and ensure there are no import‑time errors.​

Table not rendering:

Verify Markdown table syntax and that each row has matching columns; avoid partial f‑strings or missing separators.​

Too many repeats:

Increase variety by extending each category’s weekly pool beyond 7 before slicing and adjust shuffle/seeding as needed.​

Extending
Add export to CSV/PDF of plans, portion scaling to hit target calories, micronutrient constraints, and user‑defined exclusions (e.g., allergens).​

License
No license granted. All rights reserved. Viewing the source does not grant permission to use, copy, modify, or distribute this code.​

© 2025 Your Name. All rights reserved.