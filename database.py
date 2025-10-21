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

# create table to our database (backend_db)

# create_users= text("""
# CREATE TABLE IF NOT EXIST users(
#     id int AUTO_INCREMENT PRIMARY KEY, 
#     name VARCHAR(100) not null,
#     email varchar(100) not null,
#     password varchar(100) not null
#                         );

# """)

# create_courses= text("""
# CREATE TABLE IF NOT EXIST courses(
#     id int AUTO_INCREMENT PRIMARY KEY, 
#     title VARCHAR(100) NOT NULL,
#     level VARCHAR(100) NOT NULL
#                         );

# """)

# create_enrollment=("""          
# CREATE TABLE IF NOT EXIST enrollments(
#     id int AUTO_INCREMENT PRIMARY KEY,
#     userId INT,
#     courseId INT,
#     FOREIGN KEY (userId) REFERENCES users(id),                     
#     FOREIGN KEY (courseId) REFERENCES courses(id)                     
#                         );
# """)

# db.execute(create_users)
# db.execute(create_courses)
# db.execute(create_enrollment)
# print("Tables created successfully")