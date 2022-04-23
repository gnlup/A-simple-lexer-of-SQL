# import string
# from graphviz import Digraph
from os import popen
import time

class Automata:
    def __init__(self):
        '''states are int, alphabets can be string or int(discuss later)'''
        self.states=set()
        self.startStates=set()
        self.finalStates=set()
        self.alphabets=set()
        self.transitions=dict() # {fromstate:{tostate:input}}

    @staticmethod
    def epsilon():
        return "__EPSILON__"

    def addStates(self,states):
        if isinstance(states, int):
            states = set([states])
        self.states.update(states)

    def addStartStates(self,startStates):
        if isinstance(startStates, int):
            startStates = set([startStates])
        self.startStates.update(startStates)

    def addFinalStates(self,finalStates):
        if isinstance(finalStates, int):
            finalStates = set([finalStates])
        self.finalStates.update(finalStates)

    def addAlphabets(self,alphabets):
        if isinstance(alphabets, str):
            alphabets = set([alphabets])
        self.alphabets.update(alphabets)

    def addTransitions(self, newTransitions):
        '''newTransitions must be passed as a list of three-turple such as [(1,2,'a'),(2,3,['b','c','d'])]'''
        for trans in newTransitions:
            fromstate, tostate, inputs = trans
            if isinstance(inputs, str):
                inputs=set([inputs])
            if fromstate not in self.states:
                self.addStates(fromstate)
            if tostate not in self.states:
                self.addStates(tostate)
            for input in inputs:
                if input not in self.alphabets:
                    self.addAlphabets(input)
            if fromstate not in self.transitions:
                self.transitions[fromstate] = dict()
            if tostate not in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = set()
            self.transitions[fromstate][tostate].update(inputs) 
    
    def setBasicStructure(self, input=epsilon.__func__()):
        if len(self.states)!=0:
            print("The automata has already got some structure, please reset it first.")
        else :
            if isinstance(input, str):
                input = set([input])
            self.addStates(0)
            self.addStates(1)
            self.addStartStates(0)
            self.addFinalStates(1)
            self.addAlphabets(input)
            self.addTransitions([(0,1,input)])

    def getStates(self):
        print("States are:",self.states)
        return self.states

    def getStartStates(self):
        print("Start States are:",self.startStates)
        return self.startStates

    def getFinalStates(self):
        print("Final States are:",self.finalStates)
        return self.finalStates

    def getNonFinalStates(self):
        self.nonFinalStates = set()
        for state in self.states:
            if state not in self.finalStates:
                self.nonFinalStates.add(state)
        return self.nonFinalStates
    
    def getAlphabets(self):
        print("Alphabets are:",self.alphabets)
        return self.alphabets

    def getTransitions(self):
        for fromstate, tostates in self.transitions.items():
            for tostate, inputs in tostates.items():
                print(fromstate, "->", tostate, ":", inputs)
        return self.transitions

    def getInputOfStates(self, state):
        '''which inputs can transform to this->state'''
        input = set()
        for tostates in self.transitions.values():
            if state in tostates:
                input.update(tostates[state])
        return input

    def display(self):
        print("==== DISPLAYING AUTOMATA ====")
        self.getStates()
        self.getStartStates()
        self.getFinalStates()
        self.getAlphabets()
        print(self.transitions)
        self.getTransitions()

    def isValid(self):
        '''
            check if the automata is valid
            valid state: when states is empty, the automata is empty; 
            when states is not empty, the automata must have at least one start state, one final state, one transition and one alphabet
            Also, the sum of start state and final state must be less than the number of states
        '''
        print("Checking if the automata is valid...")
        if len(self.states)==0:
            if len(self.startStates)!=0 or len(self.finalStates)!=0 or len(self.transitions)!=0 or len(self.alphabets)!=0:
                raise Exception("The automata has no states, but has start states or final states or transitions or alphabets.")
            print("The automata is valid.")
            return True
        else:
            '''in this case, we don't allow \Phi language'''
            if len(self.startStates)==0:
                raise Exception("The automata has no start state, please set it first.")
            if len(self.finalStates)==0:
                raise Exception("The automata has no final state, please set it first.")
            if len(self.alphabets)==0:
                raise Exception("The automata has no alphabet, please set it first.")
            if len(self.transitions)==0:
                raise Exception("The automata has no transition, please set it first.")
            if len(self.startStates.union(self.finalStates))>len(self.states):
                raise Exception("The automata's total number of start states and final states is bigger the total number of states.")
            print("The automata is valid.")
            return True

    def isEmpty(self):
        print("Checking if the automata is empty...")
        if len(self.states)==0:
            print("Empty!")
            return True
        else :
            print("Not empty!")
            return False
        
    def increaseStatesIndex(self, addNum):
        '''increase the index of states by addNum'''
        newStates = {x+addNum for x in self.states}
        self.states = newStates.copy()
        newStartStates = {x+addNum for x in self.startStates}
        self.startStates = newStartStates.copy()
        newFinalStates = {x+addNum for x in self.finalStates}
        self.finalStates = newFinalStates.copy()
        newTransitions = dict()
        for fromstate, tostates in self.transitions.items():
            newTransitions[fromstate+addNum] = dict()
            for tostate, inputs in tostates.items():
                newTransitions[fromstate+addNum][tostate+addNum] = inputs.copy()
        self.transitions = newTransitions.copy()

    def keepOneStartState(self):
        '''keep only one start state'''
        if len(self.startStates)==1:
            pass
            # print("There is only one start state, no need to keep it.")
        else:
            '''add a new start state "0" and add transitions from 0 to old satrt states'''
            self.increaseStatesIndex(1)
            self.addStates(0)
            for oldStartState in self.startStates:
                self.addTransitions([(0,oldStartState, Automata.epsilon())])
            self.clearStartStates()
            self.addStartStates(0)
        return self

    def getMaxState(self):
        '''get the max index of all states'''
        return max(self.states)

    def keepOneFinalState(self):
        '''keep only one final state'''
        if len(self.finalStates)==1:
            pass
            # print("There is only one final state, no need to keep it.")
        else:
            newFinalState = self.getMaxState()+1
            self.addStates(newFinalState)
            for oldFinalStates in self.finalStates:
                self.addTransitions([(oldFinalStates, newFinalState, Automata.epsilon())])
            self.clearFinalStates()
            self.addFinalStates(newFinalState)

    def resetAutomata(self):
        self.states = set()
        self.startStates = set()
        self.finalStates = set()
        self.alphabets = set()
        self.transitions = dict()

    def clearStartStates(self):
        self.startStates = set()
    
    def clearFinalStates(self):
        self.finalStates = set()

    def getDotFile(self):
        dotFile = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            if len(self.startStates) != 1:
                raise Exception("Automata must has only one start state!")
            dotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % next(iter(self.startStates))
            for state in self.states:
                if state in self.finalStates:
                    dotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    dotFile += "s%d [shape=circle]\n" % state
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    for char in tostates[state]:
                        if char == '"':
                            char = '\\"'
                        dotFile += 's%d->s%d [label="%s"]\n' % (fromstate, state, char)
        dotFile += "}"
        with open("dotfile.dot", "w") as f:
            f.write(dotFile)
        return dotFile


if __name__ == "__main__":
    t = Automata()
    t.setBasicStructure()
    t.increaseStatesIndex(10)
    t.getTransitions()
    