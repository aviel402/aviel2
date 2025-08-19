
from flask import Flask, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # הקוד הכי פשוט בעולם. רק מחזיר הודעת הצלחה.
    response_string = "id_list_message=t-הצלחה. התקשורת עובדת&go_to_folder=hangup"
    return response_string, 200, {'Content-Type': 'text/plain; charset=utf-8'}