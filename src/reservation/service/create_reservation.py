from reservation.domain.reservation import Reservation
from reservation.domain.table import Table
from reservation.request_models import CreateReservationRequest
from unit_of_work import UnitOfWork
from project_config import SEAT_COUNT, SEAT_PRICE
from reservation.exceptions import NoAvailableTables

is_odd = lambda x: x % 2 == 1


def create_reservation_handler(
    user_id: int, uow: UnitOfWork, data: CreateReservationRequest
):
    fixed_people_count = (
        data.people_count + 1
        if is_odd(data.people_count)
        and (not is_odd(SEAT_COUNT) or data.people_count != SEAT_COUNT)
        else data.people_count
    )
    with uow:

        table = (
            uow.session.query(Table)
            .filter(
                Table.available_seats >= fixed_people_count,
            )
            .order_by(Table.available_seats.asc())
            .first()
        )

        if not table:
            raise NoAvailableTables()

        total_price = (
            (fixed_people_count - 1) * SEAT_PRICE
            if fixed_people_count == SEAT_COUNT
            else fixed_people_count * SEAT_PRICE
        )

        table.available_seats -= fixed_people_count

        reservation = Reservation(
            table_id=table.id,
            seat_count=fixed_people_count,
            total_price=total_price,
            created_by_id=user_id,
        )

        uow.session.add(reservation)
        uow.commit()
        return reservation.to_dict()
