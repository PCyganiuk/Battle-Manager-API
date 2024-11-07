from fastapi import APIRouter

entry_router = APIRouter()

@entry_router.get("/")
def entry():
    res = {
        "status" : "ok" ,
        "message" : "Hey you are finally awake The Api is already runinng"
    }
    return res