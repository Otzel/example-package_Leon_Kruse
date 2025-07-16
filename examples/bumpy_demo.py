from dm_control import suite, viewer
from example_package_Leon_Kruse import BumpyTerrainWrapper

# Load a DeepMind Control Suite environment
env = suite.load(domain_name="cartpole", task_name="balance")

# Wrap it to adjust terrain bumpiness
env = BumpyTerrainWrapper(env, bumpiness=2)

# Visualize using the built-in viewer
viewer.launch(env)

# Retrieve a single frame as an RGB array
frame = env.physics.render(height=480, width=640, camera_id=0)
print("Rendered frame shape:", frame.shape)
