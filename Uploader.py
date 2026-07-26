from db_connection import get_connection


try:
    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("SELECT version();")

            db_version = cur.fetchone()
            print(f"Connected to PostgreSQL! Version: {db_version[0]}")


except Exception as e:
    print(f"Database connection failed: {e}")