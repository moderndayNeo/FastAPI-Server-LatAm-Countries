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