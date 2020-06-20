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

    /\ \/ ((envX = 0) /\ (envX' = 1))
       \/ ((envX = 1) /\ (envX' = 0 \/ envX' = 2))
       \/ ((envX = 2) /\ (envX' = 1))

    /\ \/ ((envY = 0) /\ (envY' = 1))
       \/ ((envY = 1) /\ (envY' = 0 \/ envY' = 2))
       \/ ((envY = 2) /\ (envY' = 1))
    '''
aut.action['sys'] = '''
    /\ (sysX \in 0..2 /\ sysY \in 0..2)
    /\ (sysX' \in 0..2 /\ sysY' \in 0..2)

    /\ ((sysX = 0) => (sysX' = 1))
    /\ ((sysX = 1) => (sysX' = 0 \/ sysX' = 2))
    /\ ((sysX = 2) => (sysX' = 1))

    /\ ((sysY = 0) => (sysY' = 1))
    /\ ((sysY = 1) => (sysY' = 0 \/ sysY' = 2))
    /\ ((sysY = 2) => (sysY' = 1))
    '''

specs = '''
Aroom1 == envX = 2 /\ envY = 0
Aroom2 == envX = 0 /\ envY = 2
room1 == sysX = 2 /\ sysY = 0
room2 == sysX = 0 /\ sysY = 2
home == sysX = 0 /\ sysY = 0
Kroom1 == kX = 2 /\ kY = 0
Kroom2 == kX = 0 /\ kY = 2
Khome == kX = 0 /\ kY = 0

right == sysX' = sysX + 1
left == sysX' = sysX - 1
up == sysY' = sysY + 1
down == sysY' = sysY - 1

nonStuttering == (sysX' != sysX /\ sysY' != sysY)

travelling == ~ (home \/ room1 \/ room2)

sysGOTOR1 ==
    /\ ((2 > sysX) => right)  
    /\ ((0 < sysY) => down)

sysGOTOR2 ==
    /\ ((0 < sysX) => left)  
    /\ ((2 > sysY) => up)

sysGOHOME ==
    /\ ((sysX > 0) => left)  
    /\ ((sysY > 0) => down)

sysStep ==
    /\ nonStuttering
    /\ (k = 1 /\ Kroom1 /\ (travelling \/ home)) => (k' = 1 /\ kX' = kX /\ kY' = kY)
    /\ (k = 1 /\ Kroom2 /\ (travelling \/ home)) => (k' = 1 /\ kX' = kX /\ kY' = kY)
    /\ (Aroom1 /\ room1) => (k' = 1 /\ kX' = 2 /\ kY' = 0)
    /\ (Aroom2 /\ room2) => (k' = 1 /\ kX' = 0 /\ kY' = 2) 
    /\ Kroom1 => sysGOTOR1
    /\ kroom2 => sysGOTOR2
'''

aut.win['<>[]'] = aut.bdds_from('sysX=2 /\ sysY=2','sysX=0 /\ sysY=0')
aut.win['[]<>'] = aut.bdds_from('sysX=2 /\ sysY=2','sysX=0 /\ sysY=0')
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