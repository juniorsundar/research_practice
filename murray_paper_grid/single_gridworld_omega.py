from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum
import networkx as nx

import matplotlib.pyplot as plt

aut = trl.Automaton()
aut.declare_variables(active=(1, 2), 
                      pos1 = (-1,2), rX1=(0,4), rY1 = (0,4), goTo1 = (0,2))
aut.varlist['env']=['active']
aut.varlist['sys']=['rX1','rY1','goTo1','pos1']
aut.prime_varlists()

specs = '''

envInit ==
    /\ active = 1

envNext ==
    /\ (active \in 1..2 /\ active' \in 1..2)
    /\ (active' = active \/ active' != active)

rob1_init ==
    /\ pos1 = 0
    /\ goTo1 = 1
    /\ rX1 = 0 /\ rY1 = 0

room11 ==
    /\ rX1 = 4 /\ rY1 = 0

room21 ==
    /\ rX1 = 0 /\ rY1 = 4

home1 ==
    /\ rX1 = 0 /\ rY1 = 0

rob1_step ==
    /\ pos1 \in -1..2 /\ pos1' \in -1..2
    /\ goTo1 \in 0..2 /\ goTo1' \in 0..2
    /\ (pos1 = 1 => room11)
    /\ (pos1 = 2 => room21)

    /\ (pos1 = -1 => (~home1 /\ ~room21 /\ ~room11 /\ pos1' = goTo1 /\ goTo1' = goTo1 /\ rX1 \in 0..4 /\ rY1 \in 0..4))
    /\ ((pos1 = 1 /\ active = 1) => (goTo1' = 0 /\ pos1' = -1))
    /\ ((pos1 = 2 /\ active = 2) => (goTo1' = 0 /\ pos1' = -1))
    /\ ((pos1 = 1 /\ active != 1) => (goTo1' = 2 /\ pos1' = -1))
    /\ ((pos1 = 2 /\ active != 2) => (goTo1' = 1 /\ pos1' = -1))
    /\ (pos1 = 0  => (home1 /\ goTo1' = 1 /\ pos1' = -1))

environmentInit == envInit
environmentNext == envNext
sysInit == rob1_init 
sysNext == rob1_step
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

aut.win['<>[]'] = aut.bdds_from('TRUE')
aut.win['[]<>'] = aut.bdds_from('pos1 = 1','pos1 = 2')

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
pd.write_pdf('single_gridworld_game_states_omega.pdf')

