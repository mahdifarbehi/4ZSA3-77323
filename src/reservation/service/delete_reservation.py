from reservation.domain.reservation import Reservation
from unit_of_work import UnitOfWork
from backbone.base_exceptions import NotFoundException


def delete_reservation_handler(uow: UnitOfWork, reservation_id: int):
    with uow:
        reservation: Reservation = uow.main_repo.read_one(Reservation, reservation_id)
        if not reservation:
            raise NotFoundException(reservation_id)
        reservation.table.available_seats += reservation.seat_count
        uow.session.delete(reservation)
        uow.commit()
        return {"message": "Reservation canceled successfully"}
