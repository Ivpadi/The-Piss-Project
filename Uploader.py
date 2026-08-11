from db_connection import get_connection
from LiquorLand_Scraper import get_products, get_abv
from normaliser import normalise, build_product_key
from extraction_methods import get_standards
from datetime import date, datetime

# This method inserts a raw_product into a table after scraping, if a product is already inserted (after daily scrapes, most will be), then update last_seen date
def upsert_raw_product(cur, attrs, location_id):
    cur.execute("""INSERT INTO raw_product(raw_name, product_url, image_url, last_seen, location_id) 
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (product_url, location_id)
                    DO UPDATE SET last_seen = EXCLUDED.last_seen
                    RETURNING ID""", attrs["raw_name"], attrs["product_url"], attrs["image_url"], date.today(), location_id)
    # Returns product_id for later use
    return cur.fetchone()[0]


# Retrieves product_id if there is already a product_key matching with the raw item that is being inserted in current iteration/loop
def find_product_by_key(cur, product_key):
    cur.execute("""SELECT id FROM product WHERE product_key = %s""", (product_key))
    row = cur.fetchone()

    # Returns None to indicate need for insertion into product
    return row[0] if row else None

# Inserts raw_product(normalised) into product table
def insert_product(cur, attrs, product_key):
    # Calls method to get the abv (retrieved from individual product pages)
    abv = get_abv(attrs["product_url"])
    standards = get_standards(abv, attrs["volume_ml"])
    
    cur.execute("""INSERT INTO product(product_key, name, brand, category, container_type, pack_size, volume_ml, abv, standard_drinks)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id""", product_key, attrs["raw_name"], attrs["brand"], attrs["category"], attrs["container_type"], attrs["pack_size"], attrs["volume_ml"], abv, standards)
    
    # Return newly mapped product_id for later use
    return cur.fetchone()[0]


# Inserts mapping from raw_product to product
def upsert_mapping(cur, raw_product_id, product_id):
    cur.execute("""INSERT INTO product_mapping(raw_product_id, product_id)
                    VALUES (%s, %s)
                    ON CONFLICT (raw_product_id)
                    DO UPDATE SET product_id = EXCLUDED.product_id""", raw_product_id, product_id)


# Inserts price history of scraped products into table
def insert_price_history(cur, attrs, raw_product_id):
    cur.execute("""INSERT INTO price_history(price, scraped_at, raw_product_id)
                    VALUES (%s, %s, %s)
                    """, attrs["price"], datetime.now().strftime("%H:%M %d-%m-%Y"), raw_product_id)


# This method makes the call to the specific methods that normalise the products
# builds a product key, and inserts data into the tables 
def process_item(cur, raw_product, location_id):

    # Normalises the products
    attrs = normalise(raw_product)

    # Uses features to build a key
    product_key = build_product_key(attrs)

    # Inserts raw product into table and returns raw product id for later use
    raw_product_id = upsert_raw_product(cur, attrs, location_id)

    # Check if raw_product has a normalised version already in product, if so, return product_id
    product_id = find_product_by_key(cur, product_key)

    # if not, insert into table
    if product_id is None:
        product_id = insert_product(cur, attrs, product_key)

    # Inserts into mapping table for raw_product to product
    upsert_mapping(cur, raw_product_id, product_id)

    # Inserts into price_history table
    insert_price_history(cur, attrs, raw_product_id)
    


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