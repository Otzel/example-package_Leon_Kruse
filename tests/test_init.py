import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

import example_package_Leon_Kruse as pkg


def test_public_api():
    assert pkg.add_one(1) == 2
    assert pkg.add_two(1) == 3
    assert pkg.add_three(1) == 4


def test_version():
    assert hasattr(pkg, '__version__')
