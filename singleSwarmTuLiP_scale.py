from __future__ import print_function

import logging

from tulip import transys, spec, synth
from tulip.transys import machines


logging.basicConfig(level=logging.WARNING)

env_vars = {'active1','active2','active3'}
env_init = {'active1','!active2','!active3'}
env_safe = {'(active1 -> !active2 && !active3)',
            '(active2 -> !active1 && !active3)',
            '(active3 -> !active1 && !active2)'}
env_prog = {'active1','active2','active3'}

sys_vars = {'room':(0,3),'known_room':(0,3),'home':"boolean",'known':"boolean"}
sys_init = {'home', 'room = 0', '!known', 'known_room = 0'}
sys_safe = {
    'home -> X (!home)',
    'home <-> room = 0',
    '!home && X known -> X home',

    '!home && room = 1 && active1 -> X (known && known_room = 1)',
    'home && known && known_room = 1 -> X (known && known_room = 1 && room = 1)',
    '!home && (room = 1 && !active1) -> X (!known && known_room = 0 && room = 2)',

    '!home && room = 2 && active2 -> X (known && known_room = 2)',
    'home && known && known_room = 2 -> X (known && known_room = 2 && room = 2)',
    '!home && (room = 2 && !active2) -> X (!known && known_room = 0 && room = 3)',

    '!home && room = 3 && active3 -> X (known && known_room = 3)',
    'home && known && known_room = 3 -> X (known && known_room = 3 && room = 3)',
    '!home && (room = 3 && !active3) -> X (!known && known_room = 0 && room = 1)'
    }

sys_prog = set()

# Create a GR(1) specification
specs = spec.GRSpec(env_vars = env_vars, env_init = env_init, env_safety = env_safe, env_prog = env_prog,
                    sys_vars = sys_vars, sys_init = sys_init, sys_safety = sys_safe, sys_prog = sys_prog)

print(specs.dumps())

specs.moore = True
specs.qinit = '\E \A'  # i.e., "there exist sys_vars: forall sys_vars"

strategy = synth.synthesize(specs)
assert strategy is not None, 'unrealizable'

if not strategy.save('strategy_for_single_robot_scale.png'):
    print(strategy)

# simulate
print(strategy)
machines.random_run(strategy, N=10)