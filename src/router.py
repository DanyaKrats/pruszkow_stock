from fastapi import APIRouter

base_router = APIRouter(
    tags=["Main Page"],
)

@base_router.get("/", response_model=dict)
def read_root():
    return {"message": "Hello, FastAPI!"}
