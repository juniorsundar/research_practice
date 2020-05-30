from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic.enumeration import _dump_graph_as_figure
import random as rand

aut = trl.Automaton()
MAX_ROOMS = 6
aut.declare_variables(active=(1, MAX_ROOMS), known_room=(0, MAX_ROOMS), pos=(0, MAX_ROOMS), known=(0,1))

aut.varlist['env']=['active']
aut.varlist['sys']=['known_room','known','pos']
aut.prime_varlists()

aut.init['env'] = 'active = 1'
aut.init['sys'] = '''
    /\ pos = 1
    /\ known_room = 0
    /\ known=0
    '''

aut.action['sys'] = '''
    (* inversion with one-step delay *)
    /\  \/ (pos = 0 /\ pos' > 0)
        \/ (pos > 0 /\ pos' = 0)

    /\  \/ ((pos = active) /\ (known'=1 /\ known_room'=pos))
        \/ ((pos != active) /\ (known'=0 /\ known_room'=0))

    /\  ((known = 1) => (pos' = known_room))
    '''

aut.action['env'] = '''
    /\ active \in 0..6
    /\ active' \in 0..6
    /\ active' = active \/ active' != active
    '''
# aut.win['<>[]'] = aut.bdds_from('pos \in 0..6')
# aut.win['[]<>'] = aut.bdds_from('pos != 4')
aut.qinit = '\E \A'
aut.moore = True
aut.plus_one = True

# z, yij, xijk = gr1.solve_streett_game(aut)
# a = gr1.make_streett_transducer(z, yij, xijk, aut)
# enumerate
g = enum.action_to_steps(aut, 'env', 'sys', qinit=aut.qinit)
_dump_graph_as_figure(g, 'action_to_step.pdf')

#%%
# active = [g._node[0]['active']]
# known_room = [g._node[0]['known_room']]
# known = [g._node[0]['known']]
# pos = [g._node[0]['pos']]
# successors = g._succ[0]

# for i in range(0,20):
#     random = rand.randint(0,len(successors)-1)
#     nextIdx = list(successors.keys())[random]
#     print(list(successors.keys()))
#     print(nextIdx)
#     active.append(g._node[nextIdx]['active'])
#     known_room.append(g._node[nextIdx]['known_room'])
#     known.append(g._node[nextIdx]['known'])
#     pos.append(g._node[nextIdx]['pos'])
#     successors = g._succ[nextIdx]

# g = enum.enumerate_state_machine(aut.init['sys'],aut.action['sys'],aut)
# _dump_graph_as_figure(g, 'enumerate_state_machine.pdf')

