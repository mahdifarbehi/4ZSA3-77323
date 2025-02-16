from typing import Annotated
from auth.request_models import CreateUserRequest
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.service.authentication import authenticate_user
from auth.service.create_user import create_user_handler
from auth.service.user_dto import UserDTO
from auth.service.utils import get_current_user
from unit_of_work import UnitOfWork, get_uow


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login_api(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UnitOfWork = Depends(get_uow),
):
    token = authenticate_user(
        uow=uow, username=form_data.username, password=form_data.password
    )
    return token


@router.post("/user")
def create_user_api(
    data: CreateUserRequest,
    uow: UnitOfWork = Depends(get_uow),
):
    result = create_user_handler(data=data, uow=uow)
    return result


@router.get("/me")
def get_current_user_api(user: Annotated[UserDTO, Depends(get_current_user)]):
    return user
