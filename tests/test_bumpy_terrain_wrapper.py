import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from example_package_Leon_Kruse import BumpyTerrainWrapper


class Array(list):
    def copy(self):
        return Array(self)

    def __mul__(self, other):
        return Array(x * other for x in self)

    def __rmul__(self, other):
        return self.__mul__(other)


class DummyPhysics:
    def __init__(self, hfield_data):
        self.model = type('model', (), {
            'nhfield': 1,
            'hfield_data': Array(hfield_data)
        })

    def forward(self):
        pass


class DummyEnv:
    def __init__(self, hfield_data):
        self.physics = DummyPhysics(hfield_data)

    def reset(self):
        return 'reset'

    def step(self, action):
        return action


def test_bumpiness_scales_height_field():
    env = DummyEnv([1.0, 2.0, 3.0])
    wrapper = BumpyTerrainWrapper(env, bumpiness=2)
    expected = Array([x * (2/3.0) for x in [1.0, 2.0, 3.0]])
    assert env.physics.model.hfield_data == expected

    wrapper.set_bumpiness(0)
    assert env.physics.model.hfield_data == Array([0.0, 0.0, 0.0])
