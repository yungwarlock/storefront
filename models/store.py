from pydantic import BaseModel


class Store(BaseModel):
    id: str
    title: str
    description: str
