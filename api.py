from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from dotenv import load_dotenv
from datetime import datetime, timedelta
import psycopg2
import os
import uvicorn

load_dotenv()

app = FastAPI()

# python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000 --ssl-keyfile=server.key --ssl-certfile=server.crt

# Allow requests from Flask frontend (Links Different Ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment configs
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'nba_stats')
DB_USER = os.getenv('POSTGRES_USER', 'nba_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'nba_password')

fake_admin = {
    "username": "admin",
    "password": os.getenv("ADMIN_PASSWORD", "admin")
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload.get("sub") != fake_admin["username"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload

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

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == fake_admin["username"] and form_data.password == fake_admin["password"]:
        token = create_access_token({"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Invalid login")

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

@app.post("/add_player_stat")
def add_stat(data: dict = Body(...), admin=Depends(get_current_admin)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        columns = data.keys()
        values = [data[col] for col in columns]

        insert_query = f"""
            INSERT INTO player_stats ({','.join(columns)})
            VALUES ({','.join(['%s'] * len(values))})
        """
        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Stat added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/update_player_stat")
def update_stat(person_id: int, game_date: str, updates: dict = Body(...), admin=Depends(get_current_admin)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values()) + [person_id, game_date]

        query = f"""
            UPDATE player_stats
            SET {set_clause}
            WHERE person_id = %s AND game_date = %s
        """
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Stat updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete_player_stat")
def delete_stat(person_id: int, game_date: str, admin=Depends(get_current_admin)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM player_stats
            WHERE person_id = %s AND game_date = %s
        """, (person_id, game_date))

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Stat deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="server.key", ssl_certfile="server.crt")
