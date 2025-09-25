from flask import Flask, request
import random
import base64
import json

app = Flask(__name__)

# Game data
ANIMALS = {
    "ארנב מהיר": {"hp": 5, "atk": 2, "gold_drop": 2},
    "זאב ענק": {"hp": 15, "atk": 5, "gold_drop": 7},
    "דוב חזק": {"hp": 30, "atk": 8, "gold_drop": 15},
    "עכבר קטן": {"hp": 2, "atk": 1, "gold_drop": 1},
    "נחש מזרחי": {"hp": 10, "atk": 4, "gold_drop": 5},
    "גורילה ענקית": {"hp": 40, "atk": 10, "gold_drop": 20}
}

SHOP_ITEMS = {
    "1": {"name": "חרב פשוטה", "cost": 10, "power": 8},
    "2": {"name": "רובה ציד", "cost": 25, "power": 15},
    "3": {"name": "מקל קסם", "cost": 50, "power": 25}
}

INITIAL_STATE = {
    "hp": 20,
    "max_hp": 20,
    "bullets": 5,
    "gold": 0,
    "inventory": {"אגרופים": 5},
    "current_weapon": "אגרופים",
    "current_enemy": None
}

def get_state_from_url():
    """Decodes the game state from the 'state' URL parameter."""
    state_b64 = request.args.get('state')
    if not state_b64:
        return None
    try:
        return json.loads(base64.b64decode(state_b64).decode())
    except (json.JSONDecodeError, base64.binascii.Error):
        return None

def encode_state_to_b64(state):
    """Encodes the game state into a base64 string for saving."""
    return base64.b64encode(json.dumps(state).encode()).decode()

def get_next_url(state):
    """Generates the URL for the next turn, with the updated state."""
    encoded_state = encode_state_to_b64(state)
    return f"http://{request.host}/game_state?state={encoded_state}"

# --- Main Menu ---
@app.route('/', methods=['POST', 'GET'])
def main_menu():
    return "read=ברוך הבא למשחק מלחמת החיות! הקש 1 למשחק חדש, או 2 לטעינת משחק שמור. go_to_ivr=yes"

# --- Start New Game ---
@app.route('/new_game', methods=['POST', 'GET'])
def start_new_game():
    player_state = INITIAL_STATE.copy()
    player_state["current_enemy"] = None
    
    return "GoToIVR=" + get_next_url(player_state)

# --- Load Saved Game ---
@app.route('/load_game', methods=['POST', 'GET'])
def load_game():
    user_input = request.values.get('ApiUrlPress')
    
    if not user_input:
        return "read=אנא הקש את קוד השמירה שלך ולאחר מכן הקש כוכבית. go_to_ivr=yes"

    try:
        player_state = json.loads(base64.b64decode(user_input.encode()).decode())
        return "GoToIVR=" + get_next_url(player_state)
    except:
        return "read=קוד השמירה שהקשת אינו תקין. נסה שוב. go_to_ivr=yes"

# --- Game Logic & Shop ---
@app.route('/game_state', methods=['POST', 'GET'])
def game_state():
    player_state = get_state_from_url()
    user_input = request.values.get('ApiUrlPress')
    response_list = []
    
    if not player_state:
        return "read=שגיאה בטעינת מצב המשחק. go_to_ivr=yes"

    # Save and Exit (9)
    if user_input == "9":
        save_code = encode_state_to_b64(player_state)
        return f"read=קוד השמירה שלך הוא {save_code}. שמור אותו טוב! המשחק יסתיים כעת. go_to_ivr=yes"

    # Enter Shop (8)
    if user_input == "8":
        shop_menu = "read=ברוך הבא לחנות! יש לך {} זהב. הקש על מספר הפריט שתרצה לקנות. ".format(player_state['gold'])
        for key, item in SHOP_ITEMS.items():
            shop_menu += f"הקש {key} עבור {item['name']} במחיר {item['cost']} זהב. "
        shop_menu += "לחץ 0 כדי לחזור למשחק. go_to_ivr=yes"
        return shop_menu

    # Buy an item from the shop
    if user_input in SHOP_ITEMS.keys():
        item = SHOP_ITEMS[user_input]
        if player_state['gold'] >= item['cost']:
            player_state['gold'] -= item['cost']
            player_state['inventory'][item['name']] = item['power']
            response_list.append(f"read=קנית בהצלחה {item['name']}! יש לך כעת {player_state['gold']} זהב. go_to_ivr=yes")
        else:
            response_list.append("read=אין לך מספיק זהב כדי לקנות את הפריט הזה. go_to_ivr=yes")
        
        # Go back to main game loop
        new_url = get_next_url(player_state)
        return "GoToIVR=" + new_url + "&" + "&".join(response_list)

    if not player_state["current_enemy"]:
        animal_name = random.choice(list(ANIMALS.keys()))
        animal_stats = ANIMALS[animal_name]
        player_state["current_enemy"] = {"name": animal_name, "hp": animal_stats["hp"], "atk": animal_stats["atk"]}
        
        weapons_list = "אגרופים" if len(player_state['inventory']) == 1 else ",".join(player_state['inventory'].keys())
        response_list.append(f"read=הופעת מול {animal_name}! יש לו {animal_stats['hp']} נקודות חיים. יש לך {player_state['hp']} חיים ו-{player_state['bullets']} כדורים. כלי הנשק שלך: {weapons_list}. מה תעשה? go_to_ivr=yes")
    
    # User's turn
    current_enemy = player_state["current_enemy"]
    
    if user_input == "1":  # Attack
        if player_state["bullets"] > 0:
            player_damage = player_state['inventory'][player_state['current_weapon']]
            current_enemy["hp"] -= player_damage
            player_state["bullets"] -= 1
            response_list.append(f"read=תקפת את ה{current_enemy['name']} וגרמת לו {player_damage} נזק! go_to_ivr=yes")
        else:
            response_list.append("read=אין לך כדורים! עליך לטעון. go_to_ivr=yes")
    elif user_input == "2":  # Reload
        player_state["bullets"] += random.randint(3, 7)
        response_list.append(f"read=טענת כדורים! יש לך כעת {player_state['bullets']} כדורים. go_to_ivr=yes")
    elif user_input == "3": # Run away
        response_list.append(f"read=ברחת מהקרב! נסה להילחם שוב. go_to_ivr=yes")
        player_state["current_enemy"] = None
    elif user_input == "4": # Equip a weapon
        # ... (equip logic)
        pass # To be added later
    else:
        response_list.append("read=הקשה לא חוקית. go_to_ivr=yes")

    # Enemy's turn
    if current_enemy and current_enemy["hp"] > 0 and user_input in ["1", "2"]:
        enemy_damage = current_enemy["atk"]
        player_state["hp"] -= enemy_damage
        response_list.append(f"read=ה{current_enemy['name']} תקף אותך וגרם לך {enemy_damage} נזק! נותרו לך {player_state['hp']} נקודות חיים. go_to_ivr=yes")

    # Check for win or lose conditions
    if current_enemy and current_enemy["hp"] <= 0:
        gold_gained = ANIMALS[current_enemy["name"]]['gold_drop']
        player_state['gold'] += gold_gained
        response_list.append(f"read=ניצחת את ה{current_enemy['name']} וקיבלת {gold_gained} זהב! יש לך כעת {player_state['gold']} זהב. go_to_ivr=yes")
        player_state["current_enemy"] = None
    
    if player_state["hp"] <= 0:
        response_list.append("read=הפסדת בקרב! המשחק הסתיים. go_to_ivr=yes")
        player_state = INITIAL_STATE.copy()

    # Return the new state URL
    new_url = get_next_url(player_state)
    return "GoToIVR=" + new_url + "&" + "&".join(response_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
