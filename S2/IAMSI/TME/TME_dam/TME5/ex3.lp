col(0..8).
row(0..8).
val(1..9).

1 {cell(R, C, V) : val(V) } 1 :- row(R), col(C).

% Contraintes
:- cell(R, C1, V), cell(R, C2, V), C1 != C2.
:- cell(R1, C, V), cell(R2, C, V), R1 != R2.

subgrid(R1, C1, R2, C2) :- col(C1), col(C2), row(R1), row(R2),  (C1 / 3) == (C2 / 3), (R1 / 3) == (R2 / 3).
:- cell(R1, C1, V), cell(R2, C2, V), subgrid(R1, C1, R2, C2), C1 != C2, R1 != R2.

% Grille
cell(0, 1, 7).
cell(0, 3, 6).
cell(0, 5, 3).
cell(0, 7, 1).
cell(0, 8, 4).

cell(1, 0, 8).
cell(1, 4, 9).

cell(2, 1, 6).
cell(2, 2, 3).
cell(2, 3, 2).
cell(2, 4, 1).
cell(2, 6, 8).

cell(3, 4, 3).
cell(3, 7, 5).
cell(3, 8, 9).

cell(4, 0, 6).
cell(4, 3, 9).
cell(4, 6, 4).
cell(4, 8, 1).

cell(5, 0, 9).
cell(5, 1, 2).
cell(5, 3, 4).
cell(5, 5, 1).
cell(5, 8, 8).

cell(6, 1, 5).
cell(6, 3, 8).
cell(6, 8, 3).

cell(7, 0, 4).
cell(7, 2, 1).
cell(7, 3, 3).
cell(7, 4, 6).
cell(7, 5, 2).
cell(7, 6, 7).
cell(7, 7, 8).

cell(8, 0, 3).
cell(8, 2, 6).
cell(8, 3, 1).
cell(8, 6, 9).
cell(8, 8, 2).

#show cell/3.