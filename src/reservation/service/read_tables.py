from reservation.domain.table import Table
from unit_of_work import UnitOfWork


def read_tables_handler(uow: UnitOfWork):
    with uow:
        tables: list[Table] = uow.main_repo.read_all(Table)
        return [table.to_dict() for table in tables]
