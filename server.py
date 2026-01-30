from fastapi import FastAPI



app = FastAPI()


@app.get("/")
def Home():
    return {"where_am_i":"Home"}
