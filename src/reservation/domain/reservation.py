from auth.user import User
from backbone.base_class import Base
import sqlalchemy.orm as sao
import sqlalchemy as sa

from reservation.domain.table import Table


class Reservation(Base):
    __tablename__ = "reservation"
    table_id: sao.Mapped[int] = sao.mapped_column(sa.ForeignKey("table.id"))
    seat_count: sao.Mapped[int] = sao.mapped_column(sa.Integer)
    total_price: sao.Mapped[int] = sao.mapped_column(sa.Integer)
    created_by_id: sao.Mapped[int] = sao.mapped_column(sa.ForeignKey("user.id"))

    table: sao.Mapped["Table"] = sao.relationship("Table")
    created_by: sao.Mapped["User"] = sao.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "table": self.table.table_number,
            "seat_count": self.seat_count,
            "total_price": self.total_price,
            "created_by": self.created_by.username,
        }
