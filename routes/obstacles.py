from models.obstacles import Obstacle, ObstacleCords
from config.database import obstacles_collection
from schema.schemas import multiple_obstacles
from config.auth import get_current_user
from routes.pawns import websocket_connection

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, status, WebSocketDisconnect, WebSocket

obstacles_router = APIRouter()

@obstacles_router.post("/obstacles/add")
async def add_obstacle(obstacle: Obstacle):
    obstacle = dict(obstacle)
    ws_obstacle = obstacle

    obstacle["game_id"] = ObjectId(obstacle["game_id"])
    added_obstacle = await obstacles_collection.insert_one(obstacle)
    obstacle["game_id"] = str(obstacle["game_id"])
    obstacle["_id"] = str(obstacle["_id"])
    await websocket_connection.broadcast({"event": "obstacle_added", "data": ws_obstacle}, game_id=str(ws_obstacle["game_id"]))
    return{
        "status": "ok",
        "detail": " Obstacle added successfully",
        "id": str(added_obstacle.inserted_id),
    }

@obstacles_router.get("/obstacles/{game_id}")
async def get_all_obstacles(game_id: str):
    try:
        game_object_id = ObjectId(game_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid game ID format")
    obstacles = await multiple_obstacles(obstacles_collection.find({"game_id": game_object_id}))
    for obstacle in obstacles:
        obstacle["id"] = str(obstacle["id"])
        obstacle["game_id"] = str(obstacle["game_id"])
    if obstacles:
        return obstacles
    
@obstacles_router.patch("/obstacles/new-pos/{obstacle_id}")
async def modify_pawn_pos(obstacle_id: str, obstacle_cords: ObstacleCords):
    try:
        obstacle_object_id = ObjectId(obstacle_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid obstacle ID format")
    obstacle = await obstacles_collection.find_one({"_id": obstacle_object_id})
    if not obstacle:
        raise HTTPException(status_code=400, detail="obstacle not found")
    result1 = await obstacles_collection.update_one(
        {"_id": obstacle_object_id},
        {"$set": {"pos_x": obstacle_cords.pos_x}},
    )
    result2 = await obstacles_collection.update_one(
        {"_id": obstacle_object_id},
        {"$set": {"pos_y": obstacle_cords.pos_y}},
    )

    await websocket_connection.broadcast({"event": "pawn_position_updated", "pawn_id": obstacle_id, "data": obstacle_cords.dict()}, game_id=str(obstacle["game_id"]))
    
    if result1.matched_count == 0 or result2.matched_count == 0:
        raise HTTPException(status_code=404, detail="Obstacle not found")
    return {
        "status": "ok",
        "detail": " obstacle coordinates updated successfully"
    }