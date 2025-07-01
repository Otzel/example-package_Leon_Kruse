# Example Package

This package demonstrates a minimal Python library providing a few helper
functions to add numbers.

## Installation

```bash
pip install example-package-Leon-Kruse
```

## Usage

```python
from example_package_Leon_Kruse import add_one, add_two, add_three

print(add_one(1))  # 2
print(add_two(1))  # 3
print(add_three(1))  # 4
```

## Versioning

The project uses `hatch-vcs` to derive the package version from Git tags. When
installed from a release, `__version__` reflects that tag; otherwise it falls
back to ``0.0.0`` in a local checkout.

## Examples

An executable example is available in `examples/demo.py`.
