from models.games import Game, InitiativeItem
from config.database import games_collection
from schema.schemas import multiple_games
from config.auth import get_current_user
from routes.pawns import websocket_connection

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends

games_router = APIRouter()

@games_router.get("/games/{owner_id}")
async def get_user_games(owner_id: str, current_user: dict = Depends(get_current_user)):
    try:
        object_id = ObjectId(owner_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    games = await multiple_games(games_collection.find({"owner_id": object_id}))
    for game in games:
        game["id"] = str(game["id"])
        game["owner_id"] = str(game["owner_id"])
    if games:
        return games
    raise HTTPException(status_code=404, detail="No games found")

@games_router.post("/games/create")
async def create_new_game(game: Game):
    game = dict(game)
    try:
        game["owner_id"] = ObjectId(game["owner_id"])
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    await games_collection.insert_one(game)
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

@games_router.patch("/games/{game_id}/is-fog/{is_fog}")
async def set_is_fog(game_id: str, is_fog: bool):
    try:
        game_object_id = ObjectId(game_id)
    except Exception:
         raise HTTPException(status_code=400, detail="Invalid game ID format")
    game = await games_collection.find_one({"_id": game_object_id})
    if game["is_fog"] != is_fog :
        result = await games_collection.update_one(
            {"_id": game_object_id},
            {"$set": {"is_fog": is_fog}}
        )
        await websocket_connection.broadcast({"event": "is_fog_changed", "data": is_fog}, game_id=str(game_object_id))
    return{
        "status": "ok",
        "message": "Updated fog",
    }

@games_router.patch("/games/{game_id}/add-to-initiative")
async def add_to_initiative(game_id: str, pawn: InitiativeItem):
    game = await games_collection.find_one({"_id": ObjectId(game_id)})

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check if the pawn already exists in initiative_list
    if any(p["name"] == pawn.name for p in game["initiative_list"]):
        raise HTTPException(
            status_code=400, detail="Pawn is already in the initiative list"
        )
    await websocket_connection.broadcast({"event": "pawn_added_to_initiative", "data": pawn.model_dump_json()}, game_id=str(game_id))
    
    updated_initiative_list = game["initiative_list"] + [pawn.dict()]
    updated_initiative_list.sort(key=lambda p: p["initiative"], reverse=True)

    update_result = await games_collection.update_one(
        {"_id": ObjectId(game_id)},
        {"$set": {"initiative_list": updated_initiative_list}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=500, detail="Failed to add pawn to initiative list"
        )

    return {"detail": "Pawn added to initiative list successfully"}

@games_router.delete("/games/{game_id}/delete-from-initiative/{pawn_name}")
async def delete_from_initiative(game_id: str, pawn_name: str):
    game = await games_collection.find_one({"_id": ObjectId(game_id)})
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    new_initiative_list = [
        item for item in game["initiative_list"] if item["name"] != pawn_name
    ]

    update_result = await games_collection.update_one(
        {"_id": ObjectId(game_id)},
        {"$set": {"initiative_list": new_initiative_list}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Pawn not found in initiative list")

    return {"detail": "Pawn removed from initiative list"}

@games_router.patch("/games/{access_code}/join/{user_id}")
async def join_game(access_code: int, user_id: str):
    game = await games_collection.find_one({"access_code": access_code})
    
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found."
        )

    # Check if the user is already in the player_list
    if user_id in game.get("player_list", []):
        raise HTTPException(
            status_code=400,
            detail="User is already part of the game."
        )

    # Add the user to the player_list
    updated_player_list = game.get("player_list", [])
    updated_player_list.append(user_id)

    # Update the game in the database
    result = await games_collection.update_one(
        {"access_code": access_code},
        {"$set": {"player_list": updated_player_list}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=500,
            detail="Failed to update the game."
        )

    return {"message": "User successfully added to the game."}