import bcrypt
from database import db
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import uvicorn
import pandas as pd
from middleware import create_token, verify_token

load_dotenv()

app=FastAPI(title="Simple App", version="1.0.0")

token_time=int(os.getenv("token_time"))
               
class RegDetails(BaseModel):
    name: str = Field(..., example= "Saheed Olayemi")
    email: str= Field(..., example= "ola@gmail.com")
    password: str=Field(..., example= "ola121")
    userType: str = Field(..., example="student")
    gender: str= Field(..., examples="male" )
class LoginRequest(BaseModel):
    email: str = Field(..., example="ola@gmail.com")
    password: str = Field(..., example="ola124")

class Course_details(BaseModel):
    title: str= Field(..., example="Computer operation")
    level: str= Field(..., example="300 level")

class logindetail(BaseModel):
    email: str= Field(..., example= "ola@gmail.com")
    password: str=Field(..., example= "ola121")

@app.get("/")
def root():
    return {"Message": "Welcome to my FastAPI App"}

@app.post("/signup")
def signUp(input:RegDetails):
    try:
        duplicate_query=text(""" SELECT * FROM users WHERE email=:email """)
        existing=db.execute(duplicate_query,{"email":input.email})
        if existing:
            # print("Email already exist")
            raise HTTPException(status_code=400, detail="Email already exist")
        
        query= text("""
            INSERT INTO users (name, email, password,userType, gender)
        VALUES(:name, :email, :password, :userType,:gender);
        """)
        # hashing password
        salt=bcrypt.gensalt()
        hashedpassword=bcrypt.hashpw(input.password.encode('utf-8'), salt)

        # mapping data
        data= {"name":input.name, "email":input.email, "password":hashedpassword, "userType":input.userType,"gender":input.gender}
        db.execute(query,data)
        db.commit()
        return {"Message": "User created sucessfuly", "data":{"name":input.name, "email":input.email,"userType":input.userType }}
    except Exception as e:
        # db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# load user details my version
@app.get("/get-userdata/{id}")
def get_userdata(id:int):
    user_detail=[]
    try:
        query=text(""" SELECT * FROM users WHERE id=:id """)
        db_user=db.execute(query,{"id":id}).fetchall()
        # db_user=pd.DataFrame(db_user)
        if db_user:
           user_detail= db_user
           print(user_detail)
           return{"message":"Record fetch successfilly", "data":user_detail}
    except Exception as e:
        # db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
# load user details my version  

# endpoint for login
@app.post("/login")
def login(input: LoginRequest):
    try:
        query=text(""" SELECT * FROM users WHERE email=:email """)
        result = db.execute(query,{"email":input.email}).fetchone()
        if not result:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        verified_password=bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))
        if not verified_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        encoded_token= create_token(details={
            "email":result.email,
            "userTpye": result.userType
            }, expiry=token_time)
        return{"message":"login Successful", "token": encoded_token}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/courses")
def addcourse(input:Course_details, user_data = Depends(verify_token)):
    try:
        print(user_data)
        if user_data.userType!="admin":
            raise HTTPException(status_code=401, detail="Your are not authorized to add a course")

        query= text("""INSERT INTO course (title, level) VALUES(:title, :level)""")
        db.execute(query,{"title":input.title, "level":input.level})
        db.commit()
        return {"Message": "Course created sucessfuly", "data":{"title":input.title, "level":input.level }}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

if __name__=="__main__":
    uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))

