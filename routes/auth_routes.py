from fastapi import APIRouter 
from database import users
from models.auth_models import RegisterForm
from models.auth_models import LoginForm
from pymongo.errors import DuplicateKeyError
from fastapi import APIRouter, HTTPException



auth_router = APIRouter() 


@auth_router.get("/")
def test_auth_router():
    return {"status": "works"}


@auth_router.get("/all")
def get_all_users():
    result =users.find().to_list()
    for user in result:
        user["_id"] =str(user["_id"])
    print(result)
    return {"all_users": result}


@auth_router.post("/register")
def register_user(form: RegisterForm):

    try:
       users.insert_one({
           "email": form.email,
           "password": form.password,
           "account_type": form.account_type
       })

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            details="account already exists"
        )

    return {"status": "success"}


@auth_router.post("/login")
def login_user(form: LoginForm):

    found_user = users.find_one({"email": form.email})
    if found_user == None:
         raise HTTPException(
            status_code=401,
            detail="No user found. Invalid data!"
        )
    
    if(found_user["password"] != form.password):
         raise HTTPException(
            status_code=401,
            detail="Password doesn't match. Invalid Password"
         )

    return {
        "email": found_user["email"],
        "account_type": found_user["account_type"]
        }

