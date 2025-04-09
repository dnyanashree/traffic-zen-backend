from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from api.routes import users, security_routes
from db.config import startup,shutdown



@asynccontextmanager
async def lifespan(app: FastAPI):   
    startup()
    yield

    shutdown()
    
app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(security_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Traffic-Zen application!"}

if __name__ == "__main__":
    
    uvicorn.run("main:app",reload=True)