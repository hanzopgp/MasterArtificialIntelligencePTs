/*domains*/
drop all objects

create domain dcles  as numeric(5);
create domain dnoms  as varchar(20);
create domain dprix  as numeric(7,2);
create domain dnum  as numeric(2);
create domain dloc  as VARCHAR(100) ;
create domain dperc  as numeric(2,2);

--create domain dloc  as VARCHAR(100) CHECK (REGEXP_LIKE(VALUE, '[A-Z ]*,[A-Z ]*,[A-Z ]*'));


/* source 1
Produit(numP, nomP, prixP, délaiLiv, stock) 
Fournisseur(numF, nomF, localisation, remise) nomF est unique
Localisation de la forme (ville, province, pays) 
Achat(noAchat, dateAchat, moyenPaiment,  numF#) 
AchatUnit(noAchat#, numP#, qte, prixUnit) 
*/

DROP TABLE Produit IF EXISTS ;
DROP TABLE Fournisseur IF EXISTS;
DROP TABLE Achat IF EXISTS ;
DROP TABLE AchatUnit IF EXISTS ;



CREATE TABLE Produit (
    numP dcles PRIMARY KEY,
    nomP dnoms, 
    prixP dprix, 
    délaiLiv dnum, 
    stock dnum
);

CREATE TABLE Fournisseur(
    numF dcles PRIMARY KEY, 
    nomF dnoms UNIQUE, 
    ville dloc, 
    province dloc, 
    pays dloc, 
    remise dperc
);

CREATE TABLE Achat(
    noAchat dcles PRIMARY KEY, 
    dateAchat date, 
    moyenPaiment dnoms,  
    numF dcles REFERENCES Fournisseur
);

CREATE TABLE AchatUnit(
    noAchat dcles REFERENCES Achat, 
    numP dcles REFERENCES Produit, 
    qte dnum, 
    prixUnit dprix,
    PRIMARY KEY (noAchat,numP)
);

/*Insertions*/
INSERT INTO Produit (numP, nomP, prixP, délaiLiv, stock)  values
    (36566, 'Monitor','169.00', 12, 10),
    (36577, 'Laser Printer','699.00', 12, 15),
    (14590, 'Printer Cable','12.00', 12, 20),
    (12138, 'Ink Jet Printer','99.00', 12, 2),
    (45671, 'Ink Jet Cartridge','38.00', 12, 5),
    (55443, 'Color Scanner','199.99', 12, 3),
    (95676, 'Back-up System','89.00', 12, 7)
    ;

select * from produit

INSERT INTO  Fournisseur(numF, nomF, ville, province, pays, remise) values 
    (29929, 'ColorMeg', 'paris','idf','france',0.10),
    (99214, 'Connex', 'sevres','idf','france',0.12),
    (90202, 'Ethlite', 'lyon','raa','france',0.08),
    (20948, 'UV Components', 'brussels','bc','belgium',0.00),
    (95332, 'Cybercx', 'passau','bv','germany',0.00)
    ;

select * from Fournisseur


INSERT INTO  Achat(noAchat, dateAchat, moyenPaiment,  numF) values 
    (24040, '2021-02-03', 'card', 29929),
    (45877, '2021-03-03', 'cash', 99214),
    (49952, '2021-04-12', 'cash', 29929),
    (54432, '2021-04-20', 'card', 90202),
    (55443, '2021-05-02', 'cash', 95332)
;
select * from Achat



INSERT INTO  AchatUnit(noAchat, numP, qte, prixUnit) VALUES 
    (24040, 36566, 10, 150.00),
    (24040, 36577, 11, 650.00),
    (49952, 12138, 10, 89.00),
    (49952, 36577, 15, 700.00),
    (49952, 55443, 25, 180.00),
    (49952, 95676, 40, 76.00),
    (54432, 12138, 15, 35.00),
    (55443, 36577, 10, 750.00)
;

select * from AchatUnit
   

/*source 2
ProdAchats(codeProd, dateAchat, descProd, catProd, nomFour, qte, dispo, prixUnit, montant) 
*/
DROP TABLE ProdAchats IF EXISTS;
CREATE TABLE ProdAchats(
    codeProd dcles, 
    dateAchat date, 
    descProd dnoms, 
    catProd dnoms,
    nomFour dnoms, 
    qte dnum, 
    dispo dnum, 
    prixUnit dprix, 
    montant dprix
    ); 

INSERT INTO ProdAchats(codeProd, dateAchat, descProd, catProd, nomFour, qte, dispo, prixUnit, montant) values 
    (55671, '2021-02-03', 'MF Printer', 'printer', 'Printers&co', 1, 20, 200.00, 200.0),
    (85690, '2021-05-02', 'Wireless Router', 'network', 'IT expert', 2, 10, 150.00, 300.0),
    (46597, '2021-04-30', 'Kindle', 'other', 'IT expert', 4, 12, 110.00, 440.0)
    ;
    
select * from ProdAchats
