"""Wrapper to adjust terrain bumpiness in DeepMind Control Suite environments."""

from __future__ import annotations

from typing import Any


class BumpyTerrainWrapper:
    """Adjust height field amplitude to control terrain bumpiness.

    Parameters
    ----------
    env:
        A DeepMind Control Suite environment exposing a ``physics`` attribute.
    bumpiness:
        Integer between ``0`` (flat) and ``3`` (extremely bumpy).
    """

    def __init__(self, env: Any, bumpiness: int = 0) -> None:
        self.env = env
        self._original_hfield_data = None
        self.set_bumpiness(bumpiness)

    def _apply_bumpiness(self) -> None:
        physics = getattr(self.env, "physics", None)
        if physics is None:
            raise AttributeError("Wrapped environment must expose a 'physics' attribute")

        if physics.model.nhfield > 0:
            if self._original_hfield_data is None:
                self._original_hfield_data = physics.model.hfield_data.copy()
            scale = self.bumpiness / 3.0
            physics.model.hfield_data[:] = self._original_hfield_data * scale
            physics.forward()

    def set_bumpiness(self, bumpiness: int) -> None:
        if not 0 <= bumpiness <= 3:
            raise ValueError("bumpiness must be between 0 and 3")
        self.bumpiness = bumpiness
        self._apply_bumpiness()

    def reset(self, *args: Any, **kwargs: Any) -> Any:
        timestep = self.env.reset(*args, **kwargs)
        self._apply_bumpiness()
        return timestep

    def step(self, action: Any) -> Any:
        return self.env.step(action)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.env, name)
