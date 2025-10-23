from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# proper connection

# PostgreSQL connection string

# db_url = (
#     f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
#     f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# )

# Mysql connection string
db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpass")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'

# engine = create_engine(db_url, connect_args={"client_flag": CLIENT.MULTI_STATEMENTS})
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


# create table to our database (backend_db)

create_users = text("""
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);
""")

create_courses = text("""
CREATE TABLE IF NOT EXISTS courses(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    title VARCHAR(100) NOT NULL,
    level VARCHAR(100) NOT NULL
);
""")

create_enrollment = text("""
CREATE TABLE IF NOT EXISTS enrollments(
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    courseId INT,
    FOREIGN KEY (userId) REFERENCES users(id),                     
    FOREIGN KEY (courseId) REFERENCES courses(id)                     
);
""")

db.execute(create_users)
db.execute(create_courses)
db.execute(create_enrollment)
print("Tables created successfully")