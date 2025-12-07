from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users
from app.core.database import init_db
from app.core.config import settings

app = FastAPI(title="Prephoria MVP")


@app.on_event("startup")
def on_startup():
    init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include your routers
app.include_router(auth.router)
app.include_router(users.router)
