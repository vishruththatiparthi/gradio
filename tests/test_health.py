from app.main import root

import pytest

pytestmark = pytest.mark.anyio


async def test_health():
    response = await root()
    assert "message" in response
