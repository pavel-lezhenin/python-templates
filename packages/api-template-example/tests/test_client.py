"""Tests for API client."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from api_template_example import APIClient
from api_template_example.client import APIResponse

if TYPE_CHECKING:
    from pytest_httpx import HTTPXMock


class TestAPIResponse:
    """Tests for APIResponse model."""

    def test_create_response(self) -> None:
        """Test creating an API response."""
        response = APIResponse(status="ok", data={"key": "value"})

        assert response.status == "ok"
        assert response.data == {"key": "value"}


class TestAPIClient:
    """Tests for APIClient."""

    def test_init(self, base_url: str) -> None:
        """Test client initialization."""
        client = APIClient(base_url)

        assert client.base_url == base_url
        assert client.timeout == 30.0

    def test_init_default(self) -> None:
        """Test client initialization with defaults."""
        client = APIClient()

        assert client.base_url == "https://api.example.com"
        assert client.timeout == 30.0

    def test_init_strips_trailing_slash(self) -> None:
        """Test that trailing slash is stripped from base URL."""
        client = APIClient("https://api.example.com/")

        assert client.base_url == "https://api.example.com"

    def test_init_custom_timeout(self, base_url: str) -> None:
        """Test client with custom timeout."""
        client = APIClient(base_url, timeout=60.0)

        assert client.timeout == 60.0

    @pytest.mark.asyncio
    async def test_context_manager(self, base_url: str) -> None:
        """Test async context manager."""
        async with APIClient(base_url) as client:
            assert client.client is not None

    @pytest.mark.asyncio
    async def test_context_manager_with_exception(self, base_url: str) -> None:
        """Test async context manager cleanup on exception."""
        with pytest.raises(ValueError, match="test error"):
            async with APIClient(base_url) as client:
                assert client.client is not None
                raise ValueError("test error")

    @pytest.mark.asyncio
    async def test_get_success(self, base_url: str, httpx_mock: HTTPXMock) -> None:
        """Test successful GET request."""
        httpx_mock.add_response(
            url="https://api.example.com/test",
            json={"result": "success"},
        )

        async with APIClient(base_url) as client:
            response = await client.get("/test")

        assert response.status == "ok"
        assert response.data == {"result": "success"}

    @pytest.mark.asyncio
    async def test_get_without_context_manager_raises(self, base_url):
        """Test that GET without context manager raises error."""
        client = APIClient(base_url)

        with pytest.raises(RuntimeError, match="Client not initialized"):
            await client.get("/test")
