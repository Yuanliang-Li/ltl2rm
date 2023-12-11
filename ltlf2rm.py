import spot
import buddy
import sys
import itertools

def ltlf_to_dfa(ltlf_formula):
    # modified from https://spot.lrde.epita.fr/tut12.html
    aut = spot.from_ltlf(ltlf_formula).translate('ba')
    # Remove "alive" atomic proposition
    rem = spot.remove_ap()
    rem.add_ap('alive')
    aut = rem.strip(aut)
    # Simplify result and print it. Use postprocess('ba', 'det')
    # if you always want a deterministic automaton.
    aut = spot.postprocess(aut, 'ba', 'det')
    # print(aut.to_str('hoa'))
    return aut

def terf_product(automata, rewards):
    # based on the automata product from https://spot.lrde.epita.fr/ipynb/product.html
    bdict = automata[0].get_dict()
    for automaton in automata:
        if automaton.get_dict() != bdict:
            raise RuntimeError("automata should share their dictionary")
        
    result = spot.make_twa_graph(bdict)
    # Copy the atomic propositions of the two input automata
    for automaton in automata:
        result.copy_ap_of(automaton)
    
    sdict = {}
    todo = []
    def dst(state_numbers):
        state_numbers_tuple = tuple(state_numbers)
        p = sdict.get(state_numbers_tuple)
        if p is None:
            p = result.new_state()
            sdict[state_numbers_tuple] = p
            todo.append((state_numbers_tuple, p))
        return p
    
    result.set_init_state(dst( [automata[k].get_init_state_number() for k in range(len(automata)) ]  ))
    
    while todo:
        tuple_rc, osrc = todo.pop()
        # cartesian product of automata[i].out(tuple_rc[i])
        lists_of_transitions = [ automata[i].out(tuple_rc[i]) for i in range(len(automata))  ]
        for element in itertools.product(*lists_of_transitions):
            cond = element[0].cond
            for j in range(1,len(element)):
                cond = cond & element[j].cond
            
            if cond != buddy.bddfalse:
                reward = sum( [rewards[k] for k in range(len(element)) if element[k].acc ])
                acc = spot.mark_t([reward])
                dest_numbers = [ element[k].dst for k in range(len(element)) ]
                result.new_edge(osrc, dst(dest_numbers), cond, acc)
    return result


class TERF_Parser():
    def __init__(self):
        self.ltlf_formulas = []
        self.rewards = []
    def parse_terf(self,terf):
        with open(terf,"r") as f:
            n_formulas = int(f.readline())
            for n in range(n_formulas):
                self.ltlf_formulas.append( f.readline().strip() )
                self.rewards.append( int(f.readline()) )

def usage():
    return "Usage: python3 ltlf2rm.py <terf> <output_tlsf>"

if len(sys.argv) != 3:
    print(usage())


# STEP 1: parse TERF
import sys
import pprint

output_file_hoa = './out/rm' # output file in HOA format

# STEP 1: Input LTL formulas and rewards
ltl_list = ['F (a & F (b & F c))', 'F (f & g)'] # input all your LTL formulas in the list
reward_list = [1, 3]  # input the reward value for each LTL formula


# STEP 2: Transform LTLf formulae into DFA
automata = [ltlf_to_dfa(ltlf_formula) for ltlf_formula in ltl_list]

# STEP 3: Do the cross product automaton
product_dfa = terf_product(automata, reward_list)

# STEP 5: Dump HOA to output file
with open(output_file_hoa,"w") as f:
    f.write( product_dfa.to_str('hoa','t') ) # transition-based output
