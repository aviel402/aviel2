# זהו הקוד שרץ ב-el
from flask import Flask, Response, jsonify
import requests # חשוב להוסיף requests ל-requirements.txt
import os

app = Flask(__name__)

# הגדרת הכתובת של השרת השני (Render), אותה נשים במשתני הסביבה
RENDER_SERVER_URL = os.environ.get("RENDER_URL")

# --- פונקציית העזר שביקשת ---
def call_render_server(param1, param2, param3):
    """
    פונקציה זו מקבלת 3 פרמטרים, ושולחת אותם לשרת ב-Render.
    היא מחזירה את התשובה שהתקבלה.
    """
    if not RENDER_SERVER_URL:
        return "שגיאה: כתובת שרת הרנדר אינה מוגדרת"
        
    # בניית הפרמטרים לשליחה
    query_params = {'x': param1, 'y': param2, 'z': param3}
    
    try:
        # שליחת הבקשה בשיטת GET
        response = requests.get(RENDER_SERVER_URL, params=query_params)
        
        # בדיקה אם הבקשה הצליחה
        if response.ok:
            return response.text # מחזירים את הטקסט שהשרת השני החזיר
        else:
            return f"שגיאה בתקשורת עם שרת הרנדר: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"שגיאת רשת: {e}"

# דוגמת שימוש
@app.route('/',methods=['GET','POST'])
def example_usage():
    a=request.args
    if not n:
    
        call_render_server("p.txt", "w", a)
    else:
        f = call_render_server("p.txt", "r")
        return f.read()
    # מחזירים את התוצאה למשתמש (לימות המשיח)
    return Response(f"id_list_message=t-התקבל", mimetype='text/plain')



