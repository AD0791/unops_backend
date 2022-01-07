import os
from fastapi import (
    FastAPI,
    Body,
    HTTPException,
    status,
    Depends
)
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
import json
from pydantic import EmailStr
from typing import Optional
from models.user import User, RegisterUser, RegisterAdmin
from models.token import Token, TokenData
from typing import  List
import pymongo as pm
from db import db
from db.user import (
    createUser,
    getUsers,
    getUserByEmail,
    getUserByUsername,
    updateUser,
    updateUser_byEmail,
    delUserByEmail,
    delUserByUsername,
    registerUser,
    registerAdmin
)
from utils.data import dataInToDataOut
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from core.config import settings
from core.hashing import Hasher
from routers.form_data import router as data_router
from routers.questions import router as questions_router
from routers.form import router as form_router
from dependencies import oauth2_scheme, get_current_user_from_token, authenticate_user,create_access_token


app = FastAPI(title=settings.PROJECT_TITLE, description=settings.PORJECT_DESCRIPTION, version=settings.PROJECT_VERSION, docs_url=settings.DOCS_URL)

app.include_router(data_router)
app.include_router(questions_router)
app.include_router(form_router)
_forms = db["forms"]
_forms.create_index([("type",pm.ASCENDING),("name",pm.ASCENDING)], unique=True,name="form_index")


# @app.get("/", tags=['Home'])
# async def root():
#     return {"message": "Please write /docs into the browser path to enter to openapi"}




################ Admin


@app.get("/admin/user/{username}", response_model=User,response_description=settings.GET_USER_DESCRIPTION, summary=settings.GET_USER_SUMMARY, status_code=status.HTTP_201_CREATED, tags=['USER'])
async def get_userByUsername(username:str)->User:
    _user = await getUserByUsername(username)
    if _user:
        return _user
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Something went wrong wwith {username}")





@app.post("/admin/createUser", response_model=User ,response_description=settings.CREATE_USER_DESCRIPTION, summary=settings.CREATE_USER_SUMMARY, status_code=status.HTTP_201_CREATED, tags=['USER'])
async def post_user(user:User)->User:
    _user = user.dict()
    _resUser = await createUser(_user)
    if _resUser:
        return _resUser
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Something went wrong")



@app.get("/admin/user/{email}/", response_model=User, response_description=settings.GET_USER_DESCRIPTION, summary=settings.GET_USER_SUMMARY,status_code=status.HTTP_201_CREATED, tags=['USER'])
async def get_userByEmail(email: EmailStr)->User:
    _user = await getUserByEmail(email)
    if _user:
        return _user
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Something went wrong wwith {email}")



@app.get('/admin/users', response_model=List[User], response_description=settings.GET_USERS_DESCRIPTION, summary=settings.GET_USERS_SUMMARY,status_code=status.HTTP_201_CREATED, tags=['USER'])
async def get_users()->List[User]:
    _users = await getUsers()
    if _users:
        return _users
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Something went wrong")



@app.put("/admin/update_user/{username}", response_model=User,response_description=settings.UPDATE_USER_DESCRIPTION, summary=settings.UPDATE_USER_SUMMARY, status_code=status.HTTP_201_CREATED,  tags=['USER'])
async def put_user(username:str,email:EmailStr,password:str, is_active:Optional[bool], is_superUser:Optional[bool])->User:
    _user = await updateUser(username,email,password,is_active,is_superUser)
    if _user:
        return _user
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Something went wrong with {username}")


@app.put("/admin/update_user/{email}/", response_model=User,response_description=settings.UPDATE_USER_DESCRIPTION, summary=settings.UPDATE_USER_SUMMARY, status_code=status.HTTP_201_CREATED,  tags=['USER'])
async def update_user(username:str,email:EmailStr,password:str, is_active:Optional[bool], is_superUser:Optional[bool])->User:
    _user = await updateUser_byEmail(username,email,password,is_active,is_superUser)
    if _user:
        return _user
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Something went wrong with {email}")



@app.delete("/admin/delete_user/{email}/", response_description=settings.DELETE_USER_DESCRIPTION, summary=settings.DELETE_USER_SUMMARY, status_code=status.HTTP_201_CREATED, tags=['USER'])
async def delete_userByEmail(email:EmailStr)-> dict:
    _userdeleted = await delUserByEmail(email)
    if _userdeleted:
        return {"Message": f"the user with the {email} has been deleted" }
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Something went wrong with {email}")



@app.delete("/admin/delete_user/{username}", response_description=settings.DELETE_USER_DESCRIPTION, summary=settings.DELETE_USER_SUMMARY, status_code=status.HTTP_201_CREATED, tags=['USER'])
async def delete_userByUsername(username:str)->dict:
    _userdeleted = await delUserByUsername(username)
    if _userdeleted:
        return {"Message": f"the user with the {username} has been deleted" }
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Something went wrong with {username}")






@app.post('/register', response_model=RegisterUser, response_description=settings.REGISTRATION_DESCRIPTION, summary=settings.REGISTRATION_SUMMARY, status_code=status.HTTP_201_CREATED, tags=['Register'])
async def register(user: RegisterUser)->RegisterUser:
    _user = user.dict()
    _resUser = await registerUser(_user)
    if _resUser:
        return _resUser
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Something went wrong")



@app.post('/admin/register', response_model=RegisterAdmin, response_description=settings.REGISTER_ADMIN_DESCRIPTION, summary=settings.REGISTER_ADMIN_SUMMARY, status_code=status.HTTP_201_CREATED, tags=['Register'])
async def register_admin(admin: RegisterAdmin)->RegisterAdmin:
    _user = admin.dict()
    _resUser = await registerAdmin(_user)
    if _resUser:
        return _resUser
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Something went wrong")







