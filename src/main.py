from fastapi import FastAPI

from backbone.base_class import Base
from project_orm import BIND
from reservation.entrypoints import router as reservation_router
from auth.entrypoints.auth_routes import router as auth_router
from auth.service.utils import AuthMiddleware


if True:
    from reservation import domain as reservation_domain
    from auth.user import User

    Base.metadata.create_all(BIND)

app = FastAPI()

app.add_middleware(AuthMiddleware)

app.include_router(auth_router)
app.include_router(reservation_router)


@app.get("/")
def main_route():
    return {"msg": "api is running"}
