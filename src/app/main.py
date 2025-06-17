from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
from starlette.middleware.sessions import SessionMiddleware
from src.app import models, schemas
from src.app.database import engine, get_db, Base
from .auth_utils import get_password_hash, verify_password, get_current_user

SECRET_KEY = "change-this-session-secret"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Ensure tables exist when imported (for tests using TestClient without
# lifespan events)
asyncio.run(startup())

@app.post("/signup", response_model=schemas.User)
async def signup(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.username == user.username))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = models.User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@app.post("/login")
async def login(
    user: schemas.UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(models.User).filter(models.User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    request.session["user_id"] = db_user.id
    return {"message": "Logged in"}


@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}

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


