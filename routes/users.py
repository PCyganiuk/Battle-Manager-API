from fastapi import APIRouter, HTTPException
from models.users import User, UserLogin
from config.database import users_collection
from schema.schemas import individual_user, multiple_users
from config.auth import ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context, create_access_token

from datetime import timedelta, datetime
from bson import ObjectId

users_router = APIRouter()

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
# login and authorize user
@users_router.post("/users/login")
async def login_user(user:UserLogin):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=400,detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400,detail="Wrong password", headers={"WWW-Authenticate": "Bearer"})
    # TODO here add https://youtu.be/YpvcqxYiyNE?si=q-hEBQgyzw38_wWy&t=321 what is there
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return{
        "access_token": access_token,
        "token_type": "bearer"
    }