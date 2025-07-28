from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import os
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = "wefbiwwuufhh3h87fsjdvhsdidsufuueg3i4grejvig34tigsbgd8g7wy436weragb39299euf2gff"

DB_PATH = "users.db"
ESP32_IP = "192.168.0.38"

# ---------- DB SETUP ----------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                hour INTEGER,
                minute INTEGER
            );
        """)

init_db()

# ---------- AUTH ----------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cur.fetchone()
            if user:
                session["username"] = username
                session["user_id"] = user[0]  # Save ID for login_required
                return redirect(url_for("home"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Username already taken")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for("login"))

# ---------- PAGES ----------
@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

@app.route("/specs")
def specs():
    return render_template("specs.html")

@app.route("/requirements")
def requirements():
    return render_template("requirements.html")

@app.route("/alarm")
@login_required
def alarm_page():
    return render_template("alarm.html")

@app.route("/switch")
@login_required
def switch_control():
    return render_template("switch_control.html")

@app.route("/alarms")
@login_required
def view_alarms():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, hour, minute FROM alarms WHERE user_id = ?", (session["user_id"],))
        alarms = cursor.fetchall()
    return render_template("alarms.html", alarms=alarms)

@app.route("/delete-alarm/<int:alarm_id>", methods=["POST"])
@login_required
def delete_alarm(alarm_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM alarms WHERE id = ? AND user_id = ?", (alarm_id, session["user_id"]))
    flash("Alarm deleted successfully.")
    return redirect(url_for("view_alarms"))

# ---------- ESP32 COMMUNICATION ----------
@app.route("/set-alarm", methods=["POST"])
@login_required
def send_alarm():
    hour = request.form.get("hour")
    minute = request.form.get("minute")
    try:
        r = requests.post(f"http://{ESP32_IP}/alarm", data={"hour": hour, "minute": minute}, timeout=2)

        # Save alarm to database
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO alarms (user_id, hour, minute) VALUES (?, ?, ?)",
                         (session["user_id"], hour, minute))

        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": f"ESP32 not reachable: {str(e)}"})

@app.route("/switch", methods=["POST"])
@login_required
def send_switch():
    action = request.form.get("action")
    try:
        r = requests.post(f"http://{ESP32_IP}/control", data={"action": action}, timeout=2)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": f"ESP32 not reachable: {str(e)}"})

# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get PORT from env or default 5000
    app.run(host="0.0.0.0", port=port)
