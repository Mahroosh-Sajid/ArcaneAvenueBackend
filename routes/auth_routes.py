from fastapi import APIRouter, HTTPException

from models.auth_models import LoginForm, RegisterForm, AuthResponse
from database import test_collection
from pymongo.errors import DuplicateKeyError

auth_router = APIRouter()

FAKE_USER_DB = {
    "goober@gmai.com":{
        "email":"goober@gmai.com",
        "password": "test",
        "account_type":"buyer"
    }
}

@auth_router.get("/test")
def read_root():
    return {"auth": "test"}

@auth_router.post("/register", response_model=AuthResponse)
def register_user(form: RegisterForm):
    found_user=FAKE_USER_DB.get(form.email)
    print("User found was: ")
    print(found_user)
    if(found_user):
        raise HTTPException(
            status_code=403,
            details="User with this email already exists!"
        )
    
    user_dict=form.model_dump()
    FAKE_USER_DB[form.email]=user_dict
    print("New user database: ")
    print(FAKE_USER_DB)

    return AuthResponse(
        email=form.email,
        account_type=form.account_type
    )

@auth_router.post("/login", response_model=AuthResponse)
def login_user(form: LoginForm):
     found_user=FAKE_USER_DB.get(form.email)
    #  found_user_password=FAKE_USER_DB.get(form.password)
     print("User found was: ")
     print(found_user)
     if(found_user == None):
        raise HTTPException(
            status_code=401,
            detail="No user found. Invalid data: "
        )
     if(found_user["password"] != form.password):
         raise HTTPException(
            status_code=401,
            detail="Password doesnot match. Invalid Password: "
         )

     
     return AuthResponse(
        email=form.email,
        account_type=found_user["account_type"]
    )

from pydantic import BaseModel
class TestAdd( BaseModel):
    email:str
    description:str


@auth_router.post("/test_add")
def test_add(data:TestAdd):

    our_data_in_dictionary_format=data.model_dump();
    try:
        test_collection.insert_one(our_data_in_dictionary_format)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="This email already exists!"      
        )

    print("testing adding an item")

@auth_router.post("/test_find")
def test_find(data:TestAdd):

    result=test_collection.find_one({
        "email": data.email
    })

    print(result)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found "
        )
    return "found item" 
    