import importlib

mjlib = None


def _load_numpy():
    import numpy as np
    from scipy import ndimage
    return np, ndimage


def _load_dm_control():
    global mjlib
    from dm_control import mjcf
    from dm_control.mujoco.wrapper import mjbindings
    from dm_control.rl import control
    mjlib = mjbindings.mjlib
    return mjcf, control


def _add_terrain_to_model(model, num_segments=25, segment_length=10.0, segment_width=0.8):
    """Modifies MJCF model to insert terrain heightfields."""
    for geom in model.worldbody.find_all('geom'):
        if geom.type == 'plane':
            geom.remove()

    for i in range(num_segments):
        hfield = model.asset.add(
            'hfield',
            name=f'terrain_{i}',
            nrow=101,
            ncol=101,
            size=(segment_length, segment_width, 0.5, 0.1)
        )
        model.worldbody.add(
            'geom',
            name=f'terrain_{i}',
            type='hfield',
            pos=(i * segment_length - (num_segments * segment_length) / 2, 0, 0),
            hfield=hfield,
            rgba=(0.3, 0.3, 0.3, 1),
            conaffinity=1
        )
    return model


def _generate_terrain_data(physics, bump_scale, smoothness):
    np, ndimage = _load_numpy()
    for i in range(25):
        try:
            hfield_id = physics.model.name2id(f'terrain_{i}', 'hfield')
        except ValueError:
            continue

        nrow = physics.model.hfield_nrow[hfield_id]
        ncol = physics.model.hfield_ncol[hfield_id]
        terrain_len = physics.model.hfield_size[hfield_id, 1]
        terrain_width = physics.model.hfield_size[hfield_id, 0]

        bump_res_len = max(2, int(terrain_len / bump_scale))
        bump_res_width = max(2, int(terrain_width / bump_scale))
        bumps = np.random.uniform(smoothness, 1.0, (bump_res_len, bump_res_width))
        smooth_bumps = ndimage.zoom(bumps, (nrow / bump_res_len, ncol / bump_res_width))
        terrain = 0.3 + 0.4 * smooth_bumps

        start_idx = physics.model.hfield_adr[hfield_id]
        physics.model.hfield_data[start_idx:start_idx + nrow * ncol] = terrain.ravel()

        if getattr(physics, 'contexts', None):
            with physics.contexts.gl.make_current() as ctx:
                ctx.call(mjlib.mjr_uploadHField,
                         physics.model.ptr,
                         physics.contexts.mujoco.ptr,
                         hfield_id)


def patch_domain(domain_name):
    """Monkey-patches a dm_control domain to support procedural terrain."""
    mjcf, control = _load_dm_control()
    domain_mod = importlib.import_module(f"dm_control.suite.{domain_name}")

    PhysicsCls = getattr(domain_mod, "Physics", mjcf.Physics)

    TaskCls = None
    for name in dir(domain_mod):
        obj = getattr(domain_mod, name)
        if isinstance(obj, type) and issubclass(obj, control.Task) and obj is not control.Task:
            TaskCls = obj
            break

    if TaskCls is None:
        raise RuntimeError(f"Could not find a Task class in domain {domain_name}.")

    for task_name, task_fn in domain_mod.SUITE._tasks.items():
        original_fn = task_fn

        def make_wrapped_task(task_fn=original_fn, task_name=task_name):
            def wrapped_task(time_limit=25, random=None, environment_kwargs=None):
                environment_kwargs = environment_kwargs or {}
                mode = environment_kwargs.pop("mode", "normal")
                terrain_opts = environment_kwargs.pop("terrain", {})

                if mode == "normal":
                    return task_fn(time_limit=time_limit, random=random, environment_kwargs=environment_kwargs)

                bump_scale = terrain_opts.get("bump_scale", 0.2)
                smoothness = terrain_opts.get("smoothness", 0.0)

                orig_env = task_fn(time_limit=time_limit, random=random, environment_kwargs={})
                task = orig_env._task

                xml_string, assets = domain_mod.get_model_and_assets()
                mjcf_model = mjcf.from_xml_string(xml_string, assets=assets)
                mjcf_model = _add_terrain_to_model(mjcf_model)

                physics = PhysicsCls.from_xml_string(
                    mjcf_model.to_xml_string(), assets=mjcf_model.get_assets()
                )
                _generate_terrain_data(physics, bump_scale, smoothness)

                return control.Environment(
                    physics, task,
                    time_limit=time_limit,
                    control_timestep=0.004,
                    **environment_kwargs
                )
            return wrapped_task

        domain_mod.SUITE._tasks[task_name] = make_wrapped_task()
