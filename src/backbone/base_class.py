from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as sao

from backbone.base_exceptions import ValueErrorException


class Base(sao.DeclarativeBase):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    created_at: sao.Mapped[datetime] = sao.mapped_column(default=sa.func.now())
    ignored_fields: list = ["id", "created_at"]
    field_defaults: dict = {}

    @classmethod
    def create(cls, **kwargs):
        try:
            return cls(**kwargs)
        except TypeError as e:
            raise ValueErrorException(detail=str(e))

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in sa.inspection.inspect(self).mapper.column_attrs
        }
