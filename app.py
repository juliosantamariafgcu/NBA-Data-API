from flask import Flask
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Database connection details
DB_HOST = '127.0.0.1'  # Localhost if running outside Docker; use 'db' if inside Docker
DB_PORT = '5432'       # Local port (through Docker or port-forwarding)
DB_NAME = 'nba_stats'  # Correct PostgreSQL database name
DB_USER = 'nba_user'   # PostgreSQL username
DB_PASSWORD = 'nba_password'  # PostgreSQL password

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

@app.route('/')
def index():
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

if __name__ == '__main__':
    app.run(debug=True)
