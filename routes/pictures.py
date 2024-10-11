from models.pictures import Picture
from config.database import pictures_collection
from schema.schemas import individual_picture
from config.auth import get_current_user

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, status

pictures_router = APIRouter()

@pictures_router.post("/pictures/add")
async def add_new_picture(picture: Picture):
    picture = dict(picture)
    try:
        picture["game_id"] = ObjectId(picture["game_id"])
    except:
        raise HTTPException(status_code=400, detail="Invalid game ID format")
    await pictures_collection.insert_one(picture)
    return{
        "status": "ok",
        "message": "Picture added successfully",
    }

@pictures_router.get("/pictures/get-one/{picture_id}")
async def get_picture(picture_id: str):
    try:
        picture_object_id = ObjectId(picture_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid picture ID format")
    db_picture = await pictures_collection.find_one({"_id": picture_object_id})
    db_picture["_id"] = str(db_picture["_id"])
    db_picture["game_id"] = str(db_picture["game_id"])
    return db_picture

@pictures_router.get("/pictures/get-many/{game_id}")
async def get_picture(game_id: str):
    try:
        game_object_id = ObjectId(game_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid game ID format")
    db_pictures = await pictures_collection.find({"game_id": game_object_id}).to_list()
    for db_picture in db_pictures:
        db_picture["_id"] = str(db_picture["_id"])
        db_picture["game_id"] = str(db_picture["game_id"])
    return db_pictures

@pictures_router.delete("/pictures/delete/{picture_id}")
async def delete_picture(picture_id: str):
    try:
        picture_object_id = ObjectId(picture_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid picture ID format")
    pictures_collection.delete_one({"_id": picture_object_id})
    return{
        "status": "ok",
        "message": "Picture deleted successfully",
    }