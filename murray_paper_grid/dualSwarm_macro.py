"""Run contract construction and communication arch design."""
import logging

from dd import cudd

import contracts_pinfo as pinfo
import utils

TURN = utils.TURN

def swarm():
    aut = pinfo.Automaton()
    aut.players = dict(environment=1, rob1=2, rob2=3, scheduler=None)
    vrs = dict(
        active = (1,2),
        pos1 = (-1,2),
        rX1 = (0,4),
        rY1 = (0,4),
        goTo1 = (0,2),
        pos2 = (-1,2),
        rX2 = (0,4),
        rY2 = (0,4),
        goTo2 = (0,2)
    )
    vrs[TURN] = (1,3)
    aut.declare_variables(**vrs)
    aut.varlist = dict(
        environment = ['active'],
        rob1 = ['pos1', 'goTo1','rX1','rY1'],
        rob2 = ['pos2', 'goTo2','rX2','rY2'],
        scheduler=[TURN]
    )

    specs = r'''
    env_init == 
    /\ active = 1
    
    env_unchanged ==
    /\ (active' = active)

    env_step ==
    /\ active \in 1..2
    /\ active' \in 1..2

    rob1_unchanged ==
    /\ pos1' = pos1
    /\ goTo1' = goTo1
    /\ rX1' = rX1
    /\ rY1' = rY1

    rob1_init ==
    /\ pos1 = 0
    /\ goTo1 = 1
    /\ rX1 = 0 /\ rY1 = 0

    room11 ==
    /\ rX1 = 4 /\ rY1 = 0

    room21 ==
    /\ rX1 = 0 /\ rY1 = 4

    home1 ==
    /\ rX1 = 0 /\ rY1 = 0

    rob1_step ==
    /\ pos1 \in -1..2 /\ pos1' \in -1..2
    /\ goTo1 \in 0..2 /\ goTo1' \in 0..2
    /\ (pos1 = 1 => room11)
    /\ (pos1 = 2 => room21)

    /\ (pos1 = -1 => (~home1 /\ ~room21 /\ ~room11 /\ pos1' = goTo1 /\ goTo1' = goTo1 /\ rX1 \in 0..4 /\ rY1 \in 0..4))
    /\ ((pos1 = 1 /\ active = 1) => (goTo1' = 0 /\ pos1' = -1))
    /\ ((pos1 = 2 /\ active = 2) => (goTo1' = 0 /\ pos1' = -1))
    /\ ((pos1 = 1 /\ active != 1) => (goTo1' = 2 /\ pos1' = -1))
    /\ ((pos1 = 2 /\ active != 2) => (goTo1' = 1 /\ pos1' = -1))
    /\ (pos1 = 0  => (home1 /\ goTo1' = 1 /\ pos1' = -1))

    rob2_init ==
    /\ pos2 = 1 
    /\ goTo2 = 1
    /\ rX2 = 0 /\ rY2 = 0

    rob2_unchanged ==
    /\ pos2' = pos2
    /\ goTo2' = goTo2
    /\ rX2' = rX2
    /\ rY2' = rY2

    room12 ==
    /\ rX2 = 4 /\ rY2 = 0

    room22 ==
    /\ rX2 = 0 /\ rY2 = 4

    home2 ==
    /\ rX2 = 0 /\ rY2 = 0

    rob2_step ==
    /\ pos2 \in -1..2 /\ pos2' \in -1..2
    /\ goTo2 \in 0..2 /\ goTo2' \in 0..2
    /\ (pos2 = 1 => room12)
    /\ (pos2 = 2 => room22)

    /\ (pos2 = -1 => (~home2 /\ ~room22 /\ ~room12 /\ pos2' = goTo2 /\ goTo2' = goTo2 /\ rX2 \in 0..4 /\ rY2 \in 0..4))
    /\ ((pos2 = 1 /\ active = 1) => (goTo2' = 0 /\ pos2' = -1))
    /\ ((pos2 = 2 /\ active = 2) => (goTo2' = 0 /\ pos2' = -1))
    /\ ((pos2 = 1 /\ active != 1) => (goTo2' = 2 /\ pos2' = -1))
    /\ ((pos2 = 2 /\ active != 2) => (goTo2' = 1 /\ pos2' = -1))
    /\ (pos2 = 0  => (home2 /\ goTo2' = 2 /\ pos2' = -1))

    env_next ==
    \/ {turn} = 1 /\ env_step
    \/ {turn} != 1 /\ env_unchanged

    rob1_next ==
    \/ {turn} = 2 /\ rob1_step
    \/ {turn} != 2 /\ rob1_unchanged

    rob2_next ==
    \/ {turn} = 3 /\ rob2_step
    \/ {turn} != 3 /\ rob2_unchanged

    scheduler_init == ({turn} = 1)

    scheduler_next ==
    /\ (({turn} = 1) => ({turn}' = 2))
    /\ (({turn} = 2) => ({turn}' = 3))
    /\ (({turn} = 3) => ({turn}' = 1))
    /\ ({turn} \in 1..3)
    '''.format(turn=TURN)
    aut.define(specs)

    aut.init_expr = dict(
        environment='env_init',
        rob1='rob1_init',
        rob2='rob2_init',
        scheduler='scheduler_init')
    aut.action_expr = dict(
        environment='env_next',
        rob1='rob1_next',
        rob2='rob2_next',
        scheduler='scheduler_next')
    aut.win_expr = dict(
        environment = {'[]<>': ['TRUE']},
        rob1 = {'[]<>': ['pos1 = 1','pos1 = 2']},
        rob2 = {'[]<>': ['pos2 = 1','pos2 = 2']},
        scheduler = {'[]<>': ['TRUE']}
    )
    aut.build()
    aut.assert_consistent()
    return aut

if __name__ == '__main__':
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s\t%(message)s')
    handler.setFormatter(formatter)
    # `dd` logger
    log = logging.getLogger('dd')
    log.setLevel(logging.ERROR)
    # `omega` logger
    logger = logging.getLogger('omega')
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)
    logger = logging.getLogger('omega.symbolic.cover')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    # `synthesizer` logger
    logger = logging.getLogger('synthesizer.contracts_pinfo')
    logger.setLevel(logging.INFO)
    # stream to stdout
    logger.addHandler(handler)
    aut = swarm()
    # aut = charging_station_example()
    pinfo.main(aut)