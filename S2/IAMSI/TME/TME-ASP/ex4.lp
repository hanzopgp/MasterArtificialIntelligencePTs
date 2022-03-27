#const n = 7.
#const m = 4.


nodeName(1..n).
colour(1..m).


1{nodeCoul(N,C):colour(C)}1:-nodeName(N).

% Contraintes
:- nodeCoul(N1, C), nodeCoul(N2, C), edges(N1,N2).



edges(A, B) :- edges(B, A).


#show nodeCoul/2.

