import re

text1 = "Haagen Lager can 440ml"
text2 = "15 pack of Cans 330ml"



def get_container(description):

    bottle = re.compile(r"\bbottle\b", re.IGNORECASE)
    bottles = re.compile(r"\bbottles\b", re.IGNORECASE)

    can = re.compile(r"\bcan\b", re.IGNORECASE)
    cans = re.compile(r"\bcans\b", re.IGNORECASE)

    if re.search(bottle, description):
        return "bottle"

    elif re.search(bottles, description):
        return "bottles"

    elif re.search(can, description):
        return "can"

    elif re.search(cans, description):
            return "cans"

    return "Not Found"


def get_size(description):

    sizes = ["4", "6", "10", "12", "15", "18", "24"]

    for each, size in enumerate(sizes):
        count = re.compile(rf"\b{size}\b")

        if re.search(count, description):
            return size

    if get_container(description) == "can" or get_container(description) == "bottle":
        return "1"



def get_ml(description):

    mls = re.compile(r"\d+ml")

    match = re.search(mls, description)

    if match:

        value = match.group(0)

        return value


def processing_for_standards(abv, ml):

    if not abv or ml:
        return -1, -1

    clean_abv = abv.replace("%", "")

    clean_abv = float(clean_abv) / 100

    clean_ml = ml.replace("ml", "")

    return clean_abv, float(clean_ml)



def get_standards(abv, ml):

    if abv == "Not Available":
        return "No Info Available"

    clean_abv, clean_ml = processing_for_standards(abv, ml)

    if clean_ml or clean_abv == -1:
        return "No Info Available"

    standards = clean_ml * clean_abv * 0.789 / 10

    return round(standards, 1)



# test = get_standards("5.0%", "330ml")
# print(test)