from backbone.base_class import Base
import sqlalchemy.orm as sao
import sqlalchemy as sa


class Table(Base):
    __tablename__ = "table"
    table_number: sao.Mapped[str] = sao.mapped_column(sa.String(10), unique=True)
    available_seats: sao.Mapped[int] = sao.mapped_column(sa.Integer)
