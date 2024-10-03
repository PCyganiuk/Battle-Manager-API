import datetime
from fastapi import APIRouter, HTTPException
from models.users import User, UserLogin
from config.database import users_collection
from schema.schemas import individual_user, multiple_users
from bson import ObjectId
from passlib.context import CryptContext

users_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# fetch all users
@users_router.get("/users")
async def get_users():
    users = await multiple_users(users_collection.find({}))
    return users

# register new user
@users_router.post("/users/register")
async def post_user(user:User):
    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="account with that email already exists")
    user = dict(user)
    user["password"] = pwd_context.hash(user["password"])
    user["join_date"] = str(datetime.date.today())
    await users_collection.insert_one(user)
    return{
        "status": "ok",
        "message": "User added successfully",
    }
#TODO add JWT authentication to prod
@users_router.post("/users/login")
async def login_user(user:UserLogin):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=400,detail="User not found")
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400,detail="Wrong password")
    return{
        "status": "ok",
        "message": "User logged in"
    }