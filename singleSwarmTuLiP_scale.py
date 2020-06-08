from __future__ import print_function

import logging

from tulip import transys, spec, synth
from tulip.transys import machines
from omega import automata

logging.basicConfig(level=logging.WARNING)

ROOMS = 2

env_vars = set()
env_init = set()
env_safe = set()
env_prog = set()

#Environment Assumptions
if ROOMS>2:
    text = ""
    for i in range(1,ROOMS+1):
        env_vars.add("active{roomN}".format(roomN=i))
        
        if i==1:
            env_init.add("active{roomN}".format(roomN=i))
        else:
            env_init.add("!active{roomN}".format(roomN=i))

        ands = ' && '
        text = text + "( active{roomN} && ".format(roomN=i)
        for j in range(1,ROOMS+1):
            if j==i:
                continue
            text = text + "!active{roomN}".format(roomN=j)
            text = text + ands
        text = text[0:-4] + " ) || "
        env_prog.add("active{roomN}".format(roomN=i))
    env_safe.add(text[0:-4])
else:
    env_vars = {'active1','active2'}
    env_init = {'active1','!active2'}
    env_safe = {'active1 <-> !active2'}
    env_prog = {'active1','active2'}

#System Guarantees
sys_vars = {'room':(0,ROOMS),'known_room':(0,ROOMS),'home':"boolean",'known':"boolean"}
sys_init = {'home', 'room = 0', '!known', 'known_room = 0'}
sys_safe = {
    'home -> X (!home)',
    'home <-> room = 0',
    '!home && X known -> X home'
}

for i in range(1,ROOMS+1):
    line1 = '!home && room = {roomN} && active{roomN} -> X (known && known_room = {roomN})'.format(roomN=i)
    line2 = 'home && known && known_room = {roomN} -> X (known && known_room = {roomN} && room = {roomN})'.format(roomN=i)
    if i<ROOMS:
        line3 = '!home && (room = {roomN} && !active{roomN}) -> X (!known && known_room = 0 && room = {NroomN})'.format(roomN=i,NroomN=i+1)
    else:
        line3 = '!home && (room = {roomN} && !active{roomN}) -> X (!known && known_room = 0 && room = {NroomN})'.format(roomN=i,NroomN=1)
    sys_safe.add(line1)
    sys_safe.add(line2)
    sys_safe.add(line3)

sys_prog = set()

# Create a GR(1) specification
specs = spec.GRSpec(env_vars = env_vars, env_init = env_init, env_safety = env_safe, env_prog = env_prog,
                    sys_vars = sys_vars, sys_init = sys_init, sys_safety = sys_safe, sys_prog = sys_prog)

print(specs.dumps())

specs.moore = True
specs.qinit = '\E \A'  # i.e., "there exist sys_vars: forall sys_vars"

strategy = synth.synthesize(specs)
assert strategy is not None, 'unrealizable'
A = automata.Automaton(strategy)
if not strategy.save('strategy_for_single_robot_scale.png'):
    print(strategy)

# simulate
print(strategy)
machines.random_run(strategy, N=10)