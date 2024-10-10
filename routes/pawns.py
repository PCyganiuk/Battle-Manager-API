from models.pawns import Pawn, PawnCords, PawnInfo
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
    
@pawns_router.get("/pawns/one/{pawn_id}")
async def get_one_pawns(pawn_id: str):
    try:
        pawn_object_id = ObjectId(pawn_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid pawn ID format")
    
    pawn = await pawns_collection.find_one({"_id": pawn_object_id})
    
    if not pawn:
        raise HTTPException(status_code=404, detail="Pawn not found")
    
    processed_pawn = individual_pawn(pawn)
    
    processed_pawn["id"] = str(processed_pawn["id"])
    processed_pawn["game_id"] = str(processed_pawn["game_id"])
    if processed_pawn["picture_id"]:
        processed_pawn["picture_id"] = str(processed_pawn["picture_id"])
    if processed_pawn["player_character"] is not None:
        processed_pawn["player_character"] = str(processed_pawn["player_character"])
    
    return processed_pawn
    
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

@pawns_router.patch("/pawns/modify-pawn/{pawn_id}")
async def modify_pawn_info(pawn_id: str, pawn: PawnInfo):
    try:
        pawn_object_id = ObjectId(pawn_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid pawn ID format")
    
    db_pawn = await pawns_collection.find_one({"_id": pawn_object_id})
    if not db_pawn:
        raise HTTPException(status_code=400, detail="Pawn not found")
    update_data = {k: v for k, v in pawn.model_dump(exclude_unset=True).items()}
    result = await pawns_collection.update_one(
        {"_id": pawn_object_id},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {
        "status": "ok",
        "detail": " Pawn info updated successfully"
    }   

@pawns_router.patch("/pawns/modify-picture/{pawn_id}/{picture_id}")
async def modify_pawn_picture(pawn_id: str, picture_id: str):
    try:
        pawn_object_id = ObjectId(pawn_id)
        picture_object_id = ObjectId(picture_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    db_pawn = await pawns_collection.find_one({"_id": pawn_object_id})
    if not db_pawn:
        raise HTTPException(status_code=400, detail="Pawn not found")
    result = await pawns_collection.update_one(
        {"_id": pawn_object_id},
        {"$set": {"picture_id": picture_object_id}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")
    return {
        "status": "ok",
        "detail": " Pawn picture updated successfully"
    }   
@pawns_router.delete("/pawns/delete-picture/{pawn_id}")
async def delete_pawn_picture(pawn_id: str):
    try:
        pawn_object_id = ObjectId(pawn_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    db_pawn = await pawns_collection.find_one({"_id": pawn_object_id})
    if not db_pawn:
        raise HTTPException(status_code=400, detail="Pawn not found")
    result = await pawns_collection.update_one(
        {"_id": pawn_object_id},
        {"$set": {"picture_id": None}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")
    return {
        "status": "ok",
        "detail": " Pawn picture updated successfully"
    }   