from fastapi import APIRouter

entry_router = APIRouter()

@entry_router.get("/")
def entry():
    res = {
        "status" : "ok" ,
        "message" : "Api is runinng"
    }
    return res