from fastapi import APIRouter, HTTPException, status
from models.users import NewUser, User, UserSignIn

user_router = APIRouter(
    tags=["Users"]
)


users = {}

@user_router.post("/signup")
async def sign_new_user(data: NewUser):
    if data.email in users:
        raise HTTPException(status_code=status.HTTPException, detail = "User with supplied username already exists")
    users[data.email] = data
    return {"message": "User successfully registered"}


@user_router.post("/sigin")
async def sign_user_in(user: UserSignIn):
    if users[user.email] not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User does not exist")
    
    if users[user.email].password != user.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Wrong credentials passed")
    
    return {"message": "User signed in successfully "}