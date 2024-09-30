from fastapi import APIRouter

from models.users import User
from config.database import users_collection
from schema.schemas import individual_user
from bson import ObjectId

router = APIRouter()

@router.get("/users")
async def get_users():
    users_cursor = users_collection.find({})
    users = []
    async for user in users_cursor:
        users.append(individual_user(user))
    return users