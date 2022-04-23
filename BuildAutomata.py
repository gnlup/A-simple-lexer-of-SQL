from Automata import Automata
from utility import *

# when regex input is a letter or digit, just construct a basic automata
def basicStructure(input):
    a=Automata()
    a.setBasicStructure(input)
    return a

# when regex input is '|', get the two automata "plus"
def orConcat(a,b):
    res = Automata()
    res = copyAutomata(a)
    # increase index of states of b
    maxIndexOfa = res.getMaxState()
    addNumOfb = maxIndexOfa + 1
    b.increaseStatesIndex(addNumOfb)
    # "plus" b to res
    res.addStates(b.states)
    res.addStartStates(b.startStates)
    res.addFinalStates(b.finalStates)
    res.addAlphabets(b.alphabets)
    trans_b = transitonsTOtransturples(b.transitions)
    res.addTransitions(trans_b)
    # keep one start state and one final state
    res.keepOneStartState()
    res.keepOneFinalState()
    return res

# when regex input is '.', simply concat the two automata
def dotConcat(a,b,input):
    # keep a and b only one start state and one final state
    a.keepOneStartState()
    a.keepOneFinalState()
    b.keepOneStartState()
    b.keepOneFinalState()
    # create res
    res = Automata()
    res = copyAutomata(a)
    # increse index of states of b
    maxIndexOfa = res.getMaxState()
    addNumOfb = maxIndexOfa + 1
    b.increaseStatesIndex(addNumOfb)
    # concat b to res
    res.addStates(b.states)
    res.addAlphabets(b.alphabets)
    res.addAlphabets(input)
    res.addTransitions(transitonsTOtransturples(b.transitions))
    afinal = maxIndexOfa
    bstart = maxIndexOfa + 1
    res.addTransitions([(afinal, bstart, input)])
    res.clearFinalStates()
    res.addFinalStates(b.finalStates)
    return res

# when regex input is '*', "star" the automata
def starConstruct(a):
    # create res
    res = Automata()
    res = copyAutomata(a)
    # keep res only one start state and one final state
    res.keepOneStartState()
    res.keepOneFinalState()
    # increase index of states of res
    res.increaseStatesIndex(1)
    # add transitions
    resfinal = res.getMaxState()
    res.addTransitions([(0,1,Automata.epsilon()),(resfinal,resfinal+1,Automata.epsilon())])
    res.addTransitions([(resfinal,1,Automata.epsilon()),(0,resfinal+1,Automata.epsilon())])
    # add start state
    res.clearStartStates()
    res.addStartStates(0)
    # add final state
    res.clearFinalStates()
    res.addFinalStates(resfinal+1)
    return res

if __name__ == "__main__":
    a=Automata()
    a.setBasicStructure("a")
    a.getTransitions()
    b=Automata()
    b.setBasicStructure("b")
    b.getTransitions()
    res=Automata()
    res = orConcat(a,b)
    c=Automata()
    c.setBasicStructure("c")
    res = dotConcat(res,c,"digit")
    res = starConstruct(res)
    # res.getTransitions()
    res.display()