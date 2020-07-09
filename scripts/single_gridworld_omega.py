from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum
import networkx as nx

import matplotlib.pyplot as plt

aut = trl.Automaton()
aut.declare_variables(active=(1, 2), 
                      sysX1=(0,2), sysY1 = (0,2), k1 = (0,1), kR1 = (0,2), goTo1 = (0,2))
aut.varlist['env']=['active']
aut.varlist['sys']=['sysX1','sysY1','k1','kR1','goTo1']
aut.prime_varlists()

specs = '''

envInit ==
    /\ active = 1

envNext ==
    /\ (active \in 1..2 /\ active' \in 1..2)
    /\ (active' = active \/ active' != active)

dynamics1 == 
    /\ (sysX1 \in 0..2 /\ sysY1 \in 0..2)
    /\ (sysX1' \in 0..2 /\ sysY1' \in 0..2)
    /\ (k1' \in 0..1 /\ k1 \in 0..1)
    /\ (kR1' \in 0..2 /\ kR1 \in 0..2)
    /\ (goTo1' \in 0..2 /\ goTo1 \in 0..2)

    /\ (sysX1' = sysX1 => sysY1' != sysY1)
    /\ (sysY1' = sysY1 => sysX1' != sysX1)

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

sysInit1 ==
    /\ (sysX1 \in 0..2 /\ sysY1 \in 0..2)
    /\ (k1 \in 0..1)
    /\ (kR1 \in 0..2)
    /\ (goTo1 = 0)

UNC_Vars ==
    /\ kR1' = kR1
    /\ k1' = k1
    /\ goTo1' = goTo1

sysStep1 ==
    /\ dynamics1

    /\ ((~room11 /\ ~room21 /\ ~home1) => UNC_Vars)

    /\ ((room11 /\ active = 1) => (k1' = 1 /\ kR1' = 1 /\ goTo1' = 0))
    /\ ((room11 /\ active != 1) => (k1' = 0 /\ kR1' = 0 /\ goTo1' = 2))

    /\ ((room21 /\ active = 2) => (k1' = 1 /\ kR1' = 2 /\ goTo1' = 0))
    /\ ((room21 /\ active != 2) => (k1' = 0 /\ kR1' = 0 /\ goTo1' = 1))

    /\ (X room21) => (goTo1' = 2)

    /\ ((home1) => (k1 != 0 /\ kR1 != 0 /\ k1' = k1 /\ kR1' = kR1 /\ goTo1' = kR1))
    /\ (goTo1 = 0 => (~ X room21 /\ ~ X room11))

environmentInit == envInit
environmentNext == envNext
sysInit == sysInit1 
sysNext == sysStep1
'''

aut.define(specs)
aut.init.update(
    env='envInit',
    sys='sysInit')
aut.action.update(
    env='envNext',
    sys='sysNext')

# aut.win['<>[]'] = aut.bdds_from('(sysX1 = 0 /\ sysY1 = 0)','(sysX1 = 2 /\ sysY1 = 0)', '(sysX1 = 0 /\ sysY1 = 2)')
# aut.win['[]<>'] = aut.bdds_from('(sysX1 = 0 /\ sysY1 = 0)','(sysX1 = 2 /\ sysY1 = 0)', '(sysX1 = 0 /\ sysY1 = 2)')

aut.win['<>[]'] = aut.bdds_from('(sysX1 = 0 /\ sysY1 = 0)')
aut.win['[]<>'] = aut.bdds_from('(sysX1 = 2 /\ sysY1 = 0)', '(sysX1 = 0 /\ sysY1 = 2)')

aut.qinit = '\E \A'
aut.moore = True
aut.plus_one = True

# g = enum.action_to_steps(aut, 'env', 'sys', qinit=aut.qinit)
# h, _ = sym_enum._format_nx(g)
# pd = nx.drawing.nx_pydot.to_pydot(h)
# pd.write_pdf('outputs/single_gridworld_game_states_omega.pdf')

z, yij, xijk = gr1.solve_streett_game(aut)
gr1.make_streett_transducer(z, yij, xijk, aut)
aut.varlist['sys'].append('_goal')
aut.prime_varlists()
# enumerate
g = enum.action_to_steps(aut, 'env', 'impl', qinit=aut.qinit)
h, _ = sym_enum._format_nx(g)
pd = nx.drawing.nx_pydot.to_pydot(h)
pd.write_pdf('outputs/single_gridworld_game_states_omega.pdf')

