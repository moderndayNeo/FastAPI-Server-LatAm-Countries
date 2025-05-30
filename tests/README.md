# Tests for FastAPI LATAM Countries API

This directory contains tests for the LATAM Countries FastAPI application.

## Running Tests

To run all tests:

```bash
# From the project root directory
./.venv/bin/python -m pytest tests/ -v
```

To run a specific test file:

```bash
./.venv/bin/python -m pytest tests/test_countries.py -v
```

To run tests with coverage:

```bash
./.venv/bin/python -m pytest tests/ --cov=src/app --cov-report=html
```

## Test Structure

### `test_countries.py`

Tests for the countries API endpoints:

- **`test_get_countries_returns_list`**: Verifies that GET /countries returns a JSON list
- **`test_create_and_get_country`**: Tests creating a country via POST and retrieving it via GET
- **`test_get_nonexistent_country`**: Tests that requesting a non-existent country returns 404
- **`test_create_country_validation`**: Tests validation of required fields when creating countries
- **`test_countries_endpoint_structure`**: Verifies that country data has the expected structure

## Test Dependencies

The tests use:

- **pytest**: Testing framework
- **pytest-asyncio**: For async test support
- **FastAPI TestClient**: For making HTTP requests to the API

## Database

The tests use the actual application database (`latam_countries.db`) rather than a separate test database. This approach:

- Tests the real application behavior
- Uses unique country names with timestamps to avoid conflicts
- Doesn't require complex database mocking or isolation

## Adding New Tests

When adding new tests:

1. Follow the existing naming convention (`test_*` functions)
2. Use descriptive test names that explain what is being tested
3. Include docstrings explaining the test purpose
4. Use unique data (like timestamps) to avoid conflicts between test runs
5. Test both success and error cases
6. Verify response status codes and data structure

## Example Test

```python
def test_new_feature(self):
    """Test description of what this test verifies"""
    # Arrange - set up test data
    test_data = {"field": "value"}

    # Act - perform the action being tested
    response = client.post("/endpoint", json=test_data)

    # Assert - verify the results
    assert response.status_code == 200
    assert response.json()["field"] == "value"
```
