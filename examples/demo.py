from example_package_Leon_Kruse import SassyEnvWrapper

class DummyEnv:
    def step(self, action):
        return action

wrapped = SassyEnvWrapper(DummyEnv())
print("step ->", wrapped.step(42))
