from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse, Response

from app.constants import BASE_PATH
from app.crud.users import authenticate_user
from app.db.session import get_db
from app.schemas.users import UserLogin
from app.views.auth.forms import LoginForm

templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
router = APIRouter()
app = FastAPI()


@router.get("/login/")
def login(request: Request) -> Response:
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)) -> Response:
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user = UserLogin(
                email=form.email, password=form.password
            )
            current_user = authenticate_user(email=user.email, password=user.password, db=db)
            response = RedirectResponse(request.url_for('list'), status_code=302)
            data = {'email': current_user.email, 'role': current_user.role,
                    'is_superuser': current_user.is_superuser}
            request.session.update(data)
            return response
        except HTTPException as e:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append(e.detail)
            return templates.TemplateResponse("auth/login.html", form.__dict__, status_code=e.status_code)
    return templates.TemplateResponse("auth/login.html", form.__dict__)


@router.get("/logout/", response_class=HTMLResponse)
def logout(request: Request) -> Response:
    response = RedirectResponse(request.url_for('login'), status_code=302)
    request.session.clear()
    return response
