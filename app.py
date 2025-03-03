from flask import Flask
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Database connection details
DB_HOST = '127.0.0.1'  # Local port forwarded through SSH tunnel
DB_PORT = '5432'       # Local port (through SSH tunnel)
DB_NAME = 'nba_stats_db'  # Your PostgreSQL database name
DB_USER = 'postgres'      # The user you set for PostgreSQL (e.g., 'postgres')
DB_PASSWORD = 'mysecretpassword'  # Replace with the password you configured

# Establish the connection
def get_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM your_table_name')  # Replace with your table query
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return str(rows)

if __name__ == '__main__':
    app.run(debug=True)