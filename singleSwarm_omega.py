from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum
import networkx as nx

import matplotlib.pyplot as plt

aut = trl.Automaton()
MAX_ROOMS = 2
aut.declare_variables(active=(1,MAX_ROOMS), home = (0,1),known_room=(0, MAX_ROOMS), pos=(0, MAX_ROOMS), known=(0,1))
aut.varlist['env']=['active']
aut.varlist['sys']=['known_room','known','pos','home']
aut.prime_varlists()

aut.init['env'] = '''
    /\ active = 1
    '''
aut.init['sys'] = '''
    /\ pos = 0
    /\ home = 1
    /\ known_room = 0
    /\ known = 0
    '''

aut.action['sys'] = '''
    /\ (home = 1 => home' = 0)
    /\ (home = 1 <=> pos = 0)
    /\ (~(home = 0 /\ known' = 1) \/ home' = 1)
    /\ (pos' != pos)

    /\ (~(home = 0 /\ pos = 1 /\ active = 1) \/ (known' = 1 /\ known_room' = 1))
    /\ (~(home = 0 /\ pos = 2 /\ active = 2) \/ (known' = 1 /\ known_room' = 2))

    /\ (~(home = 1 /\ known = 1 /\ known_room = 1) \/ (known' = 1 /\ known_room' = 1 /\ pos' = 1))
    /\ (~(home = 1 /\ known = 1 /\ known_room = 2) \/ (known' = 1 /\ known_room' = 2 /\ pos' = 2))

    /\ (~(home = 0 /\ (pos = 2 /\ active != 2)) \/ (known' = 0 /\ known_room' = 0 /\ pos' = 1))
    /\ (~(home = 0 /\ (pos = 1 /\ active != 1)) \/ (known' = 0 /\ known_room' = 0 /\ pos' = 2))
    '''

aut.action['env'] = '''
    /\ active \in 1..2
    /\ active' \in 1..2
    /\ (active' = active \/ active' != active)
'''
aut.win['<>[]'] = aut.bdds_from('active=1 \/ active=2')
aut.win['[]<>'] = aut.bdds_from('active=1 \/ active=2')
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

active = 1
activeR = -1
room = 0
roomR = 0
current = 0
while True:
    plt.axis([-2,2,-3,4])
    plt.plot([-.25,.25,.25,-.25,-.25],[-2,-2,2,2,-2],c='red')
    plt.plot([-1.25,-.75,-.75,-1.25,-1.25],[-1,-1,1,1,-1],c=(0,0.5,1))
    plt.plot([.75,1.25,1.25,.75,.75],[-1,-1,1,1,-1],c=(0.5,1,0))

    # environment
    plt.scatter([activeR],[0.5],c='green')
    # system
    plt.scatter([roomR],[-.5],c='blue')
    plt.legend(['Home','Room 1','Room 2','Env. Player','Robot'])
    plt.show()
    # environment input
    active = int(input("Environment's Next Step: "))
    successors = list(g._succ[current].keys())
    
    if active == 1:
        activeR = -1
        for suc in successors:
            if g._node.get(suc)['active'] == 1:
                current = suc
    elif active == 2:
        activeR = 1
        for suc in successors:
            if g._node.get(suc)['active'] == 2:
                current = suc
    room = g._node.get(current)['pos']
    print("Robot goes to room {}".format(room))
    if room == 0:
        roomR = 0
    elif room == 1:
        roomR = -1
    elif room == 2:
        roomR = 1          