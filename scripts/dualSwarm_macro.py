#%%
from omega.games import gr1
from omega.games import enumeration as enum
from omega.symbolic import temporal as trl
from omega.games.enumeration import action_to_steps
from omega.symbolic import enumeration as sym_enum
import networkx as nx
import matplotlib.pyplot as plt

#%%
aut = trl.Automaton()
aut.declare_variables(room1=(1, 2), room2=(1, 2),
                      pos1 = (-1, 2), pos2 = (-1, 2),
                      goTo1 = (0, 2), goTo2 = (0, 2))
aut.varlist['env']=['room1', 'room2']
aut.varlist['sys']=['pos1', 'goTo1', 'goTo2', 'pos2']
aut.prime_varlists()

#%%
specs = '''
env_init == 
/\ room1 = 1
/\ room2 = 2

env_action ==
/\ room1 \in 1..2 /\ room2 \in 1..2
/\ room1' \in 1..2 /\ room2' \in 1..2

/\ room1 != room2
/\ room1' != room2'

sys_init ==
/\ pos1 = 1 /\ pos2 = 2
/\ goTo1 = 1 /\ goTo2 = 2

sys_action ==
/\ pos1 \in -1..2 /\ pos1' \in -1..2
/\ pos2 \in -1..2 /\ pos2' \in -1..2
/\ goTo1 \in 0..2 /\ goTo1' \in 0..2
/\ goTo2 \in 0..2 /\ goTo2' \in 0..2

/\ ((pos1 = 0) => (pos1' = -1 /\ goTo1' = 1))
/\ ((pos1 = -1) => (pos1' = goTo1 /\ goTo1' = goTo1))

/\ ((pos1 = 1 /\ room1 = 1) => (pos1' = -1 /\ goTo1' = 0))
/\ ((pos1 = 1 /\ room1 != 1) => (pos1' = -1 /\ goTo1' = 2))
/\ ((pos1 = 2 /\ room1 = 2) => (pos1' = -1 /\ goTo1' = 0))
/\ ((pos1 = 2 /\ room1 != 2) => (pos1' = -1 /\ goTo1' = 1))


/\ ((pos2 = 0) => (pos2' = -1 /\ goTo2' = 2))
/\ ((pos2 = -1) => (pos2' = goTo2 /\ goTo2' = goTo2))

/\ ((pos2 = 1 /\ room2 = 1) => (pos2' = -1 /\ goTo2' = 0))
/\ ((pos2 = 1 /\ room2 != 1) => (pos2' = -1 /\ goTo2' = 2))
/\ ((pos2 = 2 /\ room2 = 2) => (pos2' = -1 /\ goTo2' = 0))
/\ ((pos2 = 2 /\ room2 != 2) => (pos2' = -1 /\ goTo2' = 1))
'''

#%%
aut.define(specs)
aut.init.update(
    env='env_init',
    sys='sys_init')
aut.action.update(
    env='env_action',
    sys='sys_action')
aut.win['<>[]'] = aut.bdds_from('TRUE')
aut.win['[]<>'] = aut.bdds_from('TRUE')
aut.qinit = '\E \A'
aut.moore = True
aut.plus_one = True

z, yij, xijk = gr1.solve_streett_game(aut)
gr1.make_streett_transducer(z, yij, xijk, aut)
aut.varlist['sys'].append('_goal')
aut.prime_varlists()
g = enum.action_to_steps(aut, 'env', 'impl', qinit=aut.qinit)

#%%
h, _ = sym_enum._format_nx(g)
pd = nx.drawing.nx_pydot.to_pydot(h)
pd.write_pdf('outputs/game_states_macro.pdf')
    

# %%
