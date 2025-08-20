from flask import Flask, request, Response
from urllib.parse import urlencode
import os

# =======================================================
#             חלק A (ה-Controller) עם התיקון המוכח
# =======================================================

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def flask_controller():
    # התיקון הקריטי: מאחד את הנתונים לא משנה אם הגיעו ב-POST או ב-GET
    all_params = request.form if request.method == 'POST' else request.args
    
    final_response_string = yemot_service(all_params)
    return Response(final_response_string, mimetype='text/plain; charset=UTF-8')


# =======================================================
#             חלק B (המנתב - Router)
# =======================================================
def yemot_service(request_params):
    x = request_params.get("x")
    if x == "1":
        # קוראים לפונקציית המחשבון
        return a(request_params)
    return "id_list_message=t-פעולה לא מוגדרת"


# =======================================================
#        חלק C ('a') - המחשבון הרב-שלבי, גרסה סופית
# =======================================================
def a(params):
    # תומך גם ב-step וגם ב-STEP למקרה חירום
    step = params.get("step", params.get("STEP", "1"))

    # שלב 1: בקשת המספר הראשון
    if step == "1":
        prompt = "t-ברוך הבא למחשבון, אנא הקש את המספר הראשון"
        return_path_params = urlencode({'x': '1', 'step': '2'})
        return f"read={prompt}=num1,,/?{return_path_params}"
        
    # שלב 2: בקשת פעולה
    elif step == "2":
        num1 = params.get("num1")
        prompt = "t-הקש פעולה. 1 חיבור, 2 חיסור, 3 כפל, 4 חילוק, 5 חזקה"
        return_path_params = urlencode({'x': '1', 'step': '3', 'saved_num1': num1})
        return f"read={prompt}=op,,1,1,/?{return_path_params}"

    # שלב 3: בקשת מספר שני
    elif step == "3":
        num1_saved = params.get("saved_num1")
        op_saved = params.get("op")
        prompt = "t-אנא הקש את המספר השני"
        return_path_params = urlencode({'x': '1', 'step': '4', 'saved_num1': num1_saved, 'saved_op': op_saved})
        return f"read={prompt}=num2,,/?{return_path_params}"
        
    # שלב 4: ביצוע החישוב
    elif step == "4":
        a_str, b_str, c_str = params.get("saved_num1"), params.get("saved_op"), params.get("num2")
        d = ""
        try:
            a, b, c = float(a_str), b_str, float(c_str)
            if b == '1': d = a + c
            elif b == '2': d = a - c
            elif b == '3': d = a * c
            elif b == '4': d = "לא ניתן לחלק באפס" if c == 0 else round(a / c, 2)
            elif b == '5': d = a ** c
            else: d = "פעולה לא חוקית"
        except:
            d = "שגיאה בערכים"

        # חוזר להתחלה
        return f"id_list_message=t-התוצאה היא {d}&go_to_folder=/?x=1&step=1"

    return "id_list_message=t-שגיאה לא צפויה במערכת"


# קטע הרצה לשרת כמו Railway
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)