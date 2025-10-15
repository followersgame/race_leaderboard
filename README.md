# Race Leaderboard — Multi-day Version (Flask)

## Overview
Each uploaded CSV is saved as a separate day (day1.csv, day2.csv, ...). Visitors can select which day's leaderboard to view and search for players.

## Default admin login (change before deploying)
- username: admin
- password: race123

## CSV expected columns
rank,username,full_name,finish_time_seconds,finish_time_frames,lane_position,medal

## Run locally
1. Create a virtualenv: `python -m venv venv && source venv/bin/activate` (or venv\Scripts\activate on Windows)
2. Install: `pip install -r requirements.txt`
3. Run: `python app.py`
4. Open: http://127.0.0.1:5000

Upload a CSV via /login -> /upload (login required). The uploaded CSVs are saved as `uploads/dayX.csv`.
"# race_leaderboard" 
