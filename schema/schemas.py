def individual_user(user) -> dict:
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "join_date": user["join_date"]
    }

async def multiple_users(users) -> list:
    return [individual_user(user) async for user in users]