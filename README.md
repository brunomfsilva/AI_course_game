# ![](icons/king_white.png) DAMEO GAME ![](icons/king_black.png)

Requirements:
pygame 2.5.2


To run the game:
Run dameo.py file

or in bash:
python3 dameo.py

Testes:
Testes em 5x5 (várias eval functionas, várias depths, minimax e MC):
 - Minimax, 5x5, depth 5 ou mais, 3 evaluation function, umas contra as outras (5 jogos cada - 15 jogos)
 - Minimax, 5x5, depth 2/3, 3 evaluation function, umas contra as outras (5 jogos cada - 15 jogos)

Montecarlo, 5x5, 100 vs 500, 100 vs 1000, 500 vs 1000 (3 jogos cada - 9 jogos).
Montecarlo, 1000 vs 1000, 5x5 e 8x8 - comparar tempos de diferent sizes.

Montecarlo vs Minimax (3 jogos cada combinação - 27 jogos?)
[100, 1000, 5000] [2, 5, 7]