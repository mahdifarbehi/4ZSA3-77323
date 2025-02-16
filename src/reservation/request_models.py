from pydantic import BaseModel


class CreateReservationRequest(BaseModel):
    people_count: int
