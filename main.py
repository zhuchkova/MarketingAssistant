# uvicorn main:app --reload
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import psycopg
from agents.audience_agent import run_audience_agent
from db.audience_repository import save_audience_analysis

def handle_new_profile(conn, profile):
    # 1. run agent
    result = run_audience_agent(profile)

    # 2. save to DB
    save_audience_analysis(conn, profile["id"], result)

    conn.commit()

app = FastAPI()

@app.post("/user-profiles")
def create_profile(profile: dict):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_profiles (
                id, user_id, niche, offer, target_audience, expertise, tone, goal
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            profile["id"],
            profile["user_id"],
            profile["niche"],
            profile["offer"],
            profile["target_audience"],
            profile["expertise"],
            profile["tone"],
            profile["goal"]
        ))

    # trigger agent automatically
    handle_new_profile(conn, profile)

    return {"status": "created + audience analyzed"}