# Ecological Footprint – Students Life

A Streamlit dashboard that estimates and visualizes ecological footprint patterns for students.

## What this project does
- Provides a **Live Demo Calculator** for individual students.
- Supports **CSV upload** for college-level sustainability analysis.
- Calculates a `TotalScore` from transport, energy, food, and plastic-use behaviors.
- Shows visual insights like score distribution, year-wise average impact, and a sustainability leaderboard.
- Generates personalized and campus-level recommendations.

## Project structure
- `app.py` – Main Streamlit application.
- `requirements.txt` – Python package dependencies.

## Setup and run
1. Create and activate a virtual environment (recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL shown in terminal (usually `http://localhost:8501`).
5. Project is Live Now ! `http://ecofootprintstud.streamlit.app/`

## CSV notes
For full campus analytics, your CSV should include columns similar to:
- Transport mode
- Laptop/computer usage hours
- AC usage
- Diet type
- Plastic bottle usage
- Reusable bottle usage
- Year of study
- Student name (optional but useful for leaderboard)

The app includes flexible column matching, so slightly different question text can still work.

## Push this project to your GitHub repository
Target repository:
- https://github.com/ARUNULAGAPPAN/Ecological_Footprint_students-life.git

From project root (`sus`), run:

```bash
git init
git add .
git commit -m "Initial commit: ecological footprint dashboard"
git branch -M main
git remote add origin https://github.com/ARUNULAGAPPAN/Ecological_Footprint_students-life.git
git push -u origin main
```

If `origin` already exists, update it:

```bash
git remote set-url origin https://github.com/ARUNULAGAPPAN/Ecological_Footprint_students-life.git
git push -u origin main
```
