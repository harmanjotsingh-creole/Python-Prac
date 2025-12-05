from fastapi import FastAPI

app = FastAPI(title="Log Processor API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Log Processor API"}

# --- TODO: Add your endpoints here ---

