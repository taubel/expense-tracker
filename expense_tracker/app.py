from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return "I'm just a placeholder"
