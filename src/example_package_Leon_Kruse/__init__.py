"""A minimal environment wrapper for Gymnasium-like environments."""

from importlib.metadata import PackageNotFoundError, version

from .bumpy_terrain_wrapper import BumpyTerrainWrapper

__all__ = ["SassyEnvWrapper", "BumpyTerrainWrapper"]

try:  # pragma: no cover - version is provided when installed
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover - fallback for local usage
    __version__ = "0.0.0"


class SassyEnvWrapper:
    """Wrapper that prints a sassy message whenever ``step`` is called."""

    def __init__(self, env):
        self.env = env

    def step(self, action):
        print("Girl, you better step it like you mean it!")
        return self.env.step(action)

    def __getattr__(self, name):
        return getattr(self.env, name)
