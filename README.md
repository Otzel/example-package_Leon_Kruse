# Sassy Env Wrapper

This package provides a minimal wrapper for Gymnasium-style environments.
Whenever `step()` is called, the wrapper prints a short message before
forwarding the call to the original environment. It is primarily intended to
show how to publish a tiny package that wraps an environment.

## Installation

```bash
pip install --upgrade --index-url https://test.pypi.org/simple/ --no-deps example_package_Leon_Kruse
```

## Usage

```python
from example_package_Leon_Kruse import SassyEnvWrapper

class DummyEnv:
    def step(self, action):
        return action

wrapped = SassyEnvWrapper(DummyEnv())
wrapped.step(0)  # prints a sassy message
```

## Versioning

The project uses `hatch-vcs` to derive the package version from Git tags. When
installed from a release, `__version__` reflects that tag; otherwise it falls
back to ``0.0.0`` in a local checkout.

## Examples

An executable example is available in `examples/demo.py`.
