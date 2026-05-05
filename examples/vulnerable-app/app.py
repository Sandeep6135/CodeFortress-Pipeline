import sqlite3
from flask import Flask, request

app = Flask(__name__)

# INTENTIONAL VULNERABILITY 1: Hardcoded Secret (For TruffleHog to catch)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)''')
    c.execute("INSERT OR IGNORE INTO users (id, username, role) VALUES (1, 'admin', 'superuser')")
    conn.commit()
    conn.close()

@app.route('/user')
def get_user():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # INTENTIONAL VULNERABILITY 2: SQL Injection (For SonarQube/ZAP to catch)
    # Using string formatting instead of parameterized queries
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    return f"User details: {user}" if user else "User not found."

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)