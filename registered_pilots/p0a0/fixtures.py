"""Lazy deterministic fixture definitions. Import performs no IO or generation."""
import json
from pathlib import Path
import numpy as np


def configuration():
    return json.loads(Path(__file__).with_name("fixture_config.json").read_text())


def generate(case, config):
    """Future authorized pilot only; deterministic arrays, never source inputs."""
    c = config['cases'][case]
    f = dict(c)
    keys = {'points','matrix','axes','improper','path','row_matrix','translation',
            'reflection','vertices','edges','full','pieces','main','extra','spur',
            'plain','notch','zero','duplicates','small','roll_row'}
    for k in keys & c.keys():
        f[k] = np.asarray(c[k], dtype=float)
    if case == 'S01':
        f['target'] = c['scale']*(f['path']@f['row_matrix'])+f['translation']
    elif case == 'S02':
        f['target'] = f['path']*f['reflection']
    elif case == 'S03':
        t = np.arange(c['samples'], dtype=float)/(c['samples']-1)
        f['a'] = np.column_stack((5*t,2*t))
        f['b'] = np.column_stack((5*t**4,2*t**4))
    return f
