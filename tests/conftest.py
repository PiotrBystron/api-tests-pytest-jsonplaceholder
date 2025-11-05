import pytest

@pytest.fixture(scope="session")
def api_base_url():
    return "https://jsonplaceholder.typicode.com"