import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect('postgresql://postgres.aoddcnsgkkowtbktnske:users123456.@aws-1-eu-north-1.pooler.supabase.com:6543/postgres')

#CREATE THE TABLE
def create_users_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    IP BOOLEAN DEFAULT FALSE,
    banned BOOLEAN DEFAULT FALSE,
    date TEXT DEFAULT 'N/A'
);
            """)
            conn.commit()

#GET A USER INFO 
def get_user_info(user_id, col):
    allowed_columns = {"id","banned", "date","IP"}
    if col not in allowed_columns:
        raise ValueError("Invalid column name")
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = f"SELECT {col} FROM users WHERE id = %s"
            cur.execute(query, (user_id,))
            result = cur.fetchone()
            return result[0] if result else None

#ADD A USER TO THE DATABASE
def add_user(user):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (id)
                VALUES (%s)
                ON CONFLICT (id) DO NOTHING
            """, (user.id,))
            conn.commit()

#SET USER VALUE
def set_user_value(user_id, col, value):
    allowed_columns = {"banned", "date","IP"}
    if col not in allowed_columns:
        raise ValueError("Invalid column name")
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = f"UPDATE users SET {col} = %s WHERE id = %s"
            cur.execute(query, (value, user_id))
        conn.commit()

#COUNT USERS
def get_user_count():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
            return count
        
#CHECK IF USER IN THE DATABASE
def user_exists(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
            return cur.fetchone() is not None
        

