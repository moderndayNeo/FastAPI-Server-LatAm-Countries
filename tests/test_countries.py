import pytest
from fastapi.testclient import TestClient
from src.app.main import app


@pytest.fixture()
def client():
    """Create a TestClient with startup/shutdown events."""
    with TestClient(app) as c:
        yield c

class TestCountriesAPI:
    """Test cases for the countries API endpoints"""

    def test_get_countries_returns_list(self, client):
        """Test GET /countries returns a JSON list"""
        response = client.get("/countries")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        # Should return a list (could be empty or have data)
        data = response.json()
        assert isinstance(data, list)

    def test_create_and_get_country(self, client):
        """Test creating a country and then retrieving it"""
        # Create a unique country name to avoid conflicts
        import time
        unique_name = f"TestCountry_{int(time.time())}"

        country_data = {
            "name": unique_name,
            "capital": "Test Capital",
            "population": 1000000,
            "typical_dish": "Test Dish"
        }

        # Create the country
        create_response = client.post("/countries", json=country_data)
        assert create_response.status_code == 200

        created_country = create_response.json()
        assert created_country["name"] == unique_name
        assert created_country["capital"] == "Test Capital"
        assert created_country["population"] == 1000000
        assert created_country["typical_dish"] == "Test Dish"
        assert "id" in created_country

        country_id = created_country["id"]

        # Now get the specific country
        get_response = client.get(f"/countries/{country_id}")
        assert get_response.status_code == 200

        retrieved_country = get_response.json()
        assert retrieved_country["name"] == unique_name
        assert retrieved_country["capital"] == "Test Capital"
        assert retrieved_country["population"] == 1000000
        assert retrieved_country["typical_dish"] == "Test Dish"
        assert retrieved_country["id"] == country_id

    def test_get_nonexistent_country(self, client):
        """Test GET /countries/{id} with non-existent ID returns 404"""
        response = client.get("/countries/999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Country not found"

    def test_create_country_validation(self, client):
        """Test that creating a country validates required fields"""
        # Test with missing fields
        incomplete_data = {
            "name": "Incomplete Country"
            # Missing required fields
        }

        response = client.post("/countries", json=incomplete_data)
        # Should return 422 for validation error
        assert response.status_code == 422

    def test_countries_endpoint_structure(self, client):
        """Test that the countries endpoint returns properly structured data"""
        response = client.get("/countries")
        assert response.status_code == 200

        countries = response.json()
        assert isinstance(countries, list)

        # If there are countries, check the structure
        if countries:
            first_country = countries[0]
            required_fields = ["id", "name", "capital", "population", "typical_dish"]
            for field in required_fields:
                assert field in first_country, f"Missing field: {field}"

    def test_delete_country(self):
        """Test deleting a country removes it from the API"""
        import time

        unique_name = f"DeleteCountry_{int(time.time())}"
        country_data = {
            "name": unique_name,
            "capital": "Delete Capital",
            "population": 123456,
            "typical_dish": "Delete Dish",
        }

        # Create the country
        create_resp = client.post("/countries", json=country_data)
        assert create_resp.status_code == 200
        country_id = create_resp.json()["id"]

        # Delete the country
        delete_resp = client.delete(f"/countries/{country_id}")
        assert delete_resp.status_code == 200

        # Verify it no longer exists
        get_resp = client.get(f"/countries/{country_id}")
        assert get_resp.status_code == 404
