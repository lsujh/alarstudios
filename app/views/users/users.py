from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, Response

from app.constants import BASE_PATH
from app.crud.users import create_new_user, delete_user, get_user, list_users, update_user
from app.db.session import get_db
from app.schemas.users import UserAddUpdate, UserCreate
from app.views.users.forms import UserUpdateForm

templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
router = APIRouter()


@router.get("/")
async def list(request: Request, db: Session = Depends(get_db)) -> Response:
    current_user = request.session
    if current_user:
        users = list_users(db)
        return templates.TemplateResponse(
            "users/list-users.html", {"request": request, "users": users, 'current_user': current_user})
    return RedirectResponse(request.url_for('login'), status_code=302)


@router.get("/users/{id}/")
async def update(request: Request, id: int, db: Session = Depends(get_db)) -> Response:
    form = UserUpdateForm(request)
    try:
        user = get_user(id=id, db=db)
        form.__dict__.update(email=user.email, role=user.role)
        response = templates.TemplateResponse("users/update-user.html", {"request": request, 'form': form})
        return response
    except HTTPException:
        return templates.TemplateResponse("users/update-user.html", {"request": request, 'form': form})


@router.post("/users/{id}/")
async def update(request: Request, id: int, db: Session = Depends(get_db)) -> Response:
    form = UserUpdateForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user = UserAddUpdate(email=form.email, role=form.role)
            update_user(id=id, db=db, user=user)
            return RedirectResponse(request.url_for('list'), status_code=302)
        except HTTPException:
            form.__dict__.get("errors").append("Duplicate email")
            return templates.TemplateResponse("users/update-user.html", {'request': request, 'form': form})
    return templates.TemplateResponse("users/update-user.html", {'request': request, 'form': form})


@router.get("/users/")
def add_user(request: Request) -> Response:
    form = UserUpdateForm(request)
    return templates.TemplateResponse("users/add-user.html", {"request": request, 'form': form})


@router.post("/users/")
async def add_user(request: Request, db: Session = Depends(get_db)) -> Response:
    form = UserUpdateForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user = UserCreate(
                email=form.email, password=form.email, role=form.role
            )
            create_new_user(user=user, db=db)
            return RedirectResponse(request.url_for('list'), status_code=302)
        except HTTPException:
            form.__dict__.get("errors").append("Duplicate email")
            return templates.TemplateResponse("users/add-user.html", form.__dict__)
    return templates.TemplateResponse("users/add-user.html", form.__dict__)


@router.delete("/users/{id}/")
async def delete(request: Request, id: int, db: Session = Depends(get_db)) -> Response:
    try:
        delete_user(id=id, db=db)
        return RedirectResponse(request.url_for('list'), status_code=302)
    except HTTPException:
        return templates.TemplateResponse("auth/login.html", {"request": request})
