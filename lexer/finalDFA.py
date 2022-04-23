from nis import match
from unittest import case
from definitions import *
from Automata import Automata
from RegexToNFA import RegexToNFA
from NFAtoDFA import *
from DFAminimise import DFAminimise
from utility import DFAtoTransitionTable

class finalDFA:
    def __init__(self):
        self.dfa = self.finalDFA()
        self.transitionTable = self.finalTransitionTable()
        self.finalStateToType = self.getFinalStateToType()

    def finalDFA(self):
        finalRE = finalRegex
        nfa = RegexToNFA(finalRE).RegexToNFA()
        dfa = NFAtoDFA(nfa)
        finalDFA = DFAminimise(dfa).dfa
        finalDFA.display()
        drawGraph(finalDFA,"finalDFA")
        return finalDFA

    def finalTransitionTable(self):
        transitionTable = DFAtoTransitionTable(self.dfa)
        return transitionTable
    
    def printTransitionTable(self):
        for key, val in self.transitionTable.items():
            print(key, ': ', val)
    
    def getFinalStateToType(self):
        FinalStateToType = {}
        # assert type(FinalStateToType) == dict
        # print ("final states are: \n", self.dfa.finalStates)
        for state in self.dfa.finalStates:
            ipt = self.dfa.getInputOfStates(state)
            assert state not in FinalStateToType.keys()
            if '_' in ipt:
                FinalStateToType[state] = IDN
            elif '(' in ipt:
                FinalStateToType[state] = UNKOWN
            elif ipt == {'0'}:
                FinalStateToType[state] = INT
            elif 'd' in ipt:
                if '.' in ipt:
                    FinalStateToType[state] = FLT
                else :
                    FinalStateToType[state] = INT
            elif ipt == {'<'} or ipt == {'='} or ipt == {'>','!'}:
                FinalStateToType[state] = OP
            else:
                print ("ipt is ", ipt)
                raise Exception("No state match such input..")
        return FinalStateToType


# finalRes = finalDFA()
# FinalDFA = finalRes.dfa
# FinalTransitionTable = finalRes.transitionTable
# FinalStateToType = finalRes.getFinalStateToType()
# FinalStateToType = {1:IDN, 2:FLT, 3:INT, 4:OP, 5:OP, 6:INT, 7:OP, 8:UNKOWN}
# FinalStateToType = {1:UNKOWN, 2:OP, 3:INT, 4:FLT, 5:INT, 6:IDN, 7:OP, 8:OP}

if __name__ == "__main__":
    res = finalDFA()
    print("====== transition table ======")
    res.printTransitionTable()
    # print("======  FinalStateToType ======")
    # for key,val in FinalStateToType.items():
    #     print(key,": ", val)