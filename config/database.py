import os
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(f'mongodb+srv://{os.getenv("mongodb_username")}:{os.getenv("mongodb_password")}@cluster0.c4gvw.mongodb.net/?retryWrites=true&w=majority&appName=cluster0')
db = client["Battle-manager"]
users_collection = db["Users"]
games_collection = db["Games"]
pawns_collection = db["Pawns"]
obstacles_collection = db["Obstacles"]