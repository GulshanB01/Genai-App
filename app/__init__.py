from fastapi import FastAPI

app = FastAPI(title="Smart Notes AI Backend")

@app.get("/")
def root():
    return {"message": "Smart Notes API is running!"}