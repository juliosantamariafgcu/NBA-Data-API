from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Allow requests from Flask frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
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
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                season_year,
                team_tricode,
                ROUND(AVG(points), 1) AS ppg,
                ROUND(AVG(rebounds_total), 1) AS rpg,
                ROUND(AVG(assists), 1) AS apg,
                ROUND(AVG(field_goals_percentage) * 100, 1) AS fg_pct,
                ROUND(AVG(three_pointers_percentage) * 100, 1) AS three_pt_pct
            FROM player_stats
            WHERE LOWER(person_name) = LOWER(%s)
            GROUP BY season_year, team_tricode
            ORDER BY season_year DESC
        """, (name,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return {"error": "Player not found"}

        return {
            "player": name,
            "stats": [
                {
                    "season": row[0],
                    "team": row[1],
                    "ppg": row[2],
                    "rpg": row[3],
                    "apg": row[4],
                    "fg_pct": row[5],
                    "three_pt_pct": row[6]
                }
                for row in rows
            ]
        }
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == '__main__':
    app.run(debug=True)
