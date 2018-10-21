fotocamera(centro).

% qrcode 0 per false 1 per true
qrcode(0).

% mettere prima il destro cosi se sono 3 sonar uguali il sistema prenderà il primo e quindi va avanti
sonar(centro, 56).
sonar(destra, 14).
sonar(sinistra, 14).

% lidar ogni 10 gradi
lidar(0,1).
lidar(10,2).
lidar(20,3).
lidar(30,4).
lidar(40,5).
lidar(50,6).
lidar(60,7).
lidar(70,8).
lidar(80,9).
lidar(90,10).
lidar(100,11).
lidar(110,11).
lidar(120,43).
lidar(130,14).
lidar(140,15).
lidar(150,16).
lidar(160,17).
lidar(170,18).
lidar(180,19).

switch(sinistra,0).
switch(centro,0).
switch(destra,0).

volt(13).

angle8(10).
oldangle8(30).

% se il comando vecchio è indietro il sistema fa stop e attiva il lidar
commandolder(avanti).

% comandi disponibili
command(sinistra,1).
command(destra, 2).
command(avanti,3).
command(indietro,4).
command(stop,5).
command(fine,6).
command(batteria, 7).
command(correggi_a_destra, 8).
command( correggi_a_sinistra, 9).
command(attiva_lidar, 10).

% regola per il lidar ritorna l'angolo con la distanza maggiore
lidar(X):- lidar(0,A),lidar(10,B),lidar(20,C),lidar(30,D),lidar(40,E),lidar(50,F),lidar(60,G),lidar(70,H),lidar(80,I),lidar(90,L),lidar(100,M),lidar(110,N),lidar(120,O),lidar(130,P),lidar(140,Q),lidar(150,R),lidar(160,S),lidar(170,T),lidar(180,U), V is max(A,B), V1 is max(V,C),V2 is max(V1,D),V3 is max(V2,E),V4 is max(V3,F),V5 is max(V4,G), V6 is max(V5,H), V7 is max(V6,I), V8 is max(V7,L), V9 is max(V8,M), V10 is max(V9,N), V11 is max(V10,O), V12 is max(V11,P), V13  is max(V12,Q), V14 is max(V13,R), V15 is max(V14,S), V16 is max(V15,T), V17 is max(V16,U), lidar(X,V17),!.

% regola per gli switch false se sbatte true se non sbatte
switch(_):- switch(sinistra,X), switch(centro,Y), switch(destra, Z), X == 0, Y == 0, Z == 0, !.


% regola per i sonar, serve per far cambiare la direzione predefinita dritto a una certa distanza da un possibile ostacolo
sonartru(_):- sonar(destra, A), sonar(centro, B), sonar(sinistra, C),  A > 10, B > 10, C > 10, !.

% regola per capire quale è il sonar con la distanza maggiore
sonar(Y) :- sonar(centro, A), sonar(destra, B), sonar(sinistra, C), D is max(A, B), X is max(D, C), sonar(Y, X),!.

%commando batteria
command(X):- volt(Y), Y < 11, C is 7, command(X, C),!.

% comando fine
command(X):- qrcode(1), C is 6, command(X,C),!.

% comando attiva lidar
command(X):- commandolder(O), O \== indietro, switch(_,1), volt(Y), Y > 11, qrcode(Q), Q == 0, C is 10, command(X,C),!.

% comando coregi a destra
command(X):-commandolder(O), O == avanti, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonartru(_), angle8(A), oldangle8(B), S is A-B, S > 10, C is 8, command(X, C),!. 

%comando coregi a sinistra
command(X):-commandolder(O), O == avanti, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonartru(_), angle8(A), oldangle8(B), S is B-A, S > 10, C is 9, command(X, C),!. 

% comando indietro
command(X):- commandolder(O), O \== indietro, \+ sonartru(_), volt(Y), Y > 11, qrcode(Q), Q == 0, C is 4, command(X,C),!.

% comando avanti
command(X):- commandolder(O), O == avanti, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonartru(_), C is 3, command(X,C),!.
command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == centro, fotocamera(F), F == centro, C is 3, command(X,C),!. 
command(X):- commandolder(O), O \== indietro,switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == centro, C is 3, command(X,C),!.

% comando sinistra
command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == sinistra, fotocamera(F), F == sinistra, C is 1, command(X,C),!.
command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == sinistra, C is 1, command(X,C),!.

%  comando destra
command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == destra, fotocamera(F), F == destra, C is 2, command(X,C),!.
command(X):- commandolder(O), O \== indietro, switch(_), volt(Y), Y > 11, qrcode(Q), Q == 0, sonar(U), U == destra, C is 2, command(X,C),!.

% comando stop (errore)
command(X):- C is 5, command(X,C),!.

% comando avanti
commandlidar(X):-lidar(B), B < 121, B > 61, switch(_), volt(Y), Y > 11,qrcode(Q), Q == 0, C is 3, command(X,C),!.

% comando sinistra
commandlidar(X):-lidar(B), B > 120,switch(_), volt(Y), Y > 11,qrcode(Q), Q == 0, C is 1, command(X,C),!.

%  comando destra
commandlidar(X):-lidar(B), B < 60,switch(_), volt(Y), Y > 11,qrcode(Q), Q == 0, C is 2, command(X,C),!.