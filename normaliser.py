from extraction_methods import get_container, get_size, get_ml, get_standards


# Normalises and derives the needed info to then store into database.
def normalise(product):
    raw_name = product["raw_name"]

    return {
        **product,
        "container_type": get_container(raw_name),
        "pack_size": get_size(raw_name),
        "volume_ml": get_ml(raw_name),
    }

# Builds product key for ease on eyes for debugging/lookup later on
def build_product_key(attributes):
    return f"{attributes["Brand"]} | {attributes["pack_size"]} | {attributes["container_type"]} | {attributes["volume_ml"]}".lower()