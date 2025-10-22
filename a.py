# קובץ: a.py (רץ על Vercel)

from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# קוראים את הכתובת של השרת השני מתוך משתני הסביבה של Vercel
RENDER_SERVER_URL = os.environ.get("RENDER_URL")

# --- פונקציית העזר שמתקשרת עם השרת השני ---
def file_operation(file_path, mode, content=None):
    """
    מקבלת נתיב לקובץ, מצב (read/write), ותוכן (לכתיבה).
    שולחת את המידע לשרת ב-Render ומחזירה את התשובה.
    """
    if not RENDER_SERVER_URL:
        return "שגיאה: כתובת שרת הרנדר אינה מוגדרת"

    # נבנה את הבקשה. הפעם נשתמש בשיטת POST כדי לשלוח מידע
    data_to_send = {
        'filepath': file_path,
        'mode': mode,
        'content': content
    }

    try:
        response = requests.post(RENDER_SERVER_URL, json=data_to_send)
        if response.ok:
            return response.json().get('result', 'שגיאה בפורמט התשובה')
        else:
            return f"שגיאה בתקשורת עם שרת האחסון: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"שגיאת רשת: {e}"


@app.route('/', methods=['POST', 'GET'])
def main_handler():
    # קולטים פרמטר מהבקשה של ימות המשיח, לדוגמה 'text_to_save'
    text_to_write = request.values.get("text_to_save")

    # הלוגיקה שלך
    if text_to_write:
        # אם יש טקסט חדש לשמור
        operation_result = file_operation("p.txt", "w", text_to_write)
        response_text = f"תוצאת פעולת הכתיבה: {operation_result}"
    else:
        # אם רוצים לקרוא מהקובץ
        file_content = file_operation("p.txt", "r")
        response_text = f"התוכן שקראנו מהקובץ: {file_content}"
    
    return Response(f"id_list_message=t-{response_text}", mimetype='text/plain')
