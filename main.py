from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# スコアデータのモデル
class Score(BaseModel):
    username: str
    score: int

# データベースの初期化
def init_db():
    conn = sqlite3.connect("scores.db")  # SQLite3のデータベースファイル
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 初回実行時にDBを作成
init_db()

# スコアを保存するAPI
@app.post("/submit_score/")
async def submit_score(score_data: Score):
    try:
        conn = sqlite3.connect("scores.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO scores (username, score) VALUES (?, ?)", 
                    (score_data.username, score_data.score))
        conn.commit()
        conn.close()
        return {"message": "Score submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ランキング取得API
@app.get("/leaderboard/")
async def get_leaderboard():
    try:
        conn = sqlite3.connect("scores.db")
        cur = conn.cursor()
        cur.execute("SELECT username, score FROM scores ORDER BY score DESC LIMIT 10")
        data = cur.fetchall()
        conn.close()
        return {"leaderboard": [{"username": row[0], "score": row[1]} for row in data]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))