from pydantic import BaseModel

class CountryBase(BaseModel):
    name: str
    capital: str
    population: int
    typical_dish: str

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: int

    class Config:
        from_attributes = True