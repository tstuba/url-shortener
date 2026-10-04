from fastapi import FastAPI

app = FastAPI()


@app.get("/health-check")
def chealt_check() -> dict[str, str]:
    return {"status": "ok"}
