"""
Simple JSON file-based state store.
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from loguru import logger


class StateStore:
    """Persistent state storage using JSON files."""

    def __init__(self, file_path: str = "state.json"):
        self.file_path = Path(file_path)
        self.data: dict[str, Any] = {}
        self._lock = asyncio.Lock()
        self._load()

    def _load(self):
        """Load state from file if exists."""
        if self.file_path.exists():
            try:
                with open(self.file_path) as f:
                    self.data = json.load(f)
                logger.debug(f"State loaded from {self.file_path}")
            except Exception as e:
                logger.error(f"Failed to load state: {e}")
                self.data = {}
        else:
            self.data = {}

    async def save(self):
        """Save current state to file."""
        async with self._lock:
            try:
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.file_path, "w") as f:
                    json.dump(self.data, f, indent=2)
                logger.debug(f"State saved to {self.file_path}")
            except Exception as e:
                logger.error(f"Failed to save state: {e}")

    async def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the state."""
        return self.data.get(key, default)

    async def set(self, key: str, value: Any):
        """Set a value in the state."""
        self.data[key] = value
        await self.save()

    async def delete(self, key: str):
        """Delete a key from the state."""
        if key in self.data:
            del self.data[key]
            await self.save()

    async def clear(self):
        """Clear all state."""
        self.data = {}
        await self.save()

    def get_all(self) -> dict[str, Any]:
        """Get all state data (read-only copy)."""
        return self.data.copy()
