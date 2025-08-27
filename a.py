
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def calculator_main():
    all = request.form if request.form else request.args
    response_str = b(all)
    return Response(response_str, mimetype='text/plain; charset=UTF-8')


def b(all):
    text=all.get(txt)
    text = t- + text
    reteun text