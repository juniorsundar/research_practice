-------------------- MODULE Invariant --------------------
Invariant ==
     /\ _i \in 1 .. 3
     /\ active \in 1 .. 2
     /\ goTo1 \in 0 .. 2
     /\ goTo2 \in 0 .. 2
     /\ pos1 \in -1 .. 2
     /\ pos2 \in -1 .. 2
     /\ rX1 \in 0 .. 4
     /\ rX2 \in 0 .. 4
     /\ rY1 \in 0 .. 4
     /\ rY2 \in 0 .. 4
     /\  \/ (pos1 = 0) /\ (pos2 = 0) /\ (rX1 = 0) /\ (rX2 = 0) /\ (rY1 = 0) /\ (rY2 = 0)
         \/ (pos1 = 0) /\ (pos2 = 1) /\ (rX1 = 0) /\ (rX2 = 4) /\ (rY1 = 0) /\ (rY2 = 0)
         \/ (pos1 = 0) /\ (pos2 = 2) /\ (rX1 = 0) /\ (rX2 = 0) /\ (rY1 = 0) /\ (rY2 = 4)
         \/ (pos1 = 0) /\ (pos2 = -1) /\ (rX1 = 0) /\ (rX2 \in 1 .. 3) /\ (rY1 = 0)
         \/ (pos1 = 0) /\ (pos2 = -1) /\ (rX1 = 0) /\ (rX2 \in 1 .. 4) /\ (rY1 = 0) /\ (rY2 \in 1 .. 4)
         \/ (pos1 = 0) /\ (pos2 = -1) /\ (rX1 = 0) /\ (rY1 = 0) /\ (rY2 \in 1 .. 3)
         \/ (pos1 = 1) /\ (pos2 = 0) /\ (rX1 = 4) /\ (rX2 = 0) /\ (rY1 = 0) /\ (rY2 = 0)
         \/ (pos1 = 1) /\ (pos2 = 1) /\ (rX1 = 4) /\ (rX2 = 4) /\ (rY1 = 0) /\ (rY2 = 0)
         \/ (pos1 = 1) /\ (pos2 = 2) /\ (rX1 = 4) /\ (rX2 = 0) /\ (rY1 = 0) /\ (rY2 = 4)
         \/ (pos1 = 1) /\ (pos2 = -1) /\ (rX1 = 4) /\ (rX2 \in 1 .. 3) /\ (rY1 = 0)
         \/ (pos1 = 1) /\ (pos2 = -1) /\ (rX1 = 4) /\ (rX2 \in 1 .. 4) /\ (rY1 = 0) /\ (rY2 \in 1 .. 4)
         \/ (pos1 = 1) /\ (pos2 = -1) /\ (rX1 = 4) /\ (rY1 = 0) /\ (rY2 \in 1 .. 3)
         \/ (pos1 = 2) /\ (pos2 = 0) /\ (rX1 = 0) /\ (rX2 = 0) /\ (rY1 = 4) /\ (rY2 = 0)
         \/ (pos1 = 2) /\ (pos2 = 1) /\ (rX1 = 0) /\ (rX2 = 4) /\ (rY1 = 4) /\ (rY2 = 0)
         \/ (pos1 = 2) /\ (pos2 = 2) /\ (rX1 = 0) /\ (rX2 = 0) /\ (rY1 = 4) /\ (rY2 = 4)
         \/ (pos1 = 2) /\ (pos2 = -1) /\ (rX1 = 0) /\ (rX2 \in 1 .. 3) /\ (rY1 = 4)
         \/ (pos1 = 2) /\ (pos2 = -1) /\ (rX1 = 0) /\ (rX2 \in 1 .. 4) /\ (rY1 = 4) /\ (rY2 \in 1 .. 4)
         \/ (pos1 = 2) /\ (pos2 = -1) /\ (rX1 = 0) /\ (rY1 = 4) /\ (rY2 \in 1 .. 3)
         \/ (pos1 = -1) /\ (pos2 = 0) /\ (rX1 \in 1 .. 3) /\ (rX2 = 0) /\ (rY2 = 0)
         \/ (pos1 = -1) /\ (pos2 = 0) /\ (rX1 \in 1 .. 4) /\ (rX2 = 0) /\ (rY1 \in 1 .. 4) /\ (rY2 = 0)
         \/ (pos1 = -1) /\ (pos2 = 0) /\ (rX2 = 0) /\ (rY1 \in 1 .. 3) /\ (rY2 = 0)
         \/ (pos1 = -1) /\ (pos2 = 1) /\ (rX1 \in 1 .. 3) /\ (rX2 = 4) /\ (rY2 = 0)
         \/ (pos1 = -1) /\ (pos2 = 1) /\ (rX1 \in 1 .. 4) /\ (rX2 = 4) /\ (rY1 \in 1 .. 4) /\ (rY2 = 0)
         \/ (pos1 = -1) /\ (pos2 = 1) /\ (rX2 = 4) /\ (rY1 \in 1 .. 3) /\ (rY2 = 0)
         \/ (pos1 = -1) /\ (pos2 = 2) /\ (rX1 \in 1 .. 3) /\ (rX2 = 0) /\ (rY2 = 4)
         \/ (pos1 = -1) /\ (pos2 = 2) /\ (rX1 \in 1 .. 4) /\ (rX2 = 0) /\ (rY1 \in 1 .. 4) /\ (rY2 = 4)
         \/ (pos1 = -1) /\ (pos2 = 2) /\ (rX2 = 0) /\ (rY1 \in 1 .. 3) /\ (rY2 = 4)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rX1 \in 1 .. 3) /\ (rX2 \in 1 .. 3)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rX1 \in 1 .. 3) /\ (rX2 \in 1 .. 4) /\ (rY2 \in 1 .. 4)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rX1 \in 1 .. 3) /\ (rY2 \in 1 .. 3)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rX1 \in 1 .. 4) /\ (rX2 \in 1 .. 3) /\ (rY1 \in 1 .. 4)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rX1 \in 1 .. 4) /\ (rX2 \in 1 .. 4) /\ (rY1 \in 1 .. 4) /\ (rY2 \in 1 .. 4)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rX1 \in 1 .. 4) /\ (rY1 \in 1 .. 4) /\ (rY2 \in 1 .. 3)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rX2 \in 1 .. 3) /\ (rY1 \in 1 .. 3)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rX2 \in 1 .. 4) /\ (rY1 \in 1 .. 3) /\ (rY2 \in 1 .. 4)
         \/ (pos1 = -1) /\ (pos2 = -1) /\ (rY1 \in 1 .. 3) /\ (rY2 \in 1 .. 3)
     /\ care expression
=======================================================
