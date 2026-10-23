from fastapi import FastAPI
from app.routers import files

app = FastAPI(title="Document AI")

# Router'ni ulash
app.include_router(files.router, prefix="/api", tags=["files"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
