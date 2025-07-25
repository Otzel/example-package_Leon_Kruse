import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from example_package_Leon_Kruse import patch_domain


def test_patch_domain_exists():
    assert callable(patch_domain)
