from fastapi import FastAPI, Depends, HTTPException, Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime

# importing my own module

from .models import User,TaskLog,Base
from .schemas import CreateUser
from .database import SessionLocal, engine, Base
from .auth import create_access_token
from .security import hash_password, verify_password

# Initialize App and Templates
app = FastAPI()
# -------------------------------------------------------
# tracker table connect to DB
Base.metadata.create_all(bind=engine)
#--------------------------------------------------------
# templates directory (project_root/frontend)
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "frontend"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# mount static (images, css if any) - frontend/static
STATIC_DIR = TEMPLATES_DIR / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# create database tables
Base.metadata.create_all(bind=engine)

# This gives each route access to the database.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This enables JWT-based authentication for protected routes.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# These serve your frontend pages
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/workout", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("workout.html", {"request": request})

@app.get("/chest", response_class=HTMLResponse)
def chest_page(request: Request):
    return templates.TemplateResponse("chest.html", {"request": request})

@app.get("/arms", response_class=HTMLResponse)
def arms_page(request: Request):
    return templates.TemplateResponse("arms.html", {"request": request})

@app.get("/sixpack", response_class=HTMLResponse)
def sixpack_page(request: Request):
    return templates.TemplateResponse("sixpack.html", {"request": request})

@app.get("/shoulder", response_class=HTMLResponse)
def shoulder_page(request: Request):
    return templates.TemplateResponse("shoulder.html", {"request": request})

@app.get("/lowerBody", response_class=HTMLResponse)
def lowerbody_page(request: Request):
    return templates.TemplateResponse("lowerbody.html", {"request": request})

@app.get("/fullBody", response_class=HTMLResponse)
def fullbody_page(request: Request):
    return templates.TemplateResponse("fullbody.html", {"request": request})
#---------------------------------------------------------------------------------------------------
# creating tracker get method
@app.get("/tracker", response_class=HTMLResponse)
def table(request: Request, db: Session = Depends(get_db)):
    logs = db.query(TaskLog).order_by(TaskLog.timestamp.desc()).all()
    return templates.TemplateResponse("tracker.html", {"request": request, "logs": logs})

#----------------------------------------------------------------------------------------------------



# post methods
@app.post("/register")
def register(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(name=user.name, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User '{new_user.name}' registered successfully"}

# Login Route
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.name})
    return {"access_token": token, "token_type": "bearer"}
#-------------------------------------------------------------------------------------------
# Tracker adding data
# task add by use buttons
@app.post("/log-task")
def log_task(task: str = Form(...), db: Session = Depends(get_db)):
    now = datetime.now()
    log = TaskLog(
        date=now.strftime("%d-%m-%Y"),
        time=now.strftime("%H:%M"),
        task=task
    )
    db.add(log)
    db.commit()
    return RedirectResponse(url="/workout", status_code=303)
# delete Tracker
@app.post("/delete-task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return RedirectResponse(url="/tracker", status_code=303)
