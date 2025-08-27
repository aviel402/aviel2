from flask import Flask, request
import text
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def calculator_main():
    all = request.form if request.form else request.args
    response_str = text.b(all)
    return Response(response_str, mimetype='text/plain; charset=UTF-8')
