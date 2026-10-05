# FitForge – AI-Powered Personal Fitness & Lifestyle Planner

FitForge is a full-stack health, fitness, and lifestyle management platform built with Python, FastAPI, Pandas, NumPy, Matplotlib, SQLite, and modern responsive web technologies. It provides personalized fitness targets, customized training splits, macronutrient meal planning, stress management advice, and habit tracking.

---

## 📸 Key Features

- **Personalized Fitness Engine:** Calculates BMI, BMR (Miffin-St Jeor), TDEE, and safe daily calorie/macro targets based on fitness goals.
- **Custom Workout Split Generator:** Automatically constructs Push/Pull/Legs, Upper/Lower, Full Body, or Home Bodyweight splits based on equipment and available training days.
- **Pandas Nutrition Planner:** Utilizes Pandas boolean indexing to filter food datasets (`foods.csv`) and assemble daily meal plans according to dietary preferences (Vegetarian, Vegan, Non-Veg).
- **Matplotlib Analytics:** Dynamically renders dark-themed progress charts for step history and sleep trends.
- **Daily Activity & Productivity Tracker:** Persistent tracking of steps, sleep, water, stress, and daily task checklists using SQLite.
- **Interactive REST API & Docs:** Built on FastAPI with automatic OpenAPI/Swagger documentation at `/docs`.

---

## 🛠️ Tech Stack & Syllabus Coverage

| Domain | Technology / Library | Usage in FitForge |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI + Uvicorn | Asynchronous REST API routing & server |
| **Data Analysis** | Pandas | Loading, filtering, and sampling food datasets; progress analysis |
| **Numerical Processing** | NumPy | Matrix activity multipliers & sample array operations |
| **Data Visualization** | Matplotlib | Generating dark-mode trend charts (`base64` encoded) |
| **Database** | SQLite (`sqlite3`) | Persistent relational database for user profiles & logs |
| **Environment Configuration**| `python-dotenv` | Managing environment variables & external API keys |
| **Frontend UI** | HTML5, CSS3, Vanilla JS | Dark-themed glassmorphism responsive UI |

---

## 📁 Directory Structure

```text
FitForge/
├── backend/
│   ├── main.py                # FastAPI server & REST API endpoints
│   ├── database.py            # SQLite database initialization & connection
│   ├── calculations.py        # Core fitness formulas (BMI, BMR, TDEE, Macros)
│   ├── workout_generator.py   # Exercise split selection & routine generator
│   ├── nutrition.py           # Pandas-based meal planning engine
│   └── tracker.py             # Activity log handler & Matplotlib chart renderer
├── frontend/
│   ├── index.html             # Landing page & 5-step onboarding modal
│   ├── dashboard.html         # User fitness dashboard & workspace
│   ├── css/
│   │   └── style.css          # Dark fitness styling system
│   └── js/
│       └── dashboard.js       # Client-side API fetch logic
├── data/
│   └── foods.csv              # Nutrition dataset
├── .env                       # Environment variables (API Keys)
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation