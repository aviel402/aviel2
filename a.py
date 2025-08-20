from flask import Flask, request, Response
import json # נייבא את ספריית json כדי להדפיס יפה

# =======================================================
#               כלי איתור תקלות (דיבגר)
# =======================================================

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def ultimate_debugger():
    
    # --- שלב 1: תיעוד מלא של הבקשה ---
    print("\n\n--- !!! NEW REQUEST RECEIVED FROM YEMOT !!! ---")
    
    # נדפיס את שיטת הבקשה (GET או POST)
    print(f"METHOD: {request.method}")
    
    # נדפיס את הכותרות (Headers) של הבקשה
    # json.dumps יעזור לנו להציג את זה בצורה קריאה
    headers_dict = dict(request.headers)
    print(f"HEADERS: {json.dumps(headers_dict, indent=2, ensure_ascii=False)}")
    
    # נדפיס את הפרמטרים שהגיעו בכתובת (בשיטת GET)
    args_dict = request.args.to_dict()
    print(f"QUERY PARAMS (from URL): {json.dumps(args_dict, indent=2, ensure_ascii=False)}")
    
    # נדפיס את הפרמטרים שהגיעו בגוף הבקשה (בשיטת POST)
    form_dict = request.form.to_dict()
    print(f"FORM PARAMS (from Body): {json.dumps(form_dict, indent=2, ensure_ascii=False)}")
    
    print("--- END OF REQUEST DETAILS ---\n\n")
    
    # --- שלב 2: החזרת תגובה פשוטה לימות ---
    
    response_string = "id_list_message=t-תגידי לאביאל שזה עובד תגידי לאביאל שזה עובדgo_to_folder=hangup"
    
    return Response(response_string, mimetype='text/plain; charset=UTF-8')