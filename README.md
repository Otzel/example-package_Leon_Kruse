# DM Control Terrain Utilities

This package provides helpers for modifying terrains in DeepMind Control Suite environments.
It includes a wrapper for scaling existing height fields and a helper to patch domains with
procedural terrain.

## Installation

```bash
pip install --upgrade --index-url https://test.pypi.org/simple/ --no-deps example_package_Leon_Kruse
```

## Usage

```python
from example_package_Leon_Kruse import BumpyTerrainWrapper, patch_domain
from dm_control import suite, viewer

patch_domain("fish")

env = suite.load(
    "fish",
    "swim",
    task_kwargs={
        "environment_kwargs": {
            "mode": "terrain",
            "terrain": {"bump_scale": 0.15, "smoothness": 0.1},
        }
    },
)
viewer.launch(environment_loader=env)
```

Additional examples are available in `examples/demo.py` and `examples/bumpy_demo.py`.

## Versioning

The project uses `hatch-vcs` to derive the package version from Git tags. When
installed from a release, `__version__` reflects that tag; otherwise it falls
back to `0.0.0` in a local checkout.
