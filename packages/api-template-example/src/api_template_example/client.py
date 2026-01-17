"""API Client implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
from pydantic import BaseModel

if TYPE_CHECKING:
    from types import TracebackType


class APIResponse(BaseModel):
    """Standard API response model."""

    status: str
    data: dict[str, Any]


class APIClient:
    """HTTP API client with type safety."""

    def __init__(
        self, base_url: str = "https://api.example.com", *, timeout: float = 30.0
    ) -> None:
        """Initialize the API client.

        Args:
            base_url: The base URL for API requests.
            timeout: Request timeout in seconds.
        """
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    @property
    def base_url(self) -> str:
        """Get base URL."""
        return self._base_url

    @property
    def timeout(self) -> float:
        """Get timeout."""
        return self._timeout

    @property
    def client(self) -> httpx.AsyncClient | None:
        """Get HTTP client."""
        return self._client

    async def __aenter__(self) -> APIClient:
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        if self._client:  # pragma: no branch
            await self._client.aclose()

    async def get(self, endpoint: str) -> APIResponse:
        """Perform GET request.

        Args:
            endpoint: API endpoint path.

        Returns:
            Parsed API response.

        Raises:
            RuntimeError: If client is not initialized.
        """
        if not self._client:
            msg = "Client not initialized. Use async context manager."
            raise RuntimeError(msg)

        response = await self._client.get(endpoint)
        response.raise_for_status()

        return APIResponse(status="ok", data=response.json())
