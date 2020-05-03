import requests
from pprint import pprint
from cache import cache

EDAMAM_APP_ID = '03c6404c'
EDAMAM_API_KEY = '72e3f10076e3e31e6ec6484762a8bb90'

BASE_URL = "https://api.edamam.com/api/food-database/parser"


def get_nutritional_info(ingredient):
    """
    Given an ingredient, get nutritional info for it with EDAMAM.
    """
    nutrients = cache.get_nutrition(ingredient)
    if nutrients:
        print("Nutritional info for ingredient {} exists in cache".format(ingredient))
        return nutrients

    params = {
        "ingr": ingredient,
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_API_KEY,
        "categoryLabel": "food",
        "category": "generic-foods"
    }

    res = requests.get(BASE_URL, params=params)
    print("Nutrition")
    # results are / 100g
    results = res.json()
    nutrition_facts = results['hints']
    nutrition = nutrition_facts[0] # only get the first item
    nutrients = nutrition.get("food").get("nutrients")
    pprint(nutrients)
    cache.set_nutrition(ingredient, nutrients)
    return nutrients
