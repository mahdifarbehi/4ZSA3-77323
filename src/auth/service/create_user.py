from sqlalchemy.exc import IntegrityError
from auth.request_models import CreateUserRequest
from auth.user import User
from backbone.base_exceptions import DuplicateException
from backbone.base_validators import BaseValidator
from unit_of_work import UnitOfWork


def create_user_handler(uow: UnitOfWork, data: CreateUserRequest):
    with uow:
        user = User(**data.model_dump())

        BaseValidator.username(user.username)

        uow.session.add(user)

        try:
            uow.commit()
            user_dict = user.to_dict()
            user_dict.pop("password", None)
            return user_dict
        except IntegrityError:
            uow.rollback()
            raise DuplicateException(detail="User already exists")
