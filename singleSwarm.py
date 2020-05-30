from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic.enumeration import _dump_graph_as_figure

aut = trl.Automaton()
aut.declare_variables(active=(1, 6), known_idx=(0, 6), pos=(0, 6), known=(0,1))

aut.varlist['env']=['active']
aut.varlist['sys']=['known_idx','known','pos']
aut.prime_varlists()

aut.init['env'] = 'active = 1'
aut.init['sys'] = '''
    /\ pos = 1
    /\ known_idx = 0
    /\ known=0
    '''

aut.action['sys'] = '''
    /\ pos \in 0..6
    /\ pos' \in 0..6
    
    (* inversion with one-step delay *)
    /\ pos' != pos
    /\  \/ (pos = 0 /\ pos' > 0)
        \/ (pos > 0 /\ pos' = 0)
    /\  \/ ((pos = active) /\ (known'=1 /\ known_idx'=pos))
        \/ ((pos != active) /\ (known'=0 /\ known_idx'=0))
    /\  \/((known=1) /\ (pos' = known_idx))
        \/(known = 0)
    '''

aut.action['env'] = '''
    /\ active > 0
    /\ active' > 0
    '''
aut.win['<>[]'] = aut.bdds_from('pos \in 0..6')
aut.win['[]<>'] = aut.bdds_from('known = 1')
aut.qinit = '\E \A'
aut.moore = True
aut.plus_one = True

z, yij, xijk = gr1.solve_streett_game(aut)
a = gr1.make_streett_transducer(z, yij, xijk, aut)
# enumerate
g = enum.action_to_steps(aut, 'env', 'sys', qinit=aut.qinit)
_dump_graph_as_figure(g, 'action_to_step.pdf')
g.get_edge_data(0,1)

# g = enum.enumerate_state_machine(aut.init['sys'],aut.action['sys'],aut)
# _dump_graph_as_figure(g, 'enumerate_state_machine.pdf')

