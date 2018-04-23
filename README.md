# AI-chess-experiment
An experiment in chess AI using Monte-Carlo simulation method.<br/>
Required Python 3.3+<br/>
How to run:
```
  cd chess
  python parallel-runner.py
```
After the simulation, output files will be generated with the following name:<br/>
chess-parallel-0<br/>
chess-parallel-1<br/>
...<br/>
chess-parallel-9<br/>

The format of output entries is:<br/>
board|action|result

Sample output:<br/>
311214111|202|1<br/>
311111214|320|1<br/>
231111114|320|0<br/>
213111141|322|0<br/>
211111413|320|0<br/>

Result = 1: outcome is a win<br/>
Result = 0: outcome is a loss or draw<br/>
