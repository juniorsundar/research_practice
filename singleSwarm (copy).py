from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum
import networkx as nx

aut = trl.Automaton()
MAX_ROOMS = 2
aut.declare_variables(active1='bool',active2='bool', home = 'bool',known_room=(0, MAX_ROOMS), pos=(0, MAX_ROOMS), known='bool')
aut.varlist['env']=['active1','active2']
aut.varlist['sys']=['known_room','known','pos','home']
aut.prime_varlists()

aut.init['env'] = '''
    /\ active1
    /\ ~active2
    '''
aut.init['sys'] = '''
    /\ pos = 0
    /\ home
    /\ known_room = 1
    /\ known
    '''

aut.action['sys'] = '''
    /\ home <=> pos = 0
    /\ ~home => (~ home')
    /\ home => (~ home')
    (* inversion with one-step delay *)

    /\ ((pos = 1 /\ active1) => (known') /\ known_room' = 1)
    /\ ((pos = 2 /\ active2) => (known') /\ known_room' = 2)
    /\ ~home => ~known
    /\ known /\ known_room = 1 => pos' = 1
    /\ known /\ known_room = 2 => pos' = 2
    '''

aut.action['env'] = '''
    /\ active1 <=> ~active2
    '''
aut.win['<>[]'] = aut.bdds_from('active1')
aut.win['[]<>'] = aut.bdds_from('home')
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
pd.write_pdf('game_states.pdf')


