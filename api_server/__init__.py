from fastapi import FastAPI, APIRouter
from . import view

app = FastAPI()

app.include_router(view.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)