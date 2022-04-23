from Automata import Automata
from RegexToNFA import RegexToNFA
from BuildAutomata import *

def NFAtoDFA(nfa):
    '''convert e-NFA to DFA and minimise it'''
    # keep one start state of nfa
    nfa.keepOneStartState()
    # get e-closure
    e_closure = get_e_closure(nfa)
    # get DFA
    dfa = Automata()
    statesQueue = []
    newStates = dict()
    newTransitions = dict()
    # start calculate new states and new transitions
    newState = set()
    newState = e_closure[nfa.startStates.pop()]
    maxidx = 0
    newStates[frozenset(newState)] = maxidx
    dfa.startStates = set([maxidx])
    maxidx += 1
    statesQueue.append(newState)
    while statesQueue:
        currentState = statesQueue.pop(0)
        currentState = frozenset(currentState)
        for alphabet in nfa.alphabets:
            if alphabet == Automata.epsilon():
                continue
            newState = set()
            for state in currentState:
                '''calculate a_arch_transformation of the state'''
                if state not in nfa.transitions:
                    continue
                toStates = nfa.transitions[state]
                for toState in toStates:
                    if alphabet in toStates[toState]:
                        newState.update(e_closure[toState])
            newState = frozenset(newState)
            if newState:
                if newState not in newStates:
                    newStates[newState] = maxidx
                    maxidx += 1
                    statesQueue.append(newState)
                newFromState = newStates[currentState]
                newToState = newStates[newState]
                if newFromState not in newTransitions:
                    newTransitions[newFromState] = dict()
                if newToState not in newTransitions[newFromState]:
                    newTransitions[newFromState][newToState] = set()
                newTransitions[newFromState][newToState].add(alphabet)
    dfa.states = set(newStates.values())
    dfa.alphabets = nfa.alphabets
    dfa.transitions = newTransitions
    # get final states of dfa
    dfa.finalStates = set()
    for finalState in nfa.finalStates:
        for newState in newStates.keys():
            if finalState in newState:
                dfa.finalStates.add(newStates[newState])
    return dfa

def get_a_arch_transformation(nfa, state, a_arch, e_closure):
    '''get a-arch transformation of a state'''
    a_arch_transformation = set()
    if state not in nfa.transitions:
        return a_arch_transformation
    toStates = nfa.transitions[state]
    for toState in toStates:
        if a_arch in toStates[toState]:
            a_arch_transformation.update(e_closure[toState])
    return a_arch_transformation

def get_e_closure(nfa):
    '''get e-closure of a NFA'''
    e_closure = dict()
    for state in nfa.states:
        e_closure[state] = get_e_closure_of_state(nfa, state)
    return e_closure

def get_e_closure_of_state(nfa, state):
    '''get e-closure of a state'''
    e_closure = set()
    e_closure.add(state)
    myqueue = [state]
    while myqueue:
        currentState = myqueue.pop(0)
        if currentState not in nfa.transitions:
            continue
        toStates = nfa.transitions[currentState]
        for toState in toStates:
            if Automata.epsilon() in toStates[toState]:
                if toState not in e_closure:
                    e_closure.add(toState)
                    myqueue.append(toState)
    return e_closure
    

if __name__ == '__main__':
    # regex = 'a[b+c]*'
    regex = input("Please input a regex: ")
    nfa = RegexToNFA(regex).RegexToNFA()
    # nfa1 = Automata()
    # nfa1 = basicStructure('a')
    # nfa2 = Automata()
    # nfa2 = basicStructure('b')
    # nfa = Automata()
    # nfa = orConcat(nfa1, nfa2)
    nfa.display()
    dfa = NFAtoDFA(nfa)
    dfa.display()
    drawGraph(dfa)