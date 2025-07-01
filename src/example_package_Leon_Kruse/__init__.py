"""Example package providing simple arithmetic helpers."""

from importlib.metadata import PackageNotFoundError, version

from .example import add_one, add_two, add_three

try:  # pragma: no cover - version is provided when installed
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover - fallback for local usage
    __version__ = "0.0.0"

__all__ = ["add_one", "add_two", "add_three"]

