def individual_user(user) -> dict:
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "join_date": user["join_date"]
    }

async def multiple_users(users) -> list:
    return [individual_user(user) async for user in users]

def individual_game(game) -> dict:
    return{
        "id": str(game["_id"]),
        "game_name": game["game_name"],
        "owner_id": str(game["owner_id"]),
        "dimension_x": game["dimension_x"],
        "dimension_y": game["dimension_y"],
        "current_turn": str(game["current_turn"]) if game["current_turn"] else None,
        "initiative_list": [
            {"name": pawn["name"], "initiative": pawn["initiative"]} 
            for pawn in game["initiative_list"]
        ],
        "picture_id": game["picture_id"],
        "player_list": [str(player) for player in game["player_list"]],
        "is_fog": game["is_fog"],
    }

async def multiple_games(games) -> list:
    return [individual_game(game) async for game in games]

def individual_pawn(pawn) -> dict:
    return{
        "id": str(pawn["_id"]),
        "pawn_name": pawn["pawn_name"],
        "pos_x": pawn["pos_x"],
        "pos_y": pawn["pos_y"],
        "dimension_x": pawn["dimension_x"],
        "dimension_y": pawn["dimension_y"],
        "hit_points": pawn["hit_points"],
        "initiative": pawn["initiative"],
        "attack_bonus": pawn["attack_bonus"],
        "damage_bonus": pawn["damage_bonus"],
        "armor_class": pawn["armor_class"],
        "strength": pawn["strength"],
        "dexterity": pawn["dexterity"],
        "constitution": pawn["constitution"],
        "intelligence": pawn["intelligence"],
        "wisdom": pawn["wisdom"],
        "charisma": pawn["charisma"],
        "speed": pawn["speed"],
        "game_id": pawn["game_id"],
        "picture": str(pawn["picture"] if pawn["picture"] else None),
        "ai_enabled": pawn["ai_enabled"],
        "player_character": str(pawn["player_character"] if pawn["player_character"] else None),
    }

async def multiple_pawns(pawns) -> list:
    return [individual_pawn(pawn) async for pawn in pawns]

def individual_obstacle(obstacle) -> dict:
    return{
        "id": str(obstacle["_id"]),
        "pos_x": obstacle["pos_x"],
        "pos_y": obstacle["pos_y"],
        "width": obstacle["width"],
        "height": obstacle["height"],
        "game_id": obstacle["game_id"],
        "color": obstacle["color"]
    }

async def multiple_obstacles(obstacles) -> list:
    return [individual_obstacle(obstacle) async for obstacle in obstacles]