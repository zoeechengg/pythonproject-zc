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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

STATIC_IMAGE_PATH = 'static/uploaded_images'
FILE_UPLOAD_PATH = os.path.join(app.root_path, STATIC_IMAGE_PATH)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/ingredients', methods=['POST'])
def get_ingredients():
    """
    Handler for fetching ingredients + calories per ingredient for an image.

    response looks like
    [
        {
            'ingredient': 'sauce',
            'nutritional_info':
            {
                'ENERC_KCAL': 438.0,
                'PROCNT': 7.68,
                'FAT': 18.33,
                'CHOCDF': 60.52, 'FIBTG': 1.0
            }
        },
        {
            'ingredient': 'spaghetti',
            'nutritional_info':
            {
                'ENERC_KCAL': 371.0,
                'PROCNT': 13.04,
                'FAT': 1.51,
                'CHOCDF': 74.67,
                'FIBTG': 3.2
            }
        }
        ...
    ]
    :return:
    """
    if 'file' not in request.files:
        print('No file part')
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return redirect(url_for('home'))
    print(file.filename)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(FILE_UPLOAD_PATH, filename)
        file.save(file_path)

        ingredients = ingredient_fetcher.get_ingredients_for_local_image(file_path)
        response = [{
            "ingredient": ingredient,
            "nutritional_info": calories_fetcher.get_nutritional_info(ingredient)
        } for ingredient in ingredients]
        cache.persist()
        return render_template('ingredients.html',
                               img_src=os.path.join(STATIC_IMAGE_PATH, filename),
                               response=response)
