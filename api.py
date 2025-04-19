from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# python -m uvicorn api:app --reload --port 8000

# Allow requests from Flask frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'nba_stats')
DB_USER = os.getenv('POSTGRES_USER', 'nba_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'nba_password')

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
    
@app.get("/get_player_stats")
def get_player_stats(name: str):
    try:
        conn = get_db_connection()
        if not conn:
            return {"error": "Database connection failed."}

        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM player_stats
            WHERE person_name ILIKE %s
            ORDER BY game_date DESC
        """, (f"%{name}%",))

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return {"error": "Player not found"}

        return {
            "player": name,
            "stats": [dict(zip(columns, row)) for row in rows]
        }

    except Exception as e:
        return {"error": str(e)}