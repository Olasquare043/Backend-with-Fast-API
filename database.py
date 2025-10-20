from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# db_url=dialect+driver://dbuser;dbpass;dbhost;dbport;dbname
db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpass")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'

engine=create_engine(db_url)
session=sessionmaker(bind=engine)
db=session()

query=text("SELECT * FROM user")
db_users= db.execute(query).fetchall()
user_df= pd.DataFrame(db_users)
user_df
# for user in user_df:
#     print(f'{user["id"]}      {user["name"]}      {"email"}')