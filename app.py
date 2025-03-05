from flask import Flask, render_template
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database connection details
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')  # Default to localhost if not found
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'nba_stats')
DB_USER = os.getenv('POSTGRES_USER', 'nba_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'nba_password')

# Establish the connection
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
    
@app.route('/compare')
def compare():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM player_stats LIMIT 10;')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return str(rows)
    else:
        return "Failed to connect to the database."

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        return render_template("index.html")
    else:
        return "Failed to connect to the database."
    

if __name__ == '__main__':
    app.run(debug=True)
