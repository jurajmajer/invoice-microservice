import uvicorn

from main import app

app  # just because auto-clean-up deletes previous import on save

if __name__ == "__main__":
    uvicorn.run("debug:app", host="0.0.0.0", port=8000, workers=1, reload=True)
