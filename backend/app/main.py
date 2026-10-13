from fastapi import FastAPI

app = FastAPI(title="Document AI")


@app.get("/health")
def health_check():
    return {"status": "ok"}
