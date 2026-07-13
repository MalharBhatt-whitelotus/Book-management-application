from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from database import Base, engine, AsyncSessionLocal

# Import models so SQLAlchemy registers tables
from models.book import Book
from models.user import User
from models.bill import Bill

# Import routers
from routes.user_routes import router as user_router
from routes.book_routes import router as book_router
from routes.bills_routes import router as bills_router

from services.user_services import UserService

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# CORS for local frontend/backend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja templates
templates = Jinja2Templates(directory="frontend/templates")

# Optional static folder mount
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    """
    Create DB tables and ensure default admin exists.
    """
    Base.metadata.create_all(bind=engine)

    db = AsyncSessionLocal()
    try:
        UserService.create_default_admin_if_not_exists(db)
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/")
def home(request: Request):
    """
    Render login/registration page
    """
    return templates.TemplateResponse(request=request,name="login_registration.html"
    )


@app.get("/admin")
def admin_page(request: Request):
    return templates.TemplateResponse(request=request, name="admin_dashboard.html")


@app.get("/dashboard")
def user_page(request: Request):
    return templates.TemplateResponse(request=request, name="user_dashboard.html")


# API routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(book_router, prefix="/books", tags=["Books"])
app.include_router(bills_router, prefix="/bills", tags=["Bills"])