from pydantic import BaseModel


class Price(BaseModel):
    measure: str
    amount: float
    price: float
    full_price: float
