import requests
from pprint import pprint
from cache import cache

EDAMAM_APP_ID = '03c6404c'
EDAMAM_API_KEY = '72e3f10076e3e31e6ec6484762a8bb90'

BASE_URL = "https://api.edamam.com/api/food-database/parser"


def get_nutritional_info(ingredient):
    """
    Gets nutritional info for an ingredient. Example response res.json()['hints'] looks like
    {   'food': {   'category': 'Generic foods',
                                 'categoryLabel': 'food',
                                 'foodId': 'food_a8hs60uayl5icia1qe8qoba1kwp8',
                                 'label': 'spaghetti',
                                 'nutrients': {   'CHOCDF': 74.67,
                                                  'ENERC_KCAL': 371.0,
                                                  'FAT': 1.51,
                                                  'FIBTG': 3.2,
                                                  'PROCNT': 13.04}},
                     'measures': [   {   'label': 'Whole',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_unit'},
                                     {   'label': 'Serving',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_serving'},
                                     {   'label': 'Noodle',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_noodle'},
                                     {   'label': 'Sheet',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_sheet'},
                                     {   'label': 'Strip',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_strip'},
                                     {   'label': 'Shell',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_shell'},
                                     {   'label': 'Tube',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_tube'},
                                     {   'label': 'Box',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_box'},
                                     {   'label': 'Package',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_package'},
                                     {   'label': 'Packet',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_packet'},
                                     {   'label': 'Gram',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_gram'},
                                     {   'label': 'Ounce',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_ounce'},
                                     {   'label': 'Pound',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_pound'},
                                     {   'label': 'Kilogram',
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_kilogram'},
                                     {   'label': 'Cup',
                                         'qualified': [   [   {   'label': 'shaped',
                                                                  'uri': 'http://www.edamam.com/ontologies/edamam.owl#Qualifier_shaped'}]],
                                         'uri': 'http://www.edamam.com/ontologies/edamam.owl#Measure_cup'}]},
    :param ingredient:
    :return: nutrients, e.g. {   'CHOCDF': 74.67,
                                  'ENERC_KCAL': 371.0,
                                  'FAT': 1.51,
                                  'FIBTG': 3.2,
                                  'PROCNT': 13.04}
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
