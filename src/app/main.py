from fastapi import FastAPI

app = FastAPI()


# Create an empty array named "countries"
countries = [
    {
        "id": 1,
        "name": "Colombia",
        "capital": "Bogota",
        "population": 50000000,

    },
    {
        "id": 2,
        "name": "Brazil",
        "capital": "Brasilia",
        "population": 211000000,
    }
]


@app.get("/countries")
def get_countries():
    return countries

@app.post("/countries")
def create_country(country: dict):
    # Generate a new ID for the country
    new_id = max(c['id'] for c in countries) + 1 if countries else 1
    country['id'] = new_id
    countries.append(country)
    return {"message": "Country added successfully", "country": country}


@app.get("/countries/{country_id}")
def get_country(country_id: int):
    for country in countries:
        if country['id'] == country_id:
            return country
    return {"message": "Country not found"}

