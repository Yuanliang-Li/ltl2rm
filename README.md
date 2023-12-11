# LTL to Reward Machine

Translate LTL Formulas to a Reward Machine.

It is a modified version based on the repo: https://bitbucket.org/acamacho/fl2rm

## Usage
1. Open _ltlf2rm.py_ and configure your LTL formulas and rewards by:
```python
ltl_list = ['F (a & F (b & F c))', 'F (f & g)'] 
reward_list = [1, 2]  
```
Note: All LTL formulas are saved in the _ltl_list_. Each LTL formula has its reward saved in _reward_list_.

2. Run _ltlf2rm.py_ by:
```python
python3 ltlf2rm.py
```

3. Get the results from ./out

Note: The code produces a reward machine in a HOA format and a txt format, respectively. 
The HOA is an automaton with transitions labeled with rewards.
The txt format is a format that can be directly used by https://github.com/RodrigoToroIcarte/reward_machines for reinforcement learning algorithms with reward machines.

## DEPENDENCIES
Spot: https://spot.lrde.epita.fr/
