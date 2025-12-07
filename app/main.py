from fastapi import FastAPI
from app.routers import auth, users
from app.core.database import init_db

app = FastAPI(title="Prephoria MVP")


@app.on_event("startup")
def on_startup():
    init_db()


# Include your routers
app.include_router(auth.router)
app.include_router(users.router)
