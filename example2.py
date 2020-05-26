from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic.enumeration import _dump_graph_as_figure

aut = trl.Automaton()
aut.declare_variables(R_x=(-22, 22), E_x=(-22, 22), direction=(-1, 1))

aut.varlist['env']=['E_x']
aut.varlist['sys']=['R_x']
aut.prime_varlists()

aut.init['env'] = '''
    /\ E_x = 0
    /\ R_x=-20
    '''
aut.init['sys'] = 'TRUE'

aut.action['sys'] = '''
    (* type invariant *)
    /\ (R_x \in -21..21)
    /\ (R_x' \in -21..21)

    (* inversion with one-step delay *)
    /\ ((R_x' < R_x + 3) /\ (R_x' > R_x - 3))
    /\ (R_x' != R_x)
    '''

aut.action['env'] = '''
    (* type invariant *)
    /\ (E_x \in -21..21)
    /\ (E_x' \in -21..21)

    (* inversion with one-step delay *)
    /\ ((E_x' < E_x + 3) /\ (E_x' > E_x - 3))
    /\ (E_x' != E_x)
    '''

aut.win['<>[]'] = aut.bdds_from("R_x=E_x")
aut.win['[]<>'] = aut.bdds_from("R_x = 20")

aut.qinit = '\A \A'
aut.moore = True
aut.plus_one = True

z, yij, xijk = gr1.solve_streett_game(aut)
gr1.make_streett_transducer(z, yij, xijk, aut)

# enumerate
g = enum.action_to_steps(aut, 'env', 'impl', qinit=aut.qinit)
# plot
_dump_graph_as_figure(g, 'test.png')