from flask import Flask, request, Response
from urllib.parse import urlencode
import random
import os

# =======================================================
#             חלק A (ה-Controller המתוקן)
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
        return a_calculator(request_params) # קריאה למחשבון
    elif x == "2":
        return b_rock_paper_scissors(request_params) # קריאה לאבן, נייר ומספריים
    elif x == "3":
        return c_lottery(request_params) # קריאה למשחק ההגרלות
    
    return "id_list_message=t-פעולה לא מוגדרת"


# =======================================================
#        חלק C-1 (פונקציה 'a') - מחשבון רב-שלבי
# =======================================================
def a_calculator(params):
    step = params.get("step", params.get("STEP", "1"))

    # שלב 1: בקשת המספר הראשון
    if step == "1":
        prompt = "t-ברוך הבא למחשבון, אנא הקש את המספר הראשון"
        return_path_params = urlencode({'x': '1', 'step': '2'})
        return f"read={prompt}=num1,,/?{return_path_params}"
        
    # שלב 2: בקשת פעולה
    elif step == "2":
        num1 = params.get("num1")
        prompt = "t-אנא הקישו פעולה, לחיבור הקישו 1, לחיסור הקישו 2 ,לכפל הקישו 3, לחילוק הקישו 4, לחזקה הקישו 5"
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

        return f"id_list_message=t-התוצאה היא,  {d}"

    return "id_list_message=t-שגיאה לא צפויה במערכת"


# =======================================================
#        חלק C-2 (פונקציה 'b') - אבן, נייר ומספריים
# =======================================================
def b_rock_paper_scissors(params):
    step = params.get("step", "1")

    # שלב 1: בקשת בחירה
    if step == "1":
        prompt = "t-ברוך הבא לאבן נייר ומספריים. אנא בחר, 1 אבן, 2 נייר, 3 מספריים"
        return_path = f"/?x=2&step=2"
        return f"read={prompt}=choice,,1,1,{return_path}"

    # שלב 2: חישוב תוצאה
    elif step == "2":
        user_choice = params.get("choice")
        if not user_choice or user_choice not in ["1", "2", "3"]:
            return "id_list_message=t-בחירה לא חוקית.&go_to_folder=/?x=2&step=1"
        
        computer_choice = str(random.randint(1, 3))
        options = {"1": "אבן", "2": "נייר", "3": "מספריים"}
        user_text, computer_text = options[user_choice], options[computer_choice]
        
        if user_choice == computer_choice: result_text = "תיקו"
        elif (user_choice, computer_choice) in [('1', '3'), ('2', '1'), ('3', '2')]: result_text = "ניצחת"
        else: result_text = "המחשב ניצח"
        
        final_message = f"t-בחרת {user_text}, המחשב בחר {computer_text}. {result_text}."
        commands = [f"id_list_message={final_message}", "go_to_folder=/?x=2&step=1"]
        return "&".join(commands)

    return "id_list_message=t-שגיאה במשחק"


# =======================================================
#        חלק C-3 (פונקציה 'c') - משחק הגרלות
# =======================================================
def c_lottery(params):
    step = params.get("step", "1")

    # שלב 1: תפריט ראשי
    if step == "1":
        prompt = "t-ברוך הבא לשוחת ההגרלות.  הקש 1 לקובייה אחת, 2 לשתי קוביות, 3 לבחירת המספר"
        return_path = f"/?x=3&step=2"
        return f"read={prompt}=lottery_choice,,1,1,{return_path}"

    # שלב 2: עיבוד הבחירה
    elif step == "2":
        choice = params.get("lottery_choice")

        if choice == "1":
            return f"id_list_message=t-הקובייה הראתה {random.randint(1, 6)}"
        elif choice == "2":
            return f"id_list_message=t-הקוביות הראו {random.randint(1, 6)} ו {random.randint(1, 6)}"
        elif choice == "3":
            prompt = "t-הקש את המספר הגבוה ביותר לטווח ההגרלה"
            return_path = f"/?x=3&step=3"
            return f"read={prompt}=max_number,,,{return_path}"
        else:
            return "id_list_message=t-בחירה לא חוקית.&go_to_folder=/?x=3&step=1"
            
    # שלב 3: קבלת טווח והגרלה
    elif step == "3":
        max_number_str = params.get("max_number")
        try:
            max_number = int(max_number_str)
            if max_number < 1: raise ValueError()
            return f"id_list_message=t-המספר שהוגרל הוא {random.randint(1, max_number)}"
        except:
            return "id_list_message=t-ערך לא תקין.&go_to_folder=/?x=3&step=1"
    
    return "id_list_message=t-שגיאה במשחק ההגרלות"


# קטע הרצה לשרתים כמו Railway
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
