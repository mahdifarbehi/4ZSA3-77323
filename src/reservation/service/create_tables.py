from unit_of_work import UnitOfWork
from reservation.domain.table import Table
from project_config import TABLE_COUNT, SEAT_COUNT


def create_tables_handler(uow: UnitOfWork):
    with uow:
        for i in range(TABLE_COUNT):
            table = Table(table_number=f"table{i}", available_seats=SEAT_COUNT)
            uow.session.add(table)
        uow.commit()
        return "Setup is done"
