col(0..8).
row(0..8).
val(1..9).

1 {case(X, Y, V) : val(V) } 1 :- row(X), col(Y).


% Grille
case(0, 1, 7).
case(0, 3, 6).
case(0, 5, 3).
case(0, 7, 1).
case(0, 8, 4).

case(1, 0, 8).
case(1, 4, 9).

case(2, 1, 6).
case(2, 2, 3).
case(2, 3, 2).
case(2, 4, 1).
case(2, 6, 8).

case(3, 4, 3).
case(3, 7, 5).
case(3, 8, 9).

case(4, 0, 6).
case(4, 3, 9).
case(4, 6, 4).
case(4, 8, 1).

case(5, 0, 9).
case(5, 1, 2).
case(5, 3, 4).
case(5, 5, 1).
case(5, 8, 8).

case(6, 1, 5).
case(6, 3, 8).
case(6, 8, 3).

case(7, 0, 4).
case(7, 2, 1).
case(7, 3, 3).
case(7, 4, 6).
case(7, 5, 2).
case(7, 6, 7).
case(7, 7, 8).

% Contraintes
:- case(I, J1, V), case(I, J2, V), J1 != J2.
:- case(I1, J, V), case(I2, J, V), I1 != I2.

subgrid(X1, Y1, X2, Y2) :- col(X1), col(X2), row(Y1), row(Y2),  (X1 / 3) == (X2 / 3), (Y1 / 3) == (Y2 / 3).
:- case(X1, Y1, V), case(X2, Y2, V), subgrid(X1, Y1, X2, Y2), X1 != X2, Y1 != Y2.

% La difficultes d'une grille est evaluee par le nombre de solution possible, et parmis celle-la, les plus difficiles sont celles qui
% ont le peu de nombre dans la grille initial, c'est a dire peu de contraintes.

#show case/3.