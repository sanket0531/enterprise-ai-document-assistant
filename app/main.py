from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Document Assistant",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to Enterprise AI Document Assistant"}


@app.get("/health")
def health():
    return {"status": "healthy"}