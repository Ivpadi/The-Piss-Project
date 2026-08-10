from db_connection import get_connection
from LiquorLand_Scraper import get_products, clean_products

products = get_products()

cleaned = clean_products(products)

try:
    with get_connection() as conn:

        with conn.cursor() as cur:

            for product in cleaned:


                cur.execute("""INSERT INTO product(name, brand, category, container_type, pack_size, volume_ml, abv, standard_drinks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", product["raw_name"], product["brand"], product["category"], product["container_type"], product["pack_size"], product["volume_ml"], product["abv"], product["standard_drinks"])

                cur.execute("""INSERT INTO """)

            db_version = cur.fetchone()
            print(f"Connected to PostgreSQL! Version: {db_version[0]}")


except Exception as e:
    print(f"Database connection failed: {e}")