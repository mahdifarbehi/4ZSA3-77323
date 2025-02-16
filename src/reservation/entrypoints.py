from typing import Annotated
from fastapi import APIRouter, Depends
from auth.service.user_dto import UserDTO
from auth.service.utils import get_current_user
from reservation.request_models import CreateReservationRequest
from reservation.service.create_reservation import create_reservation_handler
from reservation.service.create_tables import create_tables_handler
from reservation.service.delete_reservation import delete_reservation_handler
from reservation.service.read_tables import read_tables_handler
from unit_of_work import get_uow, UnitOfWork

router = APIRouter()


@router.post("/tables")
def create_tables(uow: UnitOfWork = Depends(get_uow)):
    return create_tables_handler(uow=uow)


@router.get("/tables")
def read_tables(uow: UnitOfWork = Depends(get_uow)):
    return read_tables_handler(uow=uow)


@router.post("/book")
def create_reservation(
    data: CreateReservationRequest,
    user: Annotated[UserDTO, Depends(get_current_user)],
    uow: UnitOfWork = Depends(get_uow),
):
    return create_reservation_handler(user_id=user.id, uow=uow, data=data)


@router.delete("/cancel/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    user: Annotated[UserDTO, Depends(get_current_user)],
    uow: UnitOfWork = Depends(get_uow),
):
    return delete_reservation_handler(uow=uow, reservation_id=reservation_id)
