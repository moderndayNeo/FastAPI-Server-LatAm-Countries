from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.app import models, schemas
from src.app.database import engine, get_db, Base

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/countries", response_model=list[schemas.Country])
async def get_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Country))
    countries = result.scalars().all()
    return countries

@app.post("/countries", response_model=schemas.Country)
async def create_country(country: schemas.CountryCreate, db: AsyncSession = Depends(get_db)):
    db_country = models.Country(**country.model_dump())
    db.add(db_country)
    await db.commit()
    await db.refresh(db_country)
    return db_country

@app.get("/countries/{country_id}", response_model=schemas.Country)
async def get_country(country_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Country).filter(models.Country.id == country_id))
    country = result.scalar_one_or_none()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@app.delete("/countries/{country_id}")
async def delete_country(country_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Country).filter(models.Country.id == country_id))
    country = result.scalar_one_or_none()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    await db.delete(country)
    await db.commit()
    return {"message": "Country deleted successfully"}

@app.put("/countries/{country_id}", response_model=schemas.Country)
async def update_country(
    country_id: int,
    country_update: schemas.CountryCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Country).filter(models.Country.id == country_id))
    country = result.scalar_one_or_none()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    for key, value in country_update.model_dump().items():
        setattr(country, key, value)

    await db.commit()
    await db.refresh(country)
    return country


