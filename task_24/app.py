from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import json
import os
from typing import Optional
load_dotenv()
file_path= "database.json"

app= FastAPI(title="Simple FastAPI App", version="1.0.0")

# load data function
def load_data():
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
    
# function to update(save) the json file
def update_database(data_to_update):
    with open(file_path, 'w') as f:
        json.dump(data_to_update,f, indent=4)
    return True

# Model for validation
class Item(BaseModel):
    name: str = Field(..., description="The name of the person")
    age: int = Field(..., ge=0, description="Age must be non-negative")
    track: str = Field(..., description="Their learning track or specialization")

class  OptionalItem(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None
    track: Optional[str]=None

#  endpoints

@app.get("/get-data")
def get_data():
    return load_data()

@app.post ("/create-data")
def create_data(req: Item):
    data= load_data()# first load data
    data.append(req.model_dump())
    update_database(data)
    return {"Message": "Data Received", "Data":data}
    
@app.put("/update-data/{id}")
def update_data(id:int, req:Item):
    data= load_data()# first load data
    data[id]=req.model_dump()
    update_database(data)
    return {"Message": "Data update", "Data":data}

@app.delete("/delete-data/{id}")
def delete_data(id:int):
    data= load_data()# first load data
    data.remove(data[id])
    if update_database(data):
        return {"Message": "Data deleted", "Data":data}


@app.patch("/update-data2/{id}")
def patch_data(id: int, req: OptionalItem):
    data= load_data()# first load data
    # Only update provided fields
    data[id].update(req.model_dump(exclude_unset=True))
    if update_database(data):
        return {"Message": "Partial update successful", "Data": data[id]}



if __name__=="__main__":
    uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))