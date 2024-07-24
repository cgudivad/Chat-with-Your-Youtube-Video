import os
from flask import Flask, render_template, request, Response
from http import HTTPStatus
from utils import load, generate

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/load', methods=['POST'])
def load_controller():
    status, data = load(request.form.get('url'))
    if status == 'error':
        return Response(data, status=HTTPStatus.BAD_REQUEST)
    response = Response()
    response.set_cookie('name_space', data)
    return response

@app.route('/generate', methods=['POST'])
def generate_controller():
    prompt = request.form.get('prompt')
    model = request.form.get('model')
    name_space = request.cookies.get('name_space')
    if not name_space:
        return Response("Please load a video first", status=HTTPStatus.BAD_REQUEST)
    return Response(generate(model, name_space, prompt))

if __name__ == '__main__':
    app.run(threaded=True)