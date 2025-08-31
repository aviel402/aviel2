from flask import Flask, request
import text
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def flask_controller():
    all = request.form if request.form else request.args
    response_str = B(all)
    return Response(response_str, mimetype='text/plain; charset=UTF-8')

def B(all):
    typ=all.get("typ", "1")
    if typ == "1":
        return text.b(all)
    return "t- הגדר נתיב"