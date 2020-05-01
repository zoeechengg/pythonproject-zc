from cache import cache

from clarifai.rest import ClarifaiApp

PRED_LOWER_BOUND = 0.9

cl_app = ClarifaiApp(api_key="16601175d1524051af38960d9c4f9145")
model = cl_app.models.get(model_id="bd367be194cf45149e75f01d59f77ba7")


def get_ingredients_for_local_image(file_path):
    response = cache.get_prediction(file_path)
    if response:
        print("Prediction for image {} exists in cache".format(file_path))
        return response

    response = model.predict_by_filename(file_path, min_value=PRED_LOWER_BOUND)
    ingredients = []
    try:
        concepts = response['outputs'][0]['data']['concepts']  # clarifai API predictions of what's in the image.
        ingredients = [concept['name'] for concept in concepts]
        cache.set_prediction(file_path, ingredients)
    except Exception as e:
        print(e)

    return ingredients

def get_ingredients_for_url(url):
    response = cache.get_prediction(url)
    if response:
        print("Prediction for image {} exists in cache".format(url))
        return response

    response = model.predict_by_url(url, min_value=PRED_LOWER_BOUND)
    ingredients = []
    try:
        concepts = response['outputs'][0]['data']['concepts']  # clarifai API predictions of what's in the image.
        ingredients = [concept['name'] for concept in concepts]
        cache.set_prediction(url, ingredients)
    except Exception as e:
        print(e)

    return ingredients