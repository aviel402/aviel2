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
//        חלק C-1 ('a') - המחשבון המלא
// =======================================================
function a_calculator_logic($params) {
    $step = isset($params['step']) ? $params['step'] : '1';
    
    if ($step == '1') {
        $prompt = "t-ברוך הבא למחשבון, אנא הקש את המספר הראשון";
        $return_path = "index.php?" . http_build_query(['x' => '1', 'step' => '2']);
        return "read=$prompt=num1,,,$return_path";
    }
    elseif ($step == '2') {
        $num1_from_user = isset($params['num1']) ? $params['num1'] : '';
        $prompt = "t-אנא הקש פעולה, 1 חיבור, 2 חיסור, 3 כפל, 4 חילוק, 5 חזקה";
        $return_path = "index.php?" . http_build_query(['x' => '1', 'step' => '3', 'saved_num1' => $num1_from_user]);
        return "read=$prompt=op,1,1,$return_path";
    }
    elseif ($step == '3') {
        $num1_saved = isset($params['saved_num1']) ? $params['saved_num1'] : '';
        $op_saved = isset($params['op']) ? $params['op'] : '';
        $prompt = "t-אנא הקש את המספר השני";
        $return_path = "index.php?" . http_build_query(['x' => '1', 'step' => '4', 'saved_num1' => $num1_saved, 'saved_op' => $op_saved]);
        return "read=$prompt=num2,,,$return_path";
    }
    elseif ($step == '4') {
        $a_str = isset($params['saved_num1']) ? $params['saved_num1'] : '';
        $b_str = isset($params['saved_op']) ? $params['saved_op'] : '';
        $c_str = isset($params['num2']) ? $params['num2'] : '';
        $d = "שגיאה בערכים";
        if ($a_str && $b_str && $c_str) {
            $a = floatval($a_str); $b = $b_str; $c = floatval($c_str);
            if ($b == '1') $d = $a + $c;
            elseif ($b == '2') $d = $a - $c;
            elseif ($b == '3') $d = $a * $c;
            elseif ($b == '4') $d = ($c != 0) ? round($a / $c, 2) : "אי אפשר לחלק באפס";
            elseif ($b == '5') $d = $a ** $c;
            else $d = "פעולה לא חוקית";
        }
        $return_path = "index.php?" . http_build_query(['x' => '1', 'step' => '1']);
        return "id_list_message=t-התוצאה היא $d&go_to_folder=$return_path";
    }
    return "id_list_message=t-שגיאה לא צפויה במערכת";
}

// =======================================================
//      חלק C-2 ('b') - אבן, נייר ומספריים המלא
// =======================================================
function b_rock_paper_scissors_logic($params) {
    $step = isset($params['step']) ? $params['step'] : '1';
    
    if ($step == '1') {
        $prompt = "t-ברוך הבא לאבן נייר ומספריים. בחר: 1 אבן, 2 נייר, 3 מספריים";
        $return_path = "index.php?" . http_build_query(['x' => '2', 'step' => '2']);
        return "read=$prompt=choice,1,1,$return_path";
    }
    elseif ($step == '2') {
        $user_choice = isset($params['choice']) ? $params['choice'] : '';
        if (!in_array($user_choice, ['1', '2', '3'])) {
            return "id_list_message=t-בחירה לא חוקית&go_to_folder=index.php?".http_build_query(['x'=>'2','step'=>'1']);
        }
        $computer_choice = (string)rand(1, 3);
        $options = ["1" => "אבן", "2" => "נייר", "3" => "מספריים"];
        $user_text = $options[$user_choice]; $computer_text = $options[$computer_choice];
        if ($user_choice == $computer_choice) $result_text = "תיקו";
        elseif (($user_choice == '1' && $computer_choice == '3') || ($user_choice == '2' && $computer_choice == '1') || ($user_choice == '3' && $computer_choice == '2')) $result_text = "ניצחת";
        else $result_text = "המחשב ניצח";
        $final_message = "t-בחרת $user_text, המחשב בחר $computer_text. התוצאה: $result_text";
        $return_path = "index.php?" . http_build_query(['x' => '2', 'step' => '1']);
        return "id_list_message=$final_message&go_to_folder=$return_path";
    }
}

// =======================================================
//        חלק C-3 ('c') - משחק הגרלות המלא
// =======================================================
function c_lottery_logic($params) {
    $step = isset($params['step']) ? $params['step'] : '1';
    if ($step == '1') {
        $prompt = "t-משחק ההגרלות. 1 לקובייה, 2 לשתי קוביות, 3 למספר בטווח";
        $return_path = "index.php?" . http_build_query(['x' => '3', 'step' => '2']);
        return "read=$prompt=choice,1,1,$return_path";
    }
    elseif ($step == '2') {
        $choice = isset($params['choice']) ? $params['choice'] : '';
        $return_path = "index.php?" . http_build_query(['x' => '3', 'step' => '1']);
        if ($choice == '1') { $roll = rand(1, 6); return "id_list_message=t-הקובייה הראתה $roll&go_to_folder=$return_path"; }
        elseif ($choice == '2') { $roll1 = rand(1, 6); $roll2 = rand(1, 6); $total = $roll1 + $roll2; return "id_list_message=t-הקוביות הראו $roll1 ו-$roll2. סך הכל $total&go_to_folder=$return_path"; }
        elseif ($choice == '3') { $prompt = "t-אנא הקש את המספר הגבוה ביותר לטווח"; $return_path_range = "index.php?" . http_build_query(['x' => '3', 'step' => '3']); return "read=$prompt=max_number,,,$return_path_range"; }
        else { return "id_list_message=t-בחירה לא חוקית&go_to_folder=$return_path"; }
    }
    elseif ($step == '3') {
        $max_number_str = isset($params['max_number']) ? $params['max_number'] : '';
        $return_path = "index.php?" . http_build_query(['x' => '3', 'step' => '1']);
        if (is_numeric($max_number_str) && intval($max_number_str) > 0) { $max_number = intval($max_number_str); $random_number = rand(1, $max_number); return "id_list_message=t-המספר שהוגרל הוא $random_number&go_to_folder=$return_path"; }
        else { return "id_list_message=t-ערך לא תקין&go_to_folder=$return_path"; }
    }
    return "id_list_message=t-שגיאה במשחק";
}

// =======================================================
//        חלק C-Install - פונקציית ניהול להתקנות
// =======================================================
function handle_installation_logic($params) {
    $install_path = isset($params['x']) ? $params['x'] : '';
    $app_id = explode('/', $install_path)[1] ?? null;
    $app_names = ['1' => 'מחשבון', '2' => 'אבן נייר ומספריים', '3' => 'משחק הגרלות'];
    $app_name = isset($app_names[$app_id]) ? $app_names[$app_id] : 'יישום לא ידוע';
    $step = isset($params['step']) ? $params['step'] : '1';
    
    if ($step == '1') {
        $prompt = "t-להתקנת יישום $app_name. הקש מספר מערכת וסולמית";
        $return_path = "index.php?" . http_build_query(['x' => $install_path, 'step' => '2', 'app_name' => $app_name]);
        return "read=$prompt=system_number,10,10,$return_path";
    }
    elseif ($step == '2') {
        $system_number = isset($params['system_number']) ? $params['system_number'] : '';
        $app_name = isset($params['app_name']) ? $params['app_name'] : 'היישום';
        $prompt = "t-כעת, הקש את סיסמת הניהול";
        $return_path = "index.php?" . http_build_query(['x' => $install_path, 'step' => '3', 'app_name' => $app_name, 'system_number' => $system_number]);
        return "read=$prompt=password,,4,10,$return_path";
    }
    elseif ($step == '3') {
        $system_number = isset($params['system_number']) ? $params['system_number'] : '';
        $password = isset($params['password']) ? $params['password'] : '';
        $app_name = isset($params['app_name']) ? $params['app_name'] : 'היישום';
        $prompt = "t-לבסוף, הקש מספר שלוחה להתקנה, וסולמית";
        $return_path = "index.php?" . http_build_query(['x' => $install_path, 'step' => '4', 'app_name' => $app_name, 'system_number' => $system_number, 'password' => $password]);
        return "read=$prompt=folder_number,1,10,$return_path";
    }
    elseif ($step == '4') {
        $system_number = isset($params['system_number']) ? $params['system_number'] : ''; $password = isset($params['password']) ? $params['password'] : ''; $folder_number = isset($params['folder_number']) ? $params['folder_number'] : '';
        $message = "t-התקבלו הנתונים. המערכת היא $system_number, שלוחה $folder_number. שלב ההתקנה בפועל עדיין בפיתוח";
        return "id_list_message=$message&go_to_folder=hangup";
    }
    return "id_list_message=t-שגיאה בתהליך ההתקנה";
}

// =============== קריאה להפעלה ===============
main_controller();

?>