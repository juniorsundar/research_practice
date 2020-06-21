from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum
import networkx as nx

import matplotlib.pyplot as plt

'''
gridworld:

+------+------+------+
| x0y2 | x1y2 | x2y2 |
|      |      |      |
+------+------+------+
| x0y1 | x1y1 | x2y1 |
|      |      |      |
+------+------+------+
| x0y0 | x1y0 | x2y0 |
|      |      |      |
+------+------+------+

dynamics
x \in 0..2 /\ y \in 0..2
x' \in 0..2 /\ y' \in 0..2

x = 0 => (x' = 0 \/ x' = 1)
x = 1 => (x' = 0 \/ x' = 1 \/ x' = 2)
x = 2 => (x' = 1 \/ x' = 2)

y = 0 => (y' = 0 \/ y' = 1)
y = 1 => (y' = 0 \/ y' = 1 \/ y' = 2)
y = 2 => (y' = 1 \/ y' = 2)
'''

aut = trl.Automaton()
aut.declare_variables(sysX=(0,2), sysY = (0,2), active=(1, 2), k = (0,1), goTo = (0,2), kR = (0,2))
aut.varlist['env']=['active']
aut.varlist['sys']=['sysX','sysY','k','kR','goTo']
aut.prime_varlists()

specs = '''
envInit ==
    /\ active = 1

envNext ==
    /\ (active \in 1..2 /\ active' \in 1..2)
    /\ (active' = active \/ active' != active)

stat == (sysX' = sysX /\ sysY' = sysY)

dynamics == 
    /\ (sysX \in 0..2 /\ sysY \in 0..2)
    /\ (sysX' \in 0..2 /\ sysY' \in 0..2)

    /\ (((sysX' - sysX) < 2) /\ ((sysX' - sysX) > -2))
    /\ (((sysY' - sysY) < 2) /\ ((sysY' - sysY) > -2))

home == 
    /\ sysX = 0
    /\ sysY = 0

room1 == 
    /\ sysX = 2
    /\ sysY = 0

room2 == 
    /\ sysX = 0
    /\ sysY = 2

goTOR1 ==
    /\ ((sysX < 2) => (sysX' = sysX + 1))
    /\ ((sysY > 0) => (sysY' = sysY - 1))

goTOR2 ==
    /\ ((sysX > 0) => (sysX' = sysX - 1))
    /\ ((sysY < 2) => (sysY' = sysY + 1))

goTOHOME ==
    /\ ((sysX > 0) => (sysX' = sysX - 1))
    /\ ((sysY > 0) => (sysY' = sysY - 1))

sysInit ==
    /\ sysX = 0
    /\ sysY = 0
    /\ k = 1
    /\ goTo = 0
    /\ kR = 2

sysNext ==
    /\ dynamics
    /\ ((goTo = 0) => (goTOHOME))
    /\ ((goTo = 1) => (goTOR1))
    /\ ((goTo = 2) => (goTOR2))

    /\ ((home /\ (goTo = 1 \/ goTo = 2)) => (k' = k /\ kR' = kR /\ goTo' = goTo))
    /\ ((home /\ k = 1 /\ (kR = 1 \/ kR = 2) /\ goTo = 0) => (stat /\ k' = k /\ kR' = kR /\ goTo' = kR))

    /\ (((~home /\ ~room1 /\ ~room2)) => (k' = k /\ goTo' = goTo /\ kR' = kR))

    /\ ((room2 /\ active = 2 /\ goTo = 2) => (stat /\ k' = 1 /\ kR' = 2 /\ goTo' = 0))
    /\ ((room2 /\ goTo = 0) => (k' = 1 /\ kR' = 2 /\ goTo' = 0))
    /\ ((room2 /\ active != 2 /\ goTo = 2) => (stat /\ k' = 0 /\ kR' = 0 /\ goTo' = 1))
    /\ ((room2 /\ goTo = 1) => (k' = 0 /\ kR' = 0 /\ goTo' = 1))

    /\ ((room1 /\ active = 1 /\ goTo = 1) => (stat /\ k' = 1 /\ kR' = 1 /\ goTo' = 0))
    /\ ((room1 /\ goTo = 0) => (k' = 1 /\ kR' = 1 /\ goTo' = 0))
    /\ ((room1 /\ active != 1 /\ goTo = 1) => (stat /\ k' = 0 /\ kR' = 0 /\ goTo' = 2))
    /\ ((room1 /\ goTo = 2) => (k' = 0 /\ kR' = 0 /\ goTo' = 2))
'''

aut.define(specs)
aut.init.update(
    env='envInit',
    sys='sysInit')
aut.action.update(
    env='envNext',
    sys='sysNext')
aut.win['<>[]'] = aut.bdds_from('TRUE')
aut.win['[]<>'] = aut.bdds_from('sysX = 0 /\ sysY = 0')
aut.qinit = '\E \A'
aut.moore = True
aut.plus_one = True

z, yij, xijk = gr1.solve_streett_game(aut)
gr1.make_streett_transducer(z, yij, xijk, aut)
aut.varlist['sys'].append('_goal')
aut.prime_varlists()
# enumerate
g = enum.action_to_steps(aut, 'env', 'impl', qinit=aut.qinit)
h, _ = sym_enum._format_nx(g)
pd = nx.drawing.nx_pydot.to_pydot(h)
pd.write_pdf('game_states_omega.pdf')



    # /\ (~(home /\ k = 1 /\ kR = 1 /\ goTo = 0) \/ (k' = 1 /\ kR' = 1 /\ sysX' = 0 /\ sysY' = 0 /\ goTo' = 1))
    # /\ (~(home /\ k = 1 /\ kR = 2 /\ goTo = 0) \/ (k' = 1 /\ kR' = 2 /\ sysX' = 0 /\ sysY' = 0 /\ goTo' = 2))


    # /\ (~(k = 1 /\ kR = 1 /\ goTo = 0) \/ (k' = 1 /\ kR' = 1 /\ goTo' = 0))
    # /\ (~(k = 1 /\ kR = 2 /\ goTo = 0) \/ (k' = 1 /\ kR' = 2 /\ goTo' = 0))
    # /\ (~(k = 0 /\ kR = 0 /\ goTo = 0) \/ (k' = 1 /\ kR' = 2 /\ goTo' = 0))

    # /\ (~(~room1 /\ k = 0 /\ kR = 0 /\ goTo = 1) \/ (k' = 0 /\ kR' = 0 /\ goTo' = 1))
    # /\ (~(~room2 /\ k = 0 /\ kR = 0 /\ goTo = 2) \/ (k' = 0 /\ kR' = 0 /\ goTo' = 2))
    # /\ (~(~home /\ k = 0 /\ kR = 0 /\ goTo = 0) \/ (k' = 0 /\ kR' = 0 /\ goTo' = 0))

    # /\ (~(room1 /\ active = 1 /\ k = 0 /\ kR = 0 /\ goTo = 1) \/ (sysX' = 2 /\ sysY' = 0 /\ k' = 1 /\ kR' = 1 /\ goTo' = 0))
    # /\ (~(room1 /\ active != 1 /\ k = 0 /\ kR = 0 /\ goTo = 1) \/ (sysX' = 2 /\ sysY' = 0 /\ k' = 0 /\ kR' = 0 /\ goTo' = 2))

    # /\ (~(room2 /\ active = 2 /\ k = 0 /\ kR = 0 /\ goTo = 2) \/ (sysX' = 0 /\ sysY' = 2 /\ k' = 1 /\ kR' = 2 /\ goTo' = 0))
    # /\ (~(room2 /\ active != 2 /\ k = 0 /\ kR = 0 /\ goTo = 2) \/ (sysX' = 0 /\ sysY' = 2 /\ k' = 0 /\ kR' = 0 /\ goTo' = 1))
