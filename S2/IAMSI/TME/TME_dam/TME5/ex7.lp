#const ne = 4.
#const ns = 3.
#const nj = 2 * ns.
#const n_match = ne * (ne-1).

equipe(1..ne).
jour(1..nj).
dimanche(J) :- jour(J), J\2 == 0.

n_match { match(J, E1, E2) : jour(J), equipe(E1), equipe(E2) } n_match.

% Un match entre 2 equipes differentes
:- match(J, E, E).

% Meme jour, 1 equipe ne peut jouer contre que 1 advesaire
:- match(J, E, E1), match(J, E, E2), E1 != E2.
:- match(J, E1, E), match(J, E2, E), E1 != E2.

% Meme jour, 1 equipe ne peut jouer que soit a domicile, soit a l'ext
:- match(J, E, E1), match(J, E2, E).

% Chaque equipe joue exactement 1 match a domicile et 1 match a l'ext contre chaque advesaire
:- match(J1, E1, E2), match(J2, E1, E2), J1 != J2.