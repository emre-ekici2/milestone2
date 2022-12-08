from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class Item(BaseModel):
    name: str


app = FastAPI()

engine = create_engine(
    f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
)
Session = sessionmaker(bind=engine)

@app.get("/user")
def get_user_name(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"

    try:
        session = Session()
    except Exception as e:
        return {"message": f"Failed to connect to the database: {e}"}

    try:
        result = session.execute("SELECT * FROM my_name")
        user_name = result.fetchone()[0]
        return {"name": user_name}
    except Exception as e:
        return {"message": f"Failed to run query: {e}"}
