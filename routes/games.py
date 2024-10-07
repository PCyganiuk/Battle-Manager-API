from fastapi import APIRouter, HTTPException, Depends, status
from models.games import Game
from config.database import games_collection
from schema.schemas import individual_game, multiple_games
from config.auth import get_current_user

from datetime import timedelta, datetime
from bson import ObjectId

games_router = APIRouter()

@games_router.get("/games/{owner_id}")
async def get_user_games(owner_id: str, current_user: dict = Depends(get_current_user)):
    try:
        object_id = ObjectId(owner_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    games = await multiple_games(games_collection.find({"owner_id": object_id}))
    for game in games:
        print(game)
        game["id"] = str(game["id"])
        game["owner_id"] = str(game["owner_id"])
    if games:
        return games
    raise HTTPException(status_code=404, detail="No games found")

@games_router.post("/games/create")
async def create_new_game(game: Game):
    game = dict(game)
    game["owner_id"] = ObjectId(game["owner_id"])
    games_collection.insert_one(game)
    return{
        "status": "ok",
        "message": "Game created successfully",
    }

@games_router.patch("/games/{game_id}/modify-initiative")
async def modify_initiative(game_id: str, body: dict):
    try:
        game_object_id = ObjectId(game_id)
    except Exception:
         raise HTTPException(status_code=400, detail="Invalid game ID format")
    result = await games_collection.update_one(
        {"_id": game_object_id},
        {"$set": {"initiative_list": body["pawn_id_list"]}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Game not found")
    return{
        "status": "ok",
        "message": "Pawn ID added to initiative list successfully",
    }

@games_router.patch("/games/{game_id}/add-player/{player_id}")
async def add_player(game_id: str, player_id: str):
    try:
        game_object_id = ObjectId(game_id)
    except Exception:
         raise HTTPException(status_code=400, detail="Invalid game ID format")
    game = await games_collection.find_one({"_id": game_object_id})
    if game and player_id in game.get("player_list", []):
        return {
            "status": "ok",
            "message": "Player ID is already in the game."
        }
    result = await games_collection.update_one(
        {"_id": game_object_id},
        {"$addToSet": {"player_list": player_id}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Game not found")
    return{
        "status": "ok",
        "message": "Player ID added to the game successfully",
    }

@games_router.patch("/games/{game_id}/remove-player/{player_id}")
async def add_player(game_id: str, player_id: str):
    try:
        game_object_id = ObjectId(game_id)
    except Exception:
         raise HTTPException(status_code=400, detail="Invalid game ID format")
    game = await games_collection.find_one({"_id": game_object_id})
    if game and not player_id in game.get("player_list", []):
        return {
            "status": "ok",
            "message": "Player ID not found in the game."
        }
    result = await games_collection.update_one(
        {"_id": game_object_id},
        {"$pull": {"player_list": player_id}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Game not found")
    return{
        "status": "ok",
        "message": "Player ID removed from the game successfully",
    }

@games_router.patch("/games/{game_id}/set-current-turn/{pawn_id}")
async def set_current_turn(game_id: str, pawn_id: str):
    try:
        game_object_id = ObjectId(game_id)
    except Exception:
         raise HTTPException(status_code=400, detail="Invalid game ID format")
    game = await games_collection.find_one({"_id": game_object_id})
    if game and not pawn_id in game.get("initiative_list",[]):
        return {
            "status": "ok",
            "message": "pawn id not found in initiative list."
        }
    result = await games_collection.update_one(
        {"_id": game_object_id},
        {"$set": {"current_turn": pawn_id}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Game not found")
    return{
        "status": "ok",
        "message": "Set new current pawn",
    }