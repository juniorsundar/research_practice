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
aut.declare_variables(sysX=(0,2), sysY = (0,2), envX=(0, 2), envY=(0, 2))
aut.varlist['env']=['envX','envY']
aut.varlist['sys']=['sysX','sysY']
aut.prime_varlists()

aut.init['env'] = '''
    /\ envX = 2
    /\ envY = 2
    '''
aut.init['sys'] = '''
    /\ sysX = 0
    /\ sysY = 0
    '''
aut.action['env'] = '''
    /\ (envX \in 0..2 /\ envY \in 0..2)
    /\ (envX' \in 0..2 /\ envY' \in 0..2)
    /\ envX' != envX /\ envY' != envY

    /\ envX = 0 => (envX' = 0 \/ envX' = 1)
    /\ envX = 1 => (envX' = 0 \/ envX' = 1 \/ envX' = 2)
    /\ envX = 2 => (envX' = 1 \/ envX' = 2)

    /\ envY = 0 => (envY' = 0 \/ envY' = 1)
    /\ envY = 1 => (envY' = 0 \/ envY' = 1 \/ envY' = 2)
    /\ envY = 2 => (envY' = 1 \/ envY' = 2)
    '''
aut.action['sys'] = '''
    /\ (sysX \in 0..2 /\ sysY \in 0..2)
    /\ (sysX' \in 0..2 /\ sysY' \in 0..2)

    /\ \/ ((sysX = 0) /\ (sysX' = 0 \/ sysX' = 1))
       \/ ((sysX = 1) /\ (sysX' = 0 \/ sysX' = 1 \/ sysX' = 2))
       \/ ((sysX = 2) /\ (sysX' = 1 \/ sysX' = 2))

    /\ \/ ((sysY = 0) /\ (sysY' = 0 \/ sysY' = 1))
       \/ ((sysY = 1) /\ (sysY' = 0 \/ sysY' = 1 \/ sysY' = 2))
       \/ ((sysY = 2) /\ (sysY' = 1 \/ sysY' = 2))
    '''


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
pd.write_pdf('game_states_omega.pdf')