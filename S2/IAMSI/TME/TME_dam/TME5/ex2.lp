#const n = 8.
row(1..n).
col(1..n).

n {queen(I,J) : row(I), col(J)} n.
queen(1, 1).


% Their is no head on this line, so we remove those who respect the body.
% We remove queen who are on the same I that an other queen.
:- queen(I, J1), queen(I, J2), J1 != J2.

% Only one queen by row
:- queen(I1, J), queen(I2, J), I1 != I2.
:- queen(I, J), queen(II, JJ), (I,J) != (II, JJ), I + J == II + JJ.
:- queen(I, J), queen(II, JJ), (I,J) != (II, JJ), I - J == II - JJ.


#show queen/2.