from models.pawns import Pawn, PawnCords, PawnInfo
from config.database import pawns_collection
from schema.schemas import individual_pawn, multiple_pawns
from config.auth import get_current_user
from config.websocket import ConnectionManager

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, status, WebSocketDisconnect, WebSocket

pawns_router = APIRouter()
websocket_connection = ConnectionManager()

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
    if processed_pawn["player_character"] is not None:
        processed_pawn["player_character"] = str(processed_pawn["player_character"])
    
    return processed_pawn

@pawns_router.websocket("/ws/pawns/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    await websocket_connection.connect(websocket, game_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_connection.disconnect(websocket)
    
@pawns_router.post("/pawns/add")
async def add_new_pawn(pawn: Pawn):
    pawn = dict(pawn)
    ws_pawn = pawn

    pawn["game_id"] = ObjectId(pawn["game_id"])
    if pawn["player_character"] and pawn["player_character"] != "":
        pawn["player_character"] = ObjectId(pawn["player_character"])
    addedPawn = await pawns_collection.insert_one(pawn)
    pawn["game_id"] = str(pawn["game_id"])
    pawn["_id"] = str(pawn["_id"])
    await websocket_connection.broadcast({"event": "pawn_added", "data": ws_pawn}, game_id=str(ws_pawn["game_id"]))



    return{
        "status": "ok",
        "detail": " Pawn added successfully",
        "id": str(addedPawn.inserted_id),
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

    await websocket_connection.broadcast({"event": "pawn_position_updated", "pawn_id": pawn_id, "data": pawn_cords.dict()}, game_id=str(pawn["game_id"]))
    
    if result1.matched_count == 0 or result2.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pawn not found")
    return {
        "status": "ok",
        "detail": " Pawn coordinates updated successfully"
    }

@pawns_router.patch("/{game_id}pawns/modify-pawn/{pawn_id}")
async def modify_pawn_info(game_id: str, pawn_id: str, pawn: PawnInfo):
    try:
        pawn_object_id = ObjectId(pawn_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid pawn ID format")
    
    db_pawn = await pawns_collection.find_one({"_id": pawn_object_id})
    if not db_pawn:
        raise HTTPException(status_code=400, detail="Pawn not found")
    update_data = {k: v for k, v in pawn.model_dump(exclude_unset=True).items()}
    transformed_data = [
        {"stat": stat, "value": value} 
        for stat, value in update_data.items()
    ]
    result = await pawns_collection.update_one(
        {"_id": pawn_object_id},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")
    await websocket_connection.broadcast({"event": "pawn_stat_updated", "pawn_id": pawn_id, "data": transformed_data}, game_id)
    return {
        "status": "ok",
        "detail": " Pawn info updated successfully"
    }   