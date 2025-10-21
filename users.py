import bcrypt
from database import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import uvicorn
import pandas as pd

load_dotenv()

app=FastAPI(title="Simple App", version="1.0.0")

class simple(BaseModel):
    name: str = Field(..., example= "Saheed Olayemi")
    email: str= Field(..., example= "ola@gmail.com")
    password: str=Field(..., example= "ola121")

class logindetail(BaseModel):
    email: str= Field(..., example= "ola@gmail.com")
    password: str=Field(..., example= "ola121")

@app.get("/", description="This endpoint just return a welcome message")
def root():
    return {"Message": "Welcome to my FastAPI App"}

@app.post("/signup")
def signUp(input:simple):
    try:
        duplicate_query=text(""" SELECT * FROM users WHERE email=:email """)
        existing=db.execute(duplicate_query,{"email":input.email})
        if existing:
            print("Email already exist")
            # raise HTTPException(status_code=400, detail="Email already exist")
        
        query= text("""
            INSERT INTO users (name, email, password)
        VALUES(:name, :email, :password);
        """)
        # hashing password
        salt=bcrypt.gensalt()
        hashedpassword=bcrypt.hashpw(input.password.encode('utf-8'), salt)
        print(hashedpassword)

        # mapping data
        data= {"name":input.name, "email":input.email, "password":hashedpassword}
        db.execute(query,data)
        db.commit()
        return {"Message": "User created sucessfuly", "data":{"name":input.name, "email":input.email}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

# load used details
@app.get("/get-userdata/{id}")
def get_userdata(id:int):
    try:
        query=text(""" SELECT * FROM users WHERE id=:id """)
        db_user=db.execute(query,{"id":id}).fetchall()
        # db_user=pd.DataFrame(db_user)
        if db_user:
           return{"message":"Record fetch successfilly" ,"data":db_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    
if __name__=="__main__":
     uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))

