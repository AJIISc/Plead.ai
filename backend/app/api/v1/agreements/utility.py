from app.api.v1.agreements.constant import DB_QUERIES
from app.db.connection import get_db_connection


def get_user_by_user_id(user_id: str):
    query = DB_QUERIES["get_user_by_user_id"]
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
