from db_connection import get_connection
from LiquorLand_Scraper import get_products, clean_products
from normaliser import normalise, build_product_key


# This method makes the call to the specific methods that normalise the products
# builds a product key, and inserts data into the tables 
def process_item(cur, raw_product, location_id):

    # Normalises the products
    attrs = normalise(raw_product)

    # Uses features to build a key
    product_key = build_product_key(attrs)

    # Inserts raw product into table and returns raw product id for later use
    raw_product_id = upsert_raw_product(cur, attrs, location_id)
     
    return 1

# cur.execute("""INSERT INTO product(name, brand, category, container_type, pack_size, volume_ml, abv, standard_drinks) 
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                     ON CONFLICT (name)
#                     DO UPDATE""", product["raw_name"], product["brand"], product["category"], product["container_type"], product["pack_size"], product["volume_ml"], product["abv"], product["standard_drinks"])

#                     cur.execute("""INSERT INTO """)


def main():

    # Get products from scraper - will change later iterate through scrapers
    raw_products = get_products()

    # Sets up a connection and iterates through each raw product and processes and stores them in the database.
    try:
        with get_connection() as conn:

            with conn.cursor() as cur:

                for raw_product in raw_products:

                    try:
                        # Process item will call other methods to touch up info and insert into database
                        process_item(cur, raw_product, location_id=1)

                    except Exception as e:
                        print(f"Failed on item: {e}")
                        conn.rollback()
                        continue
                # Committing after each product so that the next product can check an updated db for duplicates
                conn.commit()

    except Exception as e:
        print(f"Database connection failed: {e}")