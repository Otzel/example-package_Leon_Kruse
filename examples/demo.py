from dm_control import suite, viewer
from example_package_Leon_Kruse import patch_domain

# Enable terrain in the fish domain
patch_domain("fish")

env = suite.load(
    domain_name="fish",
    task_name="swim",
    task_kwargs={
        "environment_kwargs": {
            "mode": "terrain",
            "terrain": {
                "bump_scale": 0.15,
                "smoothness": 0.1,
            },
        }
    }
)

viewer.launch(environment_loader=env)
