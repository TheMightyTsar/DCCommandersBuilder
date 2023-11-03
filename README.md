# DCCommanders
![GameLogo]()

# Manual
* ## Que es el juego?:
  * Cada partida se enfrentan dos **Comandantes**, los cuales son **programados** por los _jugadores_. 
  * Los **Comandantes** deben dirigir las tropas de su tablero (10x10) y atacar el tablero rival y destruir todas sus tropas. 
  * Al inicio de un enfrentamiento los **Comandantes** deberan montar su tablero y despues por turnos, como en el ajedrez, se enfrentaran dandole ordenes a sus tropas.

  * Gana el **Comandante** que destruya todas las tropas enemigas

* ## Como funciona el juego?
  * Al iniciar un enfrentamiento los **Comandantes** deben posicionar sus tropas en su tablero. 
  * Un **Comandante** solo puede hacer una jugada cada turno, para tomar esa decision recibe un informe que contiene informacion de la jugada del rival y los resultados de su jugada anterior. 
  * En cada **jugada** el comandante puede escoger una tropa que realice una accion, atacar o moverse.
  * Tu **Comandante** debe destruir todas las tropas enemigas para ganar.

* ## El Tablero:
  * Tu tablero es de 10x10 unidades

| X  | A  | B  | C  | D  | E  | F  | G  | H  | I  | J  |
|--- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 0  | A0 | B0 | C0 | D0 | E0 | F0 | G0 | H0 | I0 | J0 |
| 1  | A1 | B1 | C1 | D1 | E1 | F1 | G1 | H1 | I1 | J1 |
| 2  | A2 | B2 | C2 | D2 | E2 | F2 | G2 | H2 | I2 | J2 |
| 3  | A3 | B3 | C3 | D3 | E3 | F3 | G3 | H3 | I3 | J3 |
| 4  | A4 | B4 | C4 | D4 | E4 | F4 | G4 | H4 | I4 | J4 |
| 5  | A5 | B5 | C5 | D5 | E5 | F5 | G5 | H5 | I5 | J5 |
| 6  | A6 | B6 | C6 | D6 | E6 | F6 | G6 | H6 | I6 | J6 |
| 7  | A7 | B7 | C7 | D7 | E7 | F7 | G7 | H7 | I7 | J7 |
| 8  | A8 | B8 | C8 | D8 | E8 | F8 | G8 | H8 | I8 | J8 |
| 9  | A9 | B9 | C9 | D9 | E9 | F9 | G9 | H9 | I9 | J9 |



## Las Tropas:
Las tropas son robots con mente propia! aunque el comandante decide la jugada las tropas pueden decidir donde atacar y moverse y contarle al comandante que haran para que el comandante mande la jugada.

baseTroop
Es el programa basico de los soldados.

**soldado (soldier.py)**

**Scout (scout.py)**

**Cañon Gauss (gauss.py)**

**Granadero (grenadier.py)**

**Torre AA (tower.py)**

## Que debo implementar?

