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
        "initiative_list": [str(player) for player in game["initiative_list"]],
        "picture_id": str(game["picture_id"]) if game["picture_id"] else None,
        "player_list": [str(player) for player in game["player_list"]],
    }

async def multiple_games(games) -> list:
    return [individual_game(game) async for game in games]