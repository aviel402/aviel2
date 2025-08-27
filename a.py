from flask import Flask, request
import text
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def calculator_main():
    all = request.form if request.form else request.args
    response_str = B(all)
    return Response(response_str, mimetype='text/plain; charset=UTF-8')

def B(all):
    typ=all.get("typ", "1")
    if typ == "1":
        retrun text.b(all)
    retrun "t- הגדר נתיב"