from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum
import networkx as nx

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
    /\ pos \in 0..2
    /\ pos' \in 0..2
    /\ known_room \in 0..2
    /\ known_room' \in 0..2
    /\ home \in 0..1
    /\ home' \in 0..1
    /\ known \in 0..1
    /\ known' \in 0..1

    /\  \/ (home = 1 /\ pos = 0) 
        \/ (home = 0 /\ pos != 0)
    /\ ~(home = 1) \/ (home' = 0)
    (* inversion with one-step delay *)

    /\ ~(home = 0 /\ pos = active) \/ (known' = 1 /\ known_room' = pos /\ home' = 1)
    /\ ~(home = 1 /\ known = 1 /\ known_room > 0) \/ (known' = 1 /\ known_room' = known_room /\ pos' = known_room)

    /\ ~(home = 0 /\ (pos != active)) \/ (known' = 0 /\ known_room' = 0 /\ pos' != pos /\ home' = 0)
    '''

aut.action['env'] = '''
    /\ active \in 1..2
    /\ active' \in 1..2
    /\ (active' = active \/ active' != active)
'''
# aut.win['<>[]'] = aut.bdds_from('active1 \/ active2')
# aut.win['[]<>'] = aut.bdds_from('active1 \/ active2')
aut.qinit = '\E \A'
aut.moore = True
aut.plus_one = True

# z, yij, xijk = gr1.solve_streett_game(aut)
# gr1.make_streett_transducer(z, yij, xijk, aut)
# aut.varlist['sys'].append('_goal')
# aut.prime_varlists()
# enumerate
g = enum.action_to_steps(aut, 'env', 'sys', qinit=aut.qinit)
h, _ = sym_enum._format_nx(g)
pd = nx.drawing.nx_pydot.to_pydot(h)
pd.write_pdf('game_states.pdf')


