# AI-chess-experiment
An experiment in chess AI using Monte-Carlo simulation method.<br/>
Requires Python 3.3+<br/>
How to run:
```
  cd chess
  python parallel-runner.py
```
At the end of the simulation, the result will be printed out on the console (board|bestAction):<br/>
112411131|322<br/>
112111314|210<br/>
114111132|310<br/>
412111311|221<br/>
114111312|300<br/>
..and so on..

Board representation:<br/>
1 = empty square<br/>
2 = white KING<br/>
3 = white ROOK<br/>
4 = black KING<br/>

112411131 is a 3x3 board:<br/>
1 1 2<br/>
4 1 1<br/>
1 3 1<br/>

Action 322 means: move white ROOK to coordinate (2, 2) (Coordinate system: top left = (0, 0), bottom right = (2, 2))</br>

