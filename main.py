from fastapi import FastAPI

app = FastAPI(title="Weather Station Data Processor API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather Station Data Processor API"}

# --- TODO: Add your endpoints here ---
