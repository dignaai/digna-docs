from pydantic import BaseModel


__all__ = [
    'Config',
]


class Config(BaseModel):
    api_key: str
