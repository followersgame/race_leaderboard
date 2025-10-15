from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os, re

app = Flask(__name__)
app.secret_key = 'change_this_secret'  # change for production
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Simple admin credentials (change before deploying)
ADMIN_USER = 'admin'
ADMIN_PASS = 'race123'

DAY_FILENAME_RE = re.compile(r'^day(\\d+)\\.csv$')

def list_days():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    days = []
    for f in files:
        m = DAY_FILENAME_RE.match(f)
        if m:
            days.append(int(m.group(1)))
    days.sort()
    return days

def load_day(day):
    path = os.path.join(app.config['UPLOAD_FOLDER'], f'day{day}.csv')
    if not os.path.exists(path):
        return []
    try:
        df = pd.read_csv(path)
        expected = ['rank','username','full_name','finish_time_seconds','finish_time_frames','lane_position','medal']
        for c in expected:
            if c not in df.columns:
                df[c] = ''
        for col in ['rank','finish_time_seconds','finish_time_frames','lane_position']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        data = df.fillna('').to_dict(orient='records')
    except Exception as e:
        print('Error reading CSV:', e)
        data = []
    return data

@app.route('/')
def index():
    days = list_days()
    if days:
        # default to latest day if no query param
        try:
            sel = int(request.args.get('day', days[-1]))
        except:
            sel = days[-1]
    else:
        sel = None
    data = load_day(sel) if sel else []
    return render_template('index.html', data=data, days=days, selected_day=sel)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username','')
        pwd = request.form.get('password','')
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session['logged_in'] = True
            flash('Logged in successfully', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out', 'info')
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET','POST'])
def upload():
    if not session.get('logged_in'):
        flash('Please log in to upload files', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.lower().endswith('.csv'):
            # determine next day number
            days = list_days()
            next_day = max(days) + 1 if days else 1
            save_name = f'day{next_day}.csv'
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], save_name)
            file.save(save_path)
            flash(f'CSV uploaded successfully as {save_name}', 'success')
            return redirect(url_for('index', day=next_day))
        else:
            flash('Please upload a .csv file', 'danger')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
