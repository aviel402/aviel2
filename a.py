<?php

// =======================================================
//             חלק A (ה-Controller)
// =======================================================
function main_controller() {
    $all_params = $_REQUEST;
    $response_string = yemot_service($all_params);
    echo $response_string;
}

// =======================================================
//             חלק B (המנתב - Router)
// =======================================================
function yemot_service($request_params) {
    $x = isset($request_params['x']) ? $request_params['x'] : null;

    if ($x !== null && strpos($x, '/') !== false) {
        return handle_installation_logic($request_params);
    }
    
    if ($x == "1") return a_calculator_logic($request_params);
    elseif ($x == "2") return b_rock_paper_scissors_logic($request_params);
    elseif ($x == "3") return c_lottery_logic($request_params);
    
    return "id_list_message=t-פעולה לא מוגדרת";
}


// =======================================================
//        חלק C - אפליקציות המשחקים (1, 2, 3)
// =======================================================

function a_calculator_logic($params) { /* ... קוד המחשבון המלא ... */ }
function b_rock_paper_scissors_logic($params) { /* ... קוד אבן נייר ומספריים המלא ... */ }
function c_lottery_logic($params) { /* ... קוד משחק ההגרלות המלא ... */ }

// (כדי שההודעה לא תהיה ארוכה מדי, אני מדלג על הדבקת הקוד המלא שלהן כאן,
// אבל כמובן שהוא צריך להיות בקובץ שלך)


// =======================================================
//        חלק C - פונקציית ניהול להתקנות
// =======================================================
function handle_installation_logic($params) {
    $install_path = isset($params['x']) ? $params['x'] : '';
    $app_id = explode('/', $install_path)[1] ?? null;

    // --- הוספנו כאן את התיאור לאפליקציה 3 ---
    $app_names = [
        '1' => 'מחשבון',
        '2' => 'אבן נייר ומספריים',
        '3' => 'משחק הגרלות' // התוספת החדשה
    ];
    $app_name = isset($app_names[$app_id]) ? $app_names[$app_id] : 'יישום לא ידוע';

    $step = isset($params['step']) ? $params['step'] : '1';
    
    // שלב 1: בקשת מספר מערכת
    if ($step == '1') {
        $prompt = "t-להתקנת יישום $app_name. אנא הקש את מספר המערכת, עשר ספרות, וסולמית";
        $return_path = "index.php?" . http_build_query(['x' => $install_path, 'step' => '2', 'app_name' => $app_name]);
        return "read=$prompt=system_number,10,10,$return_path";
    }

    // שלב 2: בקשת סיסמת ניהול
    elseif ($step == '2') {
        $system_number = isset($params['system_number']) ? $params['system_number'] : '';
        $app_name = isset($params['app_name']) ? $params['app_name'] : 'היישום';
        $prompt = "t-כעת, אנא הקש את סיסמת הניהול של המערכת";
        $return_path = "index.php?" . http_build_query(['x' => $install_path, 'step' => '3', 'app_name' => $app_name, 'system_number' => $system_number]);
        return "read=$prompt=password,,4,10,$return_path";
    }

    // שלב 3: בקשת מספר שלוחה
    elseif ($step == '3') {
        $system_number = isset($params['system_number']) ? $params['system_number'] : '';
        $password = isset($params['password']) ? $params['password'] : '';
        $app_name = isset($params['app_name']) ? $params['app_name'] : 'היישום';
        $prompt = "t-לבסוף, הקש את מספר השלוחה להתקנת $app_name, וסולמית";
        $return_path = "index.php?" . http_build_query([
            'x' => $install_path, 'step' => '4', 'app_name' => $app_name, 
            'system_number' => $system_number, 'password' => $password
        ]);
        return "read=$prompt=folder_number,1,10,$return_path";
    }

    // שלב 4: שלב ההתקנה (עתידי)
    elseif ($step == '4') {
        $system_number = isset($params['system_number']) ? $params['system_number'] : '';
        $password = isset($params['password']) ? $params['password'] : '';
        $folder_number = isset($params['folder_number']) ? $params['folder_number'] : '';
        $app_name = isset($params['app_name']) ? $params['app_name'] : 'היישום';

        $message = "t-התקבלו הנתונים. המערכת היא $system_number, שלוחה $folder_number. שלב ההתקנה בפועל בפיתוח";
        return "id_list_message=$message&go_to_folder=hangup";
    }

    return "id_list_message=t-שגיאה בתהליך ההתקנה";
}


// =============== קריאה להפעלה ===============
main_controller();

?>