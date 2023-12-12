# LTL to Reward Machine

Translate LTL Formulas to a Reward Machine.

It is a modified version based on the repo: https://bitbucket.org/acamacho/fl2rm, where the code can not only output in HOA format but also in txt format and Python dict.

## Usage
1. Open **ltlf2rm.py** and configure your LTL formulas and rewards by:
```python
ltl_list = ['F (a & F (b & F c))', 'F (f & g)'] 
reward_list = [1, 2]  
```
Note: All LTL formulas are configured in the **ltl_list**. Each LTL formula has its reward saved in **reward_list**.

2. Run **ltlf2rm.py** by:
```python
python3 ltlf2rm.py
```

3. Get results from **./out**

Note: The code produces a reward machine in a HOA format, txt format, and a Python dict, respectively. 
The HOA is an automaton with states labeled with rewards.
The txt format is a format that can be directly used by https://github.com/RodrigoToroIcarte/reward_machines for reinforcement learning algorithms with reward machines.

## DEPENDENCIES
Spot: https://spot.lrde.epita.fr/
