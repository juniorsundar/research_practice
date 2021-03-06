from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum
import networkx as nx

import matplotlib.pyplot as plt

aut = trl.Automaton()
aut.declare_variables(active=(1, 2), turn = (1,2), 
                      sysX1=(0,2), sysY1 = (0,2), k1 = (0,1), goTo1 = (0,2), kR1 = (0,2),
                      sysX2=(0,2), sysY2 = (0,2), k2 = (0,1), goTo2 = (0,2), kR2 = (0,2))
aut.varlist['env']=['active','turn']
aut.varlist['sys']=['sysX1','sysY1','k1','kR1','goTo1','sysX2','sysY2','k2','kR2','goTo2']
aut.prime_varlists()

specs = '''
UNCHANGED_sys1 == 
    /\ sysX1' = sysX1 /\ sysY1' = sysY1
    /\ k1' = k1
    /\ kR1' = kR1
    /\ goTo1' = goTo1

UNCHANGED_sys2 == 
    /\ sysX2' = sysX2 /\ sysY2' = sysY2
    /\ k2' = k2
    /\ kR2' = kR2
    /\ goTo2' = goTo2

envInit ==
    /\ active = 1
    /\ turn = 1

envNext ==
    /\ (active \in 1..2 /\ active' \in 1..2)
    /\ (active' = active \/ active' != active)
    /\ (turn \in 1..2 /\ turn' \in 1..2)
    /\ (turn' != turn)
    /\ (turn = 1 => turn' = 2)
    /\ (turn = 2 => turn' = 1)

stat1 == (sysX1' = sysX1 /\ sysY1' = sysY1)

dynamics1 == 
    /\ (sysX1 \in 0..2 /\ sysY1 \in 0..2)
    /\ (sysX1' \in 0..2 /\ sysY1' \in 0..2)

    /\ (((sysX1' - sysX1) < 2) /\ ((sysX1' - sysX1) > -2))
    /\ (((sysY1' - sysY1) < 2) /\ ((sysY1' - sysY1) > -2))

home1 == 
    /\ sysX1 = 0
    /\ sysY1 = 0

room11 == 
    /\ sysX1 = 2
    /\ sysY1 = 0

room21 == 
    /\ sysX1 = 0
    /\ sysY1 = 2

goTOR11 ==
    /\ ((sysX1 < 2) => (sysX1' = sysX1 + 1))
    /\ ((sysY1 > 0) => (sysY1' = sysY1 - 1))

goTOR21 ==
    /\ ((sysX1 > 0) => (sysX1' = sysX1 - 1))
    /\ ((sysY1 < 2) => (sysY1' = sysY1 + 1))

goTOHOME1 ==
    /\ ((sysX1 > 0) => (sysX1' = sysX1 - 1))
    /\ ((sysY1 > 0) => (sysY1' = sysY1 - 1))

sysInit1 ==
    /\ sysX1 = 0
    /\ sysY1 = 0
    /\ k1 = 1
    /\ goTo1 = 0
    /\ kR1 = 2

sysStep1 ==
    /\ dynamics1
    /\ ((goTo1 = 0) => (goTOHOME1))
    /\ ((goTo1 = 1) => (goTOR11))
    /\ ((goTo1 = 2) => (goTOR21))

    /\ ((home1 /\ (goTo1 = 1 \/ goTo1 = 2)) => (k1' = k1 /\ kR1' = kR1 /\ goTo1' = goTo1))
    /\ ((home1 /\ k1 = 1 /\ (kR1 = 1 \/ kR1 = 2) /\ goTo1 = 0) => (stat1 /\ k1' = k1 /\ kR1' = kR1 /\ goTo1' = kR1))

    /\ (((~home1 /\ ~room11 /\ ~room21)) => (k1' = k1 /\ goTo1' = goTo1 /\ kR1' = kR1))

    /\ ((room21 /\ active = 2 /\ goTo1 = 2) => (stat1 /\ k1' = 1 /\ kR1' = 2 /\ goTo1' = 0))
    /\ ((room21 /\ goTo1 = 0) => (k1' = 1 /\ kR1' = 2 /\ goTo1' = 0))
    /\ ((room21 /\ active != 2 /\ goTo1 = 2) => (stat1 /\ k1' = 0 /\ kR1' = 0 /\ goTo1' = 1))
    /\ ((room21 /\ goTo1 = 1) => (k1' = 0 /\ kR1' = 0 /\ goTo1' = 1))

    /\ ((room11 /\ active = 1 /\ goTo1 = 1) => (stat1 /\ k1' = 1 /\ kR1' = 1 /\ goTo1' = 0))
    /\ ((room11 /\ goTo1 = 0) => (k1' = 1 /\ kR1' = 1 /\ goTo1' = 0))
    /\ ((room11 /\ active != 1 /\ goTo1 = 1) => (stat1 /\ k1' = 0 /\ kR1' = 0 /\ goTo1' = 2))
    /\ ((room11 /\ goTo1 = 2) => (k1' = 0 /\ kR1' = 0 /\ goTo1' = 2))

sysNext1 ==
    /\ (turn = 1 => sysStep1)
    /\ (turn != 1 => UNCHANGED_sys1)


stat2 == (sysX2' = sysX2 /\ sysY2' = sysY2)

dynamics2 == 
    /\ (sysX2 \in 0..2 /\ sysY2 \in 0..2)
    /\ (sysX2' \in 0..2 /\ sysY2' \in 0..2)

    /\ (((sysX2' - sysX2) < 2) /\ ((sysX2' - sysX2) > -2))
    /\ (((sysY2' - sysY2) < 2) /\ ((sysY2' - sysY2) > -2))

home2 == 
    /\ sysX2 = 0
    /\ sysY2 = 0

room12 == 
    /\ sysX2 = 2
    /\ sysY2 = 0

room22 == 
    /\ sysX2 = 0
    /\ sysY2 = 2

goTOR12 ==
    /\ ((sysX2 < 2) => (sysX2' = sysX2 + 1))
    /\ ((sysY2 > 0) => (sysY2' = sysY2 - 1))

goTOR22 ==
    /\ ((sysX2 > 0) => (sysX2' = sysX2 - 1))
    /\ ((sysY2 < 2) => (sysY2' = sysY2 + 1))

goTOhome2 ==
    /\ ((sysX2 > 0) => (sysX2' = sysX2 - 1))
    /\ ((sysY2 > 0) => (sysY2' = sysY2 - 1))

sysInit2 ==
    /\ sysX2 = 0
    /\ sysY2 = 0
    /\ k2 = 1
    /\ goTo2 = 0
    /\ kR2 = 2

sysStep2 ==
    /\ dynamics2
    /\ ((goTo2 = 0) => (goTOhome2))
    /\ ((goTo2 = 1) => (goTOR12))
    /\ ((goTo2 = 2) => (goTOR22))

    /\ ((home2 /\ (goTo2 = 1 \/ goTo2 = 2)) => (k2' = k2 /\ kR2' = kR2 /\ goTo2' = goTo2))
    /\ ((home2 /\ k2 = 1 /\ (kR2 = 1 \/ kR2 = 2) /\ goTo2 = 0) => (stat2 /\ k2' = k2 /\ kR2' = kR2 /\ goTo2' = kR2))

    /\ (((~home2 /\ ~room12 /\ ~room22)) => (k2' = k2 /\ goTo2' = goTo2 /\ kR2' = kR2))

    /\ ((room22 /\ active = 2 /\ goTo2 = 2) => (stat2 /\ k2' = 1 /\ kR2' = 2 /\ goTo2' = 0))
    /\ ((room22 /\ goTo2 = 0) => (k2' = 1 /\ kR2' = 2 /\ goTo2' = 0))
    /\ ((room22 /\ active != 2 /\ goTo2 = 2) => (stat2 /\ k2' = 0 /\ kR2' = 0 /\ goTo2' = 1))
    /\ ((room22 /\ goTo2 = 1) => (k2' = 0 /\ kR2' = 0 /\ goTo2' = 1))

    /\ ((room12 /\ active = 1 /\ goTo2 = 1) => (stat2 /\ k2' = 1 /\ kR2' = 1 /\ goTo2' = 0))
    /\ ((room12 /\ goTo2 = 0) => (k2' = 1 /\ kR2' = 1 /\ goTo2' = 0))
    /\ ((room12 /\ active != 1 /\ goTo2 = 1) => (stat2 /\ k2' = 0 /\ kR2' = 0 /\ goTo2' = 2))
    /\ ((room12 /\ goTo2 = 2) => (k2' = 0 /\ kR2' = 0 /\ goTo2' = 2))
    
sysNext2 ==
    /\ (turn = 2 => sysStep2)
    /\ (turn != 2 => UNCHANGED_sys2)
    
environmentInit == envInit
environmentNext == envNext
sysInit == sysInit1 /\ sysInit2
sysNext == sysNext1 /\ sysNext2
'''

aut.define(specs)
aut.init.update(
    env='envInit',
    sys='sysInit')
aut.action.update(
    env='envNext',
    sys='sysNext')
aut.win['<>[]'] = aut.bdds_from('TRUE')
aut.win['[]<>'] = aut.bdds_from('TRUE')
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
pd.write_pdf('/../outputs/dual_gridworld_game_states_omega.pdf')