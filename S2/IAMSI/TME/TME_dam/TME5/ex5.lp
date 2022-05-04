num(1..5).

color(rouge; blanc; jaune; bleu; vert).
origin(brit; suede; dane; norve; allemand).
drink(the; lait; cafe; bierre; eau).
pet(chien; oiseau; chat; poisson; cheval).
smoke(pallmall; dunhill; bluemaster; princess; blend).

5 { house_color(N, X) : num(N), color(X) } 5.
:- house_color(N1, X), house_color(N2, X), N1!=N2.
:- house_color(N, X1), house_color(N, X2), X1!=X2.

5 { house_origin(N, X) : num(N), origin(X) } 5.
:- house_origin(N1, X), house_origin(N2, X), N1!=N2.
:- house_origin(N, X1), house_origin(N, X2), X1!=X2.

5 { house_drink(N, X) : num(N), drink(X) } 5.
:- house_drink(N1, X), house_drink(N2, X), N1!=N2.
:- house_drink(N, X1), house_drink(N, X2), X1!=X2.

5 { house_pet(N, X) : num(N), pet(X) } 5.
:- house_pet(N1, X), house_pet(N2, X), N1!=N2.
:- house_pet(N, X1), house_pet(N, X2), X1!=X2.

5 { house_smoke(N, X) : num(N), smoke(X) } 5.
:- house_smoke(N1, X), house_smoke(N2, X), N1!=N2.
:- house_smoke(N, X1), house_smoke(N, X2), X1!=X2.

% Le Britannique vit dans la maison rouge.
:- house_color(N, rouge), house_origin(N, O), O != brit.

% Le Suedois garde un chien.
:- house_pet(N, chien), house_origin(N, O), O != suede.

% Le Danois boit du the.
:- house_drink(N, the), house_origin(N, O), O != dane.

% La maison verte est a gauche de la maison blanche (on va assumer que celle a gauche a le nombre plus petit)
:- house_color(N1, vert), house_color(N2, blanc), N1 != N2-1.

% Le proprietaire de la maison verte boit du cafe.
:- house_color(N, vert), house_drink(N, D), D != cafe.

% La personne qui fume des Pall Mall possede des oiseaux.
:- house_smoke(N, pallmall), house_pet(N, P), P != oiseau.

% Le proprietaire de la maison jaune fume des Dunhill.
:- house_color(N, jaune), house_smoke(N, S), S != dunhill.

% La personne qui vit dans la maison qui se trouve exactement au centre boit du lait.
:- house_drink(N, lait), N != 3.

% Le Norvegien vit dans la premiere maison.
:- house_origin(N, norve), N != 1.

% La personne qui fume des Blend vit a cote de celle qui possede des chats.
:- house_smoke(N1, blend), house_pet(N2, chat), |N1-N2| != 1.

% La personne qui possede des chevaux vit a cote du fumeur de Dunhill.
:- house_pet(N1, cheval), house_smoke(N2, dunhill), |N1-N2| != 1.

% La personne qui fume des Bluemaster boit de la bierre.
:- house_smoke(N, bluemaster), house_drink(N, D), D != bierre.

% L’Allemand fume des Princess.
:- house_origin(N, allemand), house_smoke(N, S), S != princess.

% Le Norvegien vit a cote de la maison bleue.
:- house_origin(N1, norve), house_color(N2, bleu), |N1-N2| != 1.

% La personne qui fume des Blend a un voisin qui boit de l’eau.
:- house_smoke(N1, blend), house_drink(N2, eau), |N1-N2| != 1.

#show house_color/2.
#show house_origin/2.
#show house_drink/2.
#show house_pet/2.
#show house_smoke/2.