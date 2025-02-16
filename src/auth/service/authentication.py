import jwt
from auth.user import User
from backbone.base_exceptions import UnauthorizedException
from unit_of_work import UnitOfWork
from auth.service.utils import SECRET_KEY, ALGORITHM


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(uow: UnitOfWork, username: str, password: str) -> str:
    with uow:
        user: User | None = (
            uow.session.query(User)
            .filter(User.username == username, User.password == password)
            .first()
        )
        if not user:
            raise UnauthorizedException()
        token = create_access_token(
            data={
                "sub": user.username,
            }
        )
        return token
