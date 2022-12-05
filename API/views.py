from app import app
from flask import request, jsonify
from service.utils import google_crawler, naver_crawler


@app.route('/')
def hello_flask():
    return 'Hello Flask'


@app.route('/search', method=['GET'])
def search_word():
    try:
        word = request.args['word']
    except Exception as ex:
        return jsonify(ex)

    google_img_url = google_crawler(word)
    naver_img_url = naver_crawler(word)

    return True
