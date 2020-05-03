import os

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from werkzeug.utils import secure_filename
from fetchers import ingredient_fetcher
from fetchers import calories_fetcher
from cache import cache

app = Flask(__name__)

STATIC_IMAGE_PATH = 'static/uploaded_images'
FILE_UPLOAD_PATH = os.path.join(app.root_path, STATIC_IMAGE_PATH)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """
    Returns True if the file is an allowed file type.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def render_error(msg):
    """
    Given an error message, renders the error message in the error page.
    """
    return render_template('error.html', msg=msg)

def render_ingredients(food_ingredients, img_src):
    """
    Given a list of ingredients, fetches nutritional information for each ingredient and renders it in the ingredients page.
    """
    response = [{
        "ingredient": ingredient,
        "nutritional_info": calories_fetcher.get_nutritional_info(ingredient)
    } for ingredient in food_ingredients]
    cache.persist()
    return render_template('ingredients.html',
                            img_src=img_src,
                            ingredients=response)

@app.route('/')
def home():
    """
    Renders the home page for Calorify.
    """
    return render_template('home.html')


@app.route('/ingredients', methods=['POST'])
def get_ingredients():
    """
    Handler for fetching ingredients + calories per ingredient for an image.
    """

    img_url = request.form.get('url_upload')
    if img_url:
        ingredients = ingredient_fetcher.get_ingredients_for_url(img_url)
        return render_ingredients(ingredients, img_url)

    if 'file' not in request.files:
        return render_error("No url was entered and no file was selected.")

    file = request.files['file']
    if file.filename == '':
        return render_error("No url was entered and no file was selected.")


    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(FILE_UPLOAD_PATH, filename)
        file.save(file_path)

        ingredients = ingredient_fetcher.get_ingredients_for_local_image(file_path)
        return render_ingredients(ingredients, os.path.join(STATIC_IMAGE_PATH, filename))
    else:
        return render_error("Your file <{}> is an invalid image file.".format(file.filename))