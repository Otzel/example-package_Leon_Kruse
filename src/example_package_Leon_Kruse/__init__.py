"""Utilities for DM Control terrain manipulation."""

from importlib.metadata import PackageNotFoundError, version

from .bumpy_terrain_wrapper import BumpyTerrainWrapper
from .terrain_patch import patch_domain

__all__ = ["BumpyTerrainWrapper", "patch_domain"]

try:  # pragma: no cover - version is provided when installed
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover - fallback for local usage
    __version__ = "0.0.0"
