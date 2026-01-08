import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "databases", "database.db")

# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- ROUTE ----------
@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        if name:
            conn.execute(
                "INSERT INTO users (name) VALUES (?)",
                (name,)
            )
            conn.commit()
        return redirect(url_for("home"))

    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    return render_template("index.html", users=users)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run()
