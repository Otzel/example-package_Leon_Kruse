import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from example_package_Leon_Kruse import SassyEnvWrapper


class DummyEnv:
    def __init__(self):
        self.count = 0

    def step(self, action):
        self.count += 1
        return self.count


def test_step_prints_and_delegates(capfd):
    env = SassyEnvWrapper(DummyEnv())
    result = env.step(None)
    captured = capfd.readouterr().out
    assert "Girl, you better step it like you mean it!" in captured
    assert result == 1
