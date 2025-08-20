# =======================================================
#             חלק B (המנתב - Router) - גרסה מעודכנת
# =======================================================

def yemot_service(request_params):
    x = request_params.get("x")
    if x == "1":
        # קריאה לפונקציית המחשבון
        return a(request_params)
    
    # --- התוספת החדשה ---
    elif x == "2":
        # קריאה לפונקציית אבן, נייר ומספריים
        return b(request_params)
    
    # אם לא נמצאה פונקציה מתאימה
    return "id_list_message=t-פעולה לא מוגדרת"```

### שלב 2: בניית חלק C החדש (המשחק עצמו)

עכשיו ניצור את הפונקציה החדשה שלנו, שכל כולה מוקדשת למשחק. נקרא לה `b`. היא תפעל גם כן בשיטת ה"שלבים".

הנה הקוד שצריך להוסיף לקובץ `a.py`, מתחת לחלק של המחשבון.

```python
# =======================================================
#        חלק C-2 (פונקציה 'b') - אבן, נייר ומספריים
# =======================================================
def b(params):
    
    # נצטרך את 'random' בשביל הבחירה של המחשב
    import random
    
    step = params.get("step", "1")

    # --- שלב 1: קבלת פנים ובקשת בחירה מהשחקן ---
    if step == "1":
        prompt = "t-ברוכים הבאים לאבן נייר ומספריים. אנא בחר: 1 לאבן, 2 לנייר, או 3 למספריים"
        # אחרי הבחירה, נחזור לשלב 2
        return_path = f"/?x=2&step=2"
        # נקבל קלט מהמשתמש ונשמור אותו במשתנה 'choice'
        return f"read={prompt}=choice,,1,1,{return_path}"

    # --- שלב 2: קבלת הבחירה, חישוב התוצאה והכרזה ---
    elif step == "2":
        user_choice = params.get("choice")

        # נוודא שהקלט תקין
        if not user_choice or user_choice not in ["1", "2", "3"]:
            return "id_list_message=t-בחירה לא חוקית. נסה שנית.&go_to_folder=/?x=2&step=1"
        
        # בחירת המחשב
        computer_choice = str(random.randint(1, 3))
        
        # תרגום המספרים למילים
        options = {"1": "אבן", "2": "נייר", "3": "מספריים"}
        user_text = options[user_choice]
        computer_text = options[computer_choice]
        
        # קביעת המנצח
        if user_choice == computer_choice:
            result_text = "תיקו"
        elif (user_choice == '1' and computer_choice == '3') or \
             (user_choice == '2' and computer_choice == '1') or \
             (user_choice == '3' and computer_choice == '2'):
            result_text = "ניצחת"
        else:
            result_text = "המחשב ניצח"
        
        # הרכבת התגובה הסופית, ואפשרות לשחק שוב
        final_message = f"t-בחרת {user_text}, המחשב בחר {computer_text}. התוצאה: {result_text}."
        
        # נחבר את כל הפקודות יחד
        commands_to_send = [
            f"id_list_message={final_message}",
            "id_list_message=t-למשחק נוסף, הישאר על הקו",
            # חזרה לתחילת המשחק
            "go_to_folder=/?x=2&step=1"
        ]
        
        return "&".join(commands_to_send)

    # במקרה של שלב לא מוכר
    return "id_list_message=t-שגיאה במשחק אבן נייר ומספריים"