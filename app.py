from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime


app = Flask(__name__)

# ======================
# DATABASE SETUP
# ======================
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ======================
# ROUTES
# ======================

# HOMEPAGE
@app.route('/')
def homepage():
    return render_template("homepage.html")


# FEATURES PAGE
@app.route('/features')
def features():
    return render_template("features.html")


# SCRAPE TOOL PAGE
@app.route('/scrapetool')
def scrapetool():
    return render_template("scrapetool.html")


# CONTACT PAGE
@app.route('/contact')
def contact():
    return render_template("contact.html")


# SIGNUP PAGE
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username,password) VALUES (?,?)",
                  (username, password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# LOGIN PAGE
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD (SCRAPER)

@app.route('/dashboard')
def dashboard():

    files = []

    # get all csv files
    for file in os.listdir():
        if file.endswith(".csv"):
            files.append(file)

    return render_template("dashboard.html", files=files)



@app.route('/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(debug=True)
