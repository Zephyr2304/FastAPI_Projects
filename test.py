from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def First_api():
    return{"response":"Status OK"}