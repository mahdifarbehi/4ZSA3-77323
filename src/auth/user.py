import sqlalchemy.orm as sao

from backbone.base_class import Base


class User(Base):
    __tablename__ = "user"

    username: sao.Mapped[str] = sao.mapped_column(unique=True)
    password: sao.Mapped[str]
