# app/tests/conftest.py

import pytest
from app.utils.auth import hash_password  # ✅ should now work

@pytest.fixture
def test_password():
    return hash_password("test123")
