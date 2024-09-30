def individual_user(user) -> dict:
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"]
    }