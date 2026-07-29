DROP TABLE IF EXISTS store CASCADE;
DROP TABLE IF EXISTS location CASCADE;
DROP TABLE IF EXISTS raw_product CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS product_mapping CASCADE;
DROP TABLE IF EXISTS price_history CASCADE;



CREATE TABLE store(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    website VARCHAR(255) NOT NULL
);
 

CREATE TABLE location(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    store_id INT NOT NULL,
        CONSTRAINT fk_store
            FOREIGN KEY (store_id)
                REFERENCES store(id)
);
 

CREATE TABLE raw_product(
    id SERIAL PRIMARY KEY,
    raw_name VARCHAR(100) NOT NULL,
    product_url VARCHAR(255) UNIQUE NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    store_id INT NOT NULL,
    location_id INT NOT NULL,
    CONSTRAINT fk_raw_product_store
        FOREIGN KEY (store_id)
            REFERENCES store(id),
    CONSTRAINT fk_location
        FOREIGN KEY (location_id)
            REFERENCES location(id)
);
 

CREATE TABLE product(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    container_type VARCHAR(50),
    pack_size INT NOT NULL,
    volume_ml INT NOT NULL,
    abv DECIMAL(4,2),
    standard_drinks DECIMAL(4,2)
);
 

CREATE TABLE product_mapping(
    raw_product_id INT PRIMARY KEY
        REFERENCES raw_product(id),
    product_id INT NOT NULL
        REFERENCES product(id)
);

 



CREATE TABLE price_history(
    id SERIAL PRIMARY KEY,
    price DECIMAL(8,2) NOT NULL,
    scraped_at TIMESTAMP NOT NULL,
    raw_product_id INT NOT NULL
        REFERENCES raw_product(id)
);

