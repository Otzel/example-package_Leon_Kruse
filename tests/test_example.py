import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from example_package_Leon_Kruse.example import add_one


def test_add_one():
    assert add_one(3) == 4
