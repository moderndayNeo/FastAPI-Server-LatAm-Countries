# FastAPI LATAM Countries

This project is a web application built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. The application provides a RESTful API to manage information about countries in Latin America.

## Technologies Used

- FastAPI - web framework
- SQLAlchemy - ORM
- Alembic - database migration tool
- aiomysql - MySQL connector
- Pydantic - data validation
- Python 3.12 - programming language

## Project Structure

- `src/app/main.py`: The main entry point of the application. It defines the FastAPI app and the API endpoints.
- `src/app/models.py`: Defines the SQLAlchemy models for the database.
- `src/app/schemas.py`: Defines the Pydantic schemas for data validation.
- `src/app/database.py`: Contains the database configuration and session management.
- `src/app/__init__.py`: Initializes the app package and exposes the necessary modules.

## Setup Instructions

1. **Create a virtual environment**:

   ```sh
   python -m venv .venv
   ```

2. **Activate the virtual environment**:

   ```sh
   source .venv/bin/activate
   ```

3. **Install the dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```sh
   fastapi dev src/app/main.py
   ```

## API Endpoints

- `GET /countries`: Retrieve a list of all countries.
- `POST /countries`: Create a new country.
- `GET /countries/{country_id}`: Retrieve a specific country by ID.
- `DELETE /countries/{country_id}`: Delete a specific country by ID.
- `PUT /countries/{country_id}`: Update a specific country by ID.
- `POST /signup`: Create a new user account.
- `POST /login`: Authenticate and start a session (sets a cookie).
- `POST /logout`: Clear the current session.

## Notes

- Ensure you have a running MySQL database and update the database configuration in `src/app/database.py` accordingly.
- Use Alembic for database migrations to keep the database schema in sync with the models.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
