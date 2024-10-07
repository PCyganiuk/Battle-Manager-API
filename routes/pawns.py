from models.pawns import Pawn, PawnCords
from config.database import pawns_collection
from schema.schemas import individual_pawn, multiple_pawns
from config.auth import get_current_user

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, status

pawns_router = APIRouter()

@pawns_router.get("/pawns/{game_id}")
async def get_all_pawns(game_id: str):
    try:
        game_object_id = ObjectId(game_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid game ID format")
    pawns = await multiple_pawns(pawns_collection.find({"game_id": game_object_id}))
    for pawn in pawns:
        pawn["id"] = str(pawn["id"])
        pawn["game_id"] = str(pawn["game_id"])
    if pawns:
        return pawns
    
@pawns_router.post("/pawns/add")
async def add_new_pawn(pawn: Pawn):
    pawn = dict(pawn)
    pawn["game_id"] = ObjectId(pawn["game_id"])
    if pawn["player_character"]:
        pawn["player_character"] = ObjectId(pawn["player_character"])
    await pawns_collection.insert_one(pawn)
    return{
        "status": "ok",
        "detail": " Pawn added successfully"
    }

@pawns_router.patch("/pawns/new-pos/{pawn_id}")
async def modify_pawn_pos(pawn_id: str, pawn_cords: PawnCords):
    try:
        pawn_object_id = ObjectId(pawn_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid pawn ID format")
    pawn = await pawns_collection.find_one({"_id": pawn_object_id})
    if not pawn:
        raise HTTPException(status_code=400, detail="Pawn not found")
    result1 = await pawns_collection.update_one(
        {"_id": pawn_object_id},
        {"$set": {"pos_x": pawn_cords.pos_x}},
    )
    result2 = await pawns_collection.update_one(
        {"_id": pawn_object_id},
        {"$set": {"pos_y": pawn_cords.pos_y}},
    )
    if result1.matched_count == 0 or result2.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pawn not found")
    return {
        "status": "ok",
        "detail": " Pawn coordinates updated successfully"
    }