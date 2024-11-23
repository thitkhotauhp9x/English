import asyncio

import pytest


async def fetch_data():
    await asyncio.sleep(1)
    return "Data received"


@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data()
    assert result == "Data received"
