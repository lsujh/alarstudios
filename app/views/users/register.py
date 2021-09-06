from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse, Response

from app.constants import BASE_PATH
from app.crud.users import create_new_user
from app.db.session import get_db
from app.schemas.users import UserCreate
from app.views.users.forms import UserCreateForm

templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
router = APIRouter()


@router.get("/register/")
def register(request: Request) -> Response:
    return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)) -> Response:
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user = UserCreate(
                email=form.email, password=form.password
            )
            create_new_user(user=user, db=db)
            return RedirectResponse(request.url_for('login'), status_code=302)
        except HTTPException:
            form.__dict__.get("errors").append("Duplicate or invalid email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)
