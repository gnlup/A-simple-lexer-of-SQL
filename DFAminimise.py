from audioop import tostereo
import turtle
from Automata import Automata
from NFAtoDFA import *
from utility import *

class DFAminimise:
    def __init__(self, dfa):
        self.dfa = dfa
        self.dfa = self.DFAminimise()

    def createNewDivision(self, preState):
        '''
        According to preState and transitions of dfa, plus propogation principle,
        to create a new division
        preStates = [{..},{..}], stateCollection is one of {..} in preStates 
        RETURN: a list like preStates, but with new division
        '''
        curState = []
        for stateCollection in preState:
            curState+=self.divideStateCollection(stateCollection, preState)
        return curState

    def divideStateCollection(self, stateCollection, preState):
        '''
            return a list of new states, the new states are divided from stateCollection
            such as stateCollection {1,2,3} -> [{1,2},{3}]
        '''
        newStateCollection = []
        for ch in self.dfa.alphabets:
            # calculate ch_arch_transfrom for every satate in stateCollection
            ch_arch_transfrom = dict()
            newDivision = dict()
            for state in stateCollection:
                ch_arch_transfrom[state] = self.getToStateIndex(state, preState, ch)
            for fromState, toState in ch_arch_transfrom.items():
                if toState not in newDivision:
                    newDivision[toState] = set()
                newDivision[toState].add(fromState)
            if len(newDivision.values()) != 1:
                break
        newStateCollection = newDivision.values()
        return newStateCollection 

    def getToStateIndex(self, state, preState, ch):
        '''
            Given a state, get its transition state(i.e. toState),
            and get which state collection the toState is in according to current preState
        '''
        if state not in self.dfa.transitions:
            return -1
        ToState = 0
        for tostate, chset in self.dfa.transitions[state].items():
            if ch in chset:
                # ToState is where that we calculate from state via ch_arch to
                # For that it's dfa, given fromstate(i.e. state) and ch, there is only one ToState
                ToState = tostate
                break
        for i in range(len(preState)):
            if ToState in preState[i]:
                return i

    def DFAminimise(self):
        '''minimise a DFA'''
        # initial division: final states and non-final states 
        newStates = []
        newStates.append(self.dfa.finalStates)
        newStates.append(self.dfa.getNonFinalStates())
        preState = []
        # use propogation principle
        while True:
            preState = newStates
            newStates = self.createNewDivision(preState)
            if preState == newStates:
                break
        # now newStates is the final division of dfa states
        # create a dict to record new index of these divisions
        # such as we got new divisions like [{1,2},{3}], 
        # so the record will be {{1,2}:0,{3}:1}
        newStateDict = dict()
        assert len(self.dfa.startStates) == 1
        oldStartState = next(iter(self.dfa.startStates))
        i = 1 
        for states in newStates:
            if oldStartState in states:
                newStateDict[frozenset(states)] = 0
            else:
                newStateDict[frozenset(states)] = i
                i += 1
        # get a dict to record which new state does every old state belong to
        oldState2newState = self.getOldState2NewStateDict(newStateDict)
        # create a new transition dict
        newTransitions = self.createNewTransitions(oldState2newState)
        # get new Final states
        newFinalStates = self.getNewFinalStates(oldState2newState)
        newStatesAll = set(newStateDict.values())
        resdfa = Automata()
        resdfa.addStates(newStatesAll)
        resdfa.addStartStates(0)
        resdfa.addAlphabets(self.dfa.getAlphabets())
        resdfa.addFinalStates(newFinalStates)
        resdfa.addTransitions(newTransitions)
        return resdfa

    def getOldState2NewStateDict(self, newStateDict):
        '''
            create a dict to record which new state does every old state belong to
        '''
        oldState2newState = dict()
        for oldStates, newState in newStateDict.items():
            for oldState in oldStates:
                assert oldState not in oldState2newState
                oldState2newState[oldState] = newState
        return oldState2newState

    def createNewTransitions(self, oldStateTOnewState):
        '''
            create a new transition rules from oldStateTOnewState
            just go over every transition in the old transition dict, 
            get which new stateCollection does the old state(in the old transition dict) belongs to.
            oldStateTOnewState will be like {1:0,2:0,3:1}
            return type will be a list of three-turple like [(0,1,{'a'}),(1,2,{'a'}),(2,3,{'a'})],
        '''
        newTransitions = []
        # get new transitions
        for oldfromstate, oldtransitions in self.dfa.transitions.items():
            newfromstate = oldStateTOnewState[oldfromstate]
            for oldtostate, chset in oldtransitions.items():
                newtostate = oldStateTOnewState[oldtostate]
                for ch in chset:
                    newTransitions.append((newfromstate, newtostate, ch))
        return newTransitions

    def getNewFinalStates(self, oldStateTOnewState):
        oldFinalStates = self.dfa.finalStates
        newFinalStates = set()
        for oldFinalState in oldFinalStates:
            newFinalStates.add(oldStateTOnewState[oldFinalState])
        assert len(newFinalStates) >= 1
        return newFinalStates
        
if __name__ == "__main__":
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
    drawGraph(dfa, "non-minimise-dfa")
    dfamini = DFAminimise(dfa)
    resdfa = dfamini.DFAminimise()
    resdfa.display()
    drawGraph(resdfa)
        
