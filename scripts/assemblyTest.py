#!/usr/bin/env python
"""Synthesize two Moore implementations, and simulate their assembly."""
from matplotlib import pyplot as plt
from omega.games import gr1
from omega.logic import syntax as stx
from omega import steps
from omega.symbolic import temporal as trl


def main():
    """Synthesize two Moore components, assemble, and simulate them."""
    # synthesize
    foo_spec = specify_component_foo()
    bar_spec = specify_component_bar()
    synthesize_some_controller('bar', 'foo', foo_spec)
    synthesize_some_controller('foo', 'bar', bar_spec)
    # assemble
    foo = steps.AutomatonStepper(foo_spec)
    bar = steps.AutomatonStepper(bar_spec)
    sch = steps.Scheduler(2)
    asm = steps.Assembly()
    asm.machines = dict(scheduler=sch, foo=foo, bar=bar)
    # history
    n_steps = 20
    asm.init()
    print(asm.state)
    for _ in range(n_steps):
        asm.step()
        print(asm.state)
    # plotting
    plot_machines(asm)
    plt.xlabel('behavior states')
    plt.show()


def specify_component_foo():
    """Return temporal logic spec of component foo."""
    aut = trl.Automaton()
    aut.players = ['foo', 'bar', 'scheduler']
    aut.declare_variables(active=(1, 2), home = (0,1),known_room=(0, 2), pos=(0, 2), known=(0,1), turn=(0, 1))
    aut.varlist['scheduler'] = ['turn']
    aut.varlist['foo'] = ['active']
    aut.varlist['bar'] = ['known_room','known','pos','home']
    spec = r'''
    FooInit == active = 1
    BarInit == 
    /\ pos = 0
    /\ home = 1
    /\ known_room = 1
    /\ known = 1
    /\ turn = 1

    INV ==
    /\ pos \in 0..2
    /\ known_room \in 0..2
    /\ home \in 0..1
    /\ known \in 0..1

    BarUNCHANGED ==
    /\ home' = home
    /\ pos' = pos
    /\ known' = known
    /\ known_room' = known_room

    BarAction ==
        /\ INV
        /\ (home = 1 => home' = 0)
        /\ (home = 1 <=> pos = 0)
        /\ (~(home = 0 /\ known' = 1) \/ home' = 1)

        /\ (~(home = 0 /\ pos = 1 /\ active = 1) \/ (known' = 1 /\ known_room' = 1))
        /\ (~(home = 0 /\ pos = 2 /\ active = 2) \/ (known' = 1 /\ known_room' = 2))

        /\ (~(home = 1 /\ known = 1 /\ known_room = 1) \/ (known' = 1 /\ known_room' = 1 /\ pos' = 1))
        /\ (~(home = 1 /\ known = 1 /\ known_room = 2) \/ (known' = 1 /\ known_room' = 2 /\ pos' = 2))

        /\ (~(home = 0 /\ (pos = 2 /\ active != 2)) \/ (known' = 0 /\ known_room' = 0 /\ pos' = 1))
        /\ (~(home = 0 /\ (pos = 1 /\ active != 1)) \/ (known' = 0 /\ known_room' = 0 /\ pos' = 2))
    
    FooNext ==
        \/ ((turn = 1) /\ (active' = active))
        \/  /\ (turn = 0 /\ active \in 1..2 /\ active' \in 1..2)
            /\ (active' = active \/ active' != active) 

    BarNext ==
        \/ ((turn = 1) /\ (BarAction))
        \/  /\ ((turn = 0) /\ (BarUNCHANGED))
            /\ (turn' = 1)
    '''
    aut.define(spec)
    aut.init.update(
        foo='FooInit',
        bar='BarInit')
    aut.action.update(
        foo='FooNext',
        bar='BarNext')
    aut.win = dict(
        foo={'<>[]': aut.bdds_from('turn = 0', 'turn = 1'),
             '[]<>': aut.bdds_from('active=1','active=2')})
    aut.qinit = r'\E \A'
    aut.moore = True
    aut.plus_one = True
    return aut


def specify_component_bar():
    """Return temporal logic spec of component bar."""
    aut = trl.Automaton()
    aut.players = ['foo', 'bar', 'scheduler']
    aut.declare_variables(active=(1, 2), home = (0,1),known_room=(0, 2), pos=(0, 2), known=(0,1), turn=(0, 1))
    aut.varlist['scheduler'] = ['turn']
    aut.varlist['foo'] = ['active']
    aut.varlist['bar'] = ['known_room','known','pos','home']
    spec = r'''
    FooInit == active = 1 /\ turn = 1
    BarInit ==
    /\ pos = 0
    /\ home = 1
    /\ known_room = 1
    /\ known = 1

    INV ==
    /\ pos \in 0..2
    /\ known_room \in 0..2
    /\ home \in 0..1
    /\ known \in 0..1

    BarUNCHANGED ==
    /\ home' = home
    /\ pos' = pos
    /\ known' = known
    /\ known_room' = known_room

    BarAction ==
        /\ INV
        /\ (home = 1 => home' = 0)
        /\ (home = 1 <=> pos = 0)
        /\ (~(home = 0 /\ known' = 1) \/ home' = 1)

        /\ (~(home = 0 /\ pos = 1 /\ active = 1) \/ (known' = 1 /\ known_room' = 1))
        /\ (~(home = 0 /\ pos = 2 /\ active = 2) \/ (known' = 1 /\ known_room' = 2))

        /\ (~(home = 1 /\ known = 1 /\ known_room = 1) \/ (known' = 1 /\ known_room' = 1 /\ pos' = 1))
        /\ (~(home = 1 /\ known = 1 /\ known_room = 2) \/ (known' = 1 /\ known_room' = 2 /\ pos' = 2))

        /\ (~(home = 0 /\ (pos = 2 /\ active != 2)) \/ (known' = 0 /\ known_room' = 0 /\ pos' = 1))
        /\ (~(home = 0 /\ (pos = 1 /\ active != 1)) \/ (known' = 0 /\ known_room' = 0 /\ pos' = 2))

    FooNext ==
        \/  /\ (turn = 0 /\ active \in 1..2 /\ active' \in 1..2)
            /\ (active' = active \/ active' != active) 
        \/  /\ ((turn = 1) /\ (active' = active))
            /\ (turn' = 0)
    BarNext ==
        \/ ((turn = 0) /\ (BarUNCHANGED))
        \/ ((turn = 1) /\ (BarAction))
    '''
    aut.define(spec)
    aut.init.update(
        foo='FooInit',
        bar='BarInit')
    aut.action.update(
        foo='FooNext',
        bar='BarNext')
    aut.win = dict(
        bar={'<>[]': aut.bdds_from('turn = 0', 'turn = 1'),
             '[]<>': aut.bdds_from('TRUE')})
    aut.qinit = r'\E \A'
    aut.moore = True
    aut.plus_one = True
    return aut


def synthesize_some_controller(env, sys, aut):
    """Return a controller that implements the spec.

    If no controller exists, then raise an `Exception`.
    The returned controller is represented as a `networkx` graph.
    """
    aut.prime_varlists()
    # vars
    aut.varlist['env'] = aut.varlist[env] + aut.varlist['scheduler']
    aut.varlist['sys'] = aut.varlist[sys]
    # init
    aut.init['env'] = aut.init[env]
    aut.init['sys'] = aut.init[sys]
    # actions
    aut.action['env'] = aut.action[env]
    aut.action['sys'] = aut.action[sys]
    # win
    aut.win['[]<>'] = aut.win[sys]['[]<>']
    aut.win['<>[]'] = aut.win[sys]['<>[]']
    z, yij, xijk = gr1.solve_streett_game(aut)
    gr1.make_streett_transducer(z, yij, xijk, aut)
    aut.varlist[sys].append('_goal')
    aut.prime_varlists()


def plot_machines(asm):
    """Plot machine behaviors over a finite number of steps."""
    nrows = len(asm.machines)
    history = asm.past + [asm.state]
    n_steps = len(history)  # missing last state
    t = range(n_steps)
    plt.subplots(nrows=nrows, ncols=1)
    styles = ['b-o', 'r--', 'k-', 'g-*']  # def style picker
    for i, (name, stm) in enumerate(asm.machines.items()):
        plt.subplot(nrows, 1, i + 1)
        plt.title(name)
        styles_cp = list(styles)
        # TODO: could instead plot only sys vars and memory
        for var in stm.vars:
            if stx.isprimed(var):
                continue
            x = [steps.omit_prefix(state, name)[var]
                 for state in history]
            style = styles_cp.pop()
            plt.plot(t, x, style, label=var)
        plt.legend()
        plt.grid()


if __name__ == '__main__':
    main()
