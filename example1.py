from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic.enumeration import _dump_graph_as_figure


# declarations
aut = trl.Automaton()
aut.declare_variables(x=(1, 6), y=(1, 6))
aut.varlist['env'] = ['x']
aut.varlist['sys'] = ['y']
aut.prime_varlists()
aut.moore = True
# specification using stepwise implication
aut.init['env'] = 'x = 1 /\ y = 2'
aut.init['sys'] = aut.true
aut.action['sys'] = " x < 5 /\ y' = IF x = 4 THEN 1 ELSE x "
aut.action['env'] = " x \in 1..4 /\ x' \in 1..4 "
# enumerate and plot
g = action_to_steps(aut, 'env', 'sys', qinit='\A \A')
_dump_graph_as_figure(g, 'foo.pdf')