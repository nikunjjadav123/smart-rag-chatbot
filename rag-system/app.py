from fastapi import FastAPI
from dotenv import load_dotenv
from vectorstore.index_builder import rebuild_index


app = FastAPI()

@app.post("/rebuild-index")
def rebuild_index():
    return {"message": "Index rebuilt successfully"}

