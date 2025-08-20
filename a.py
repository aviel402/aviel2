from flask import Flask, request, Response
from urllib.parse import urlencode
import os

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def calculator_main():
    all_params = request.form if request.form else request.args
    response_str = yemot_service(all_params)
    return Response(response_str, mimetype='text/plain; charset=UTF-8')

def yemot_service(params):
    if params.get("x") == "1":
        return calculator_logic(params)
    return "id_list_message=t-פעולה לא מוגדרת"

def calculator_logic(params):
    step = params.get("step", params.get("STEP", "1"))
    
    if step == "1":
        prompt = "t-ברוך הבא למחשבון, אנא הקש מספר ראשון"
        return_path = urlencode({'x': '1', 'step': '2'})
        return f"read={prompt}=num1,,/?{return_path}"
    
    # ... כאן נמצאת שאר הלוגיקה המצוינת של המחשבון עם השלבים ...
    elif step == "2":
         num1 = params.get("num1")
         prompt = "t-הקש פעולה"
         return_path = urlencode({'x': '1', 'step': '3', 'num1': num1})
         return f"read={prompt}=op,,1,1,/?{return_path}"
    # ... וכו' ...
    else:
         return "id_list_message=t-הגעת לסוף"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)