from Automata import Automata
from os import popen

def copyAutomata(a):
    newcopy = Automata()
    newcopy.states = a.states.copy()
    newcopy.startStates = a.startStates.copy()
    newcopy.finalStates = a.finalStates.copy()
    newcopy.alphabets = a.alphabets.copy()
    newcopy.transitions = a.transitions.copy()
    return newcopy

def transitonsTOtransturples(transitions):
    '''transform transitions from dict to list like [(1,2,'a'),(2,3,['b','c','d'])]'''
    transturples = []
    for fromstate, tostates in transitions.items():
        for tostate, inputs in tostates.items():
            transturples.append((fromstate, tostate, inputs))
    return transturples

def drawGraph(automata, file = ""):
    """From https://github.com/max99x/automata-editor/blob/master/util.py"""
    f = popen(r"dot -Tpng -o %s.png" % file, 'w')
    try:
        f.write(automata.getDotFile())
    except:
        raise BaseException("Error creating graph")
    finally:
        f.close()

def isDFA(dfa):
    pass

def upsidedownDict(dic):
    '''exchange keys and values of a dict'''
    newDict = dict()
    for key, value in dic.items():
        if value not in newDict:
            newDict[value] = set()
        if type(key) != set:
            key = set(key)
        newDict[value].update(key)
    return newDict

def regexTrans(regex):
    '''input will be like *-*'''
    st = regex[0]
    fn = regex[len(regex)-1]
    newreg = st
    for i in range(ord(st)+1, ord(fn)+1):
        newreg = newreg + '+' + chr(i)
    return newreg

def DFAtoTransitionTable(dfa):
    transitionTable = dict()
    for fromstate, tostates in dfa.transitions.items():
        for tostate in tostates:
            for ch in tostates[tostate]:
                assert (fromstate, ch) not in transitionTable
                transitionTable[(fromstate, ch)] = tostate
    return transitionTable

def listTOdict(l):
    '''transform a list to a dict'''
    dic = dict()
    j = 1
    for i in l:
        dic[i] = j
        j += 1
    return dic

if __name__ == "__main__":
    # a = Automata()
    # a.setBasicStructure("a")
    # a.display()
    # drawGraph(a)
    regex = '0-9'
    newreg = regexTrans(regex)
    print(newreg)
