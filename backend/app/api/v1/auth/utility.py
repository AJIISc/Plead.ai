
from app.db.database import get_db_conn
from app.db.models import User  
import logging
from sqlalchemy.orm import Session
logger = logging.getLogger(__name__)

def get_public_key(user_id):
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT public_key FROM plead_user_information WHERE id = %s
            """,
            (user_id,)
        )
        return cursor.fetchone()


def get_private_key(user_id):
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT private_key FROM plead_user_information WHERE id = %s
            """,
            (user_id,)
        )
        return cursor.fetchone()