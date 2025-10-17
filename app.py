from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional
import uvicorn
import json
import os
load_dotenv()

app= FastAPI(title="Simple FastAPI App", version="1.0.0")
file_path= "database.json"
# load data function
def load_data():
    if not os.path.exists(file_path):
        return []
    with open(file_path) as f:
        return json.load(f)
# function to update the json file
def update_database(data_to_update):
    if data_to_update:
        with open(file_path, 'w') as f:
            json.dump(data_to_update,f, indent=2)
            return True
    return False

class Item(BaseModel):
    name: str =Field(...)
    age:int = Field(...)
    track: str = Field(...)

class  OptionalItem(BaseModel):
    name: Optional[str]=None
    age: Optional[str]=None
    track: Optional[str]=None

# load data first 
data=load_data()

#  endpoints
@app.get("/", description="This endpoint just return a welcome message")
def root():
    return {"Message": "Welcome to my FastAPI App"}

@app.get("/get-data")
def get_data():
    return load_data()

@app.post ("/create-data")
def create_data(req: Item):
    data.append(req.model_dump())
    if update_database(data):
        return {"Message": "Data Received", "Data":data}
@app.put("/update-data/{id}")
def update_data(id:int, req:Item):
    data[id]=req.model_dump()
    if update_database(data):
        return {"Message": "Data update", "Data":data}

@app.delete("/delete-data/{id}")
def delete_data(id:int):
    data.remove(data[id])
    if update_database(data):
        return {"Message": "Data deleted", "Data":data}

@app.patch("/update-data2/{id}")
def path_data(id:int, req:OptionalItem):
    data[id]= req.model_dump()
    if update_database(data):
        return {"Message": "Data update", "Data":data}


if __name__=="__main__":
    uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))