-------------------- MODULE Invariant --------------------
Invariant ==
     /\ _i \in 1 .. 3
     /\ goTo1 \in 0 .. 2
     /\ goTo2 \in 0 .. 2
     /\ pos1 \in -1 .. 2
     /\ pos2 \in -1 .. 2
     /\ room1 \in 1 .. 2
     /\ room2 \in 1 .. 2
     /\  \/ (room1 = 1) /\ (room2 = 2)
         \/ (room1 = 2) /\ (room2 = 1)
     /\ care expression
=======================================================
