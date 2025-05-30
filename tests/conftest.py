import pytest

# Configure pytest-asyncio
pytest_plugins = ("pytest_asyncio",)

@pytest.fixture(scope="session")
def event_loop_policy():
    """Set the event loop policy for the test session"""
    import asyncio
    return asyncio.DefaultEventLoopPolicy()