from matplotlib import pyplot as plt
from omega.games import gr1
from omega.logic import syntax as stx
from omega import steps
from omega.symbolic import temporal as trl
from omega.games import enumeration as enum
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum

import networkx as nx

MAX_ROOMS = 2

# def specify_component_1():
#     global MAX_ROOMS
#     aut = trl.Automaton()
#     aut.players = ['sys1','env','scheduler']
#     aut.declare_variables(active = (1,MAX_ROOMS), 
#                           home1 = (0,1), 
#                           known_room1 = (0, MAX_ROOMS), 
#                           pos1 = (0, MAX_ROOMS), 
#                           known1 = (0,1),
#                           turn=(0,2))
#     aut.varlist['scheduler']=['turn']
#     aut.varlist['env']=['active']
#     aut.varlist['sys1']=['known_room1','known1','pos1','home1']
#     spec = r'''
#     sys1Init == pos1 = 0 /\ home1 = 1 /\ known_room1 = 0 /\ known1 = 0
    
#     '''

# def specify_component_2():


# def specify_environment():



aut = trl.Automaton()
aut.players = dict(env=1,sys1=2,sys2=3,scheduler=None)
vrs = dict(active = (1,MAX_ROOMS), 
           home1 = (0,1), 
           known_room1 = (0, MAX_ROOMS), 
           pos1 = (0, MAX_ROOMS), 
           known1 = (0,1), 
           home2 = (0,1), 
           known_room2 = (0, MAX_ROOMS), 
           pos2 = (0, MAX_ROOMS), 
           known2 = (0,1),
           t = (1,3))
aut.declare_variables(**vrs)
aut.varlist = dict(
    env = ['active'],
    sys1 = ['known_room1','known1','pos1','home1'],
    sys2 = ['known_room2','known2','pos2','home2'],
    scheduler = ['t']
)
s = r'''
    UNCHANGED_env == active' = active

    UNCHANGED_sys1 == 
    /\ home1' = home1
    /\ pos1' = pos1
    /\ known1' = known1
    /\ known_room1' = known_room1

    UNCHANGED_sys2 == 
    /\ home2' = home2
    /\ pos2' = pos2
    /\ known2' = known2
    /\ known_room2' = known_room2

    envInit == 
    /\ active = 1

    sys1Init ==
    /\ pos1 = 0
    /\ home1 = 1
    /\ known_room1 = 0
    /\ known1 = 0

    sys2Init ==
    /\ pos2 = 0
    /\ home2 = 1
    /\ known_room2 = 0
    /\ known2 = 0

    envTurn == t = 1
    sys1Turn == t = 2
    sys2Turn == t = 3

    envInv ==
    /\ (active \in 1..2)

    sys1Inv ==
    /\ (home1 = 1 <=> pos1 = 0)

    sys2Inv ==
    /\ (home2 = 1 <=> pos2 = 0)

    envStep == 
    /\ envTurn
    /\ active' \in 1..2
    /\ (active' = active \/ active' != active)

    sys1Step ==
    /\ sys1Turn
    /\ (home1 = 1 => home1' = 0)
    /\ (~(home1 = 0 /\ known1' = 1) \/ home1' = 1)
    /\ (pos1' != pos1)

    /\ (~(home1 = 0 /\ pos1 = 1 /\ active = 1) \/ (known1' = 1 /\ known_room1' = 1))
    /\ (~(home1 = 0 /\ pos1 = 2 /\ active = 2) \/ (known1' = 1 /\ known_room1' = 2))

    /\ (~(home1 = 1 /\ known1 = 1 /\ known_room1 = 1) \/ (known1' = 1 /\ known_room1' = 1 /\ pos1' = 1))
    /\ (~(home1 = 1 /\ known1 = 1 /\ known_room1 = 2) \/ (known1' = 1 /\ known_room1' = 2 /\ pos1' = 2))

    /\ (~(home1 = 0 /\ (pos1 = 2 /\ active != 2)) \/ (known1' = 0 /\ known_room1' = 0 /\ pos1' = 1))
    /\ (~(home1 = 0 /\ (pos1 = 1 /\ active != 1)) \/ (known1' = 0 /\ known_room1' = 0 /\ pos1' = 2))

    sys2Step ==
    /\ sys2Turn
    /\ (home2 = 1 => home2' = 0)
    /\ (home2 = 1 <=> pos2 = 0)
    /\ (~(home2 = 0 /\ known2' = 1) \/ home2' = 1)
    /\ (pos2' != pos2)

    /\ (~(home2 = 0 /\ pos2 = 1 /\ active = 1) \/ (known2' = 1 /\ known_room2' = 1))
    /\ (~(home2 = 0 /\ pos2 = 2 /\ active = 2) \/ (known2' = 1 /\ known_room2' = 2))

    /\ (~(home2 = 1 /\ known2 = 1 /\ known_room2 = 1) \/ (known2' = 1 /\ known_room2' = 1 /\ pos2' = 1))
    /\ (~(home2 = 1 /\ known2 = 1 /\ known_room2 = 2) \/ (known2' = 1 /\ known_room2' = 2 /\ pos2' = 2))

    /\ (~(home2 = 0 /\ (pos2 = 2 /\ active != 2)) \/ (known2' = 0 /\ known_room2' = 0 /\ pos2' = 1))
    /\ (~(home2 = 0 /\ (pos2 = 1 /\ active != 1)) \/ (known2' = 0 /\ known_room2' = 0 /\ pos2' = 2))

    envNext ==
    /\ envInv
    /\ \/ envStep
       \/ UNCHANGED_env

    sys1Next ==
    /\ sys1Inv
    /\ \/ sys1Step
       \/ UNCHANGED_sys1

    sys2Next ==
    /\ sys2Inv
    /\ \/ sys2Step
       \/ UNCHANGED_sys2
    
    schedulerInit == (t = 1)
    schedulerNext ==
    /\ ((t = 1) => (t' = 2))
    /\ ((t = 2) => (t' = 3))
    /\ ((t = 3) => (t' = 1))
    /\ (t \in 1..3)
'''

aut.define(s)
aut.init.update(env='envInit',sys1='sys1Init',sys2='sys2Init',scheduler='schedulerInit')
aut.action.update(env='envNext',sys1='sys1Next',sys2='sys2Next',scheduler='schedulerNext')
aut.win['<>[]'] = aut.bdds_from('active=1 \/ active=2')
aut.win['[]<>'] = aut.bdds_from('active=1 \/ active=2')

# aut.win = dict(env={'[]<>':aut.bdds_from('active=1 \/ active=2'),
#                     '<>[]':aut.bdds_from('active=1 \/ active=2')},
#                sys1={'[]<>':aut.bdds_from('pos 1 = 0'),
#                      '<>[]':aut.bdds_from('pos1 = 0')},
#                sys2={'[]<>':aut.bdds_from('pos2 = 0'),
#                      '<>[]':aut.bdds_from('pos2 = 0')},
#                scheduler={'[]<>':aut.bdds_from('t=1 \/ t=2 \/ t=3'),
#                           '<>[]':aut.bdds_from('t=1 \/ t=2 \/ t=3')})

aut.prime_varlists(['env','sys1','sys2','scheduler'])
aut.qinit = '\E \A'
aut.moore = True
aut.plus_one = True

z, yij, xijk = gr1.solve_streett_game(aut)
# gr1.make_streett_transducer(z, yij, xijk, aut)
# aut.varlist['sys1'].append('_goal')
# # aut.varlist['sys2'].append('_goal')
# aut.prime_varlists()

g1 = enum.action_to_steps(aut, 'scheduler', 'sys1', qinit=aut.qinit)
g2 = enum.action_to_steps(aut, 'scheduler', 'sys2', qinit=aut.qinit)
g3 = enum.action_to_steps(aut, 'scheduler', 'env', qinit=aut.qinit)

h, _ = sym_enum._format_nx(g1)
pd = nx.drawing.nx_pydot.to_pydot(h)
pd.write_pdf('assembly1.pdf')

h, _ = sym_enum._format_nx(g2)
pd = nx.drawing.nx_pydot.to_pydot(h)
pd.write_pdf('assembly2.pdf')

h, _ = sym_enum._format_nx(g3)
pd = nx.drawing.nx_pydot.to_pydot(h)
pd.write_pdf('assembly3.pdf')