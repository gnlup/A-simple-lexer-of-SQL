# from operator import index
from Automata import Automata
from BuildAutomata import *
from utility import *
from definitions import *

class RegexToNFA:
    def __init__(self, regex):
        self.regex = regex
        print("The regex is: ",self.regex)
        self.operatorStack = []
        self.automataStack = []
        self.openingBracket = '['
        self.closingBracket = ']'
        self.starOperator ='~'
        self.dotOperator = '`'
        self.orOperator = '+'
        self.backslash = '\\'
        self.operators = [self.starOperator, self.dotOperator, self.orOperator]
        self.noStarOperators = [self.dotOperator, self.orOperator]
        '''
            priority   [   ]   *   +   `
                [      <   =   <   <   <
                `      <   >   <   >   >
                +      <   >   <   >   <
            ] will never go into the stack
            * will never go into the stack
        '''
        self.priorityTable = \
        {
            self.openingBracket:{self.openingBracket:'<',self.closingBracket:'=',self.starOperator:'<',self.orOperator:'<',self.dotOperator:'<'},\
            self.dotOperator:{self.openingBracket:'<',self.closingBracket:'>',self.starOperator:'<',self.orOperator:'>',self.dotOperator:'>'},\
            self.orOperator:{self.openingBracket:'<',self.closingBracket:'>',self.starOperator:'<',self.orOperator:'>',self.dotOperator:'<'}
        }  
        self.priorThanOr = [self.starOperator, self.dotOperator, self.orOperator]
        self.inferiorThanOr = [self.openingBracket]
        self.alphabets = set()
        self.alphabets.update([chr(i) for i in range(65,91)])
        self.alphabets.update([chr(i) for i in range(97,123)])
        self.alphabets.update([chr(i) for i in range(48,58)])
        self.otherAlphabets = {'=', '>', '<', '!', '.', ' ', '&', '|', '_', ',', '(', ')','-','"','*'}
        self.alphabets.update(self.otherAlphabets)
        self.NFA = Automata()

    def RegexToNFA(self):
        self.regex = self.addDotOperator()
        print(self.regex)
        self.checkRegex()
        for c in self.regex:
            if c in self.alphabets:
                self.automataStack.append(basicStructure(c))
            elif c == self.openingBracket:
                self.operatorStack.append(c)
            elif c == self.closingBracket:
                if len(self.operatorStack) == 0:
                    raise Exception("Empty operator stack. No opening bracket before closing bracket..")
                while len(self.operatorStack) > 0:
                    ch = self.operatorStack[-1]
                    if ch == self.openingBracket:
                        self.operatorStack.pop()
                        break
                    self.processOperator(ch)
                    self.operatorStack.pop()
            elif c == self.orOperator:
                while len(self.operatorStack) > 0:
                    ch = self.operatorStack[-1]
                    if self.priorityTable[ch][c] == '<':
                        self.operatorStack.append(c)
                        break
                    else :
                         self.processOperator(ch)
                         self.operatorStack.pop()
                if len(self.operatorStack) == 0:
                    self.operatorStack.append(c)
            elif c == self.dotOperator:
                while len(self.operatorStack) > 0:
                    ch = self.operatorStack[-1]
                    if self.priorityTable[ch][c] == '<':
                        self.operatorStack.append(c)
                        break
                    else :
                         self.processOperator(ch)
                         self.operatorStack.pop()
                if len(self.operatorStack) == 0:
                    self.operatorStack.append(c)
            elif c == self.starOperator:
                if len(self.automataStack) == 0:
                    raise Exception("ERROR! No automata in stack, can not calculate star operator.")
                self.processOperator(c)
            else :
                raise Exception("ERROR! Invalid character in regex. Regex can only contain alphabets and + ` * ( )")
        while len(self.operatorStack) > 0:
            ch = self.operatorStack[-1]
            self.processOperator(ch)
            self.operatorStack.pop()
        if len(self.operatorStack) != 0:
            raise Exception("ERROR! There may still are operators in operatorStack, something is wrong.")
        if len(self.automataStack) != 1:
            raise Exception("ERROR! There must be only one automata in stack, something is wrong.")
        self.NFA = self.automataStack.pop()
        return self.NFA

    def checkRegex(self):
        pre = ''
        for c in self.regex:
            if c == self.closingBracket:
                if pre in self.noStarOperators or pre == '':
                    raise Exception("ERROR! Invalid regex. No operator or '' before closing bracket.")
            elif c == self.openingBracket:
                if pre in self.alphabets or pre == self.closingBracket or pre == self.starOperator:
                    raise Exception("ERROR! Invalid regex. Before opening bracket must be operators.")
            elif c == self.starOperator:
                if pre in self.operators or pre == '' or pre == self.openingBracket:
                    raise Exception("ERROR! Invalid regex. Before star operator must be alphabets or closing bracket.")
            elif c == self.dotOperator:
                if pre in self.noStarOperators or pre == '' or pre == self.openingBracket:
                    raise Exception("ERROR! Invalid regex. Before dot operator must be alphabets or closing bracket.")
            elif c == self.orOperator:
                if pre in self.noStarOperators or pre == '' or pre == self.openingBracket:
                    raise Exception("ERROR! Invalid regex. Before or operator must be alphabets or closing bracket.")
            elif c in self.alphabets:
                if pre in self.alphabets or pre == self.closingBracket or pre == self.starOperator:
                    raise Exception("ERROR! Invalid regex. Two alphabets in a row.")
            else :
                print("Invalid character: ", c)
                raise Exception("ERROR! Invalid regex. Invalid character.")
            pre = c

    def addDOTcondition(self, a, b):
        if a in self.alphabets:
            if b in self.alphabets or b == self.openingBracket:
                return True
            return False
        if a == self.closingBracket:
            if b in self.alphabets or b == self.openingBracket:
                return True
            return False
        if a == self.starOperator:
            if b in self.alphabets or b == self.openingBracket:
                return True
            return False
        return False

    def addDotOperator(self):
        if len(self.regex) == 0:
            raise Exception("ERROR! Empty regex.")
        if len(self.regex) == 1:
            return self.regex
        i = 1
        while i < len(self.regex):
            if self.addDOTcondition(self.regex[i-1], self.regex[i]):
                self.regex = self.regex[:i] + self.dotOperator + self.regex[i:]
                i += 1
            i += 1
        return self.regex

    def processOperator(self, ch):
        if ch == self.dotOperator:
            if len(self.automataStack) < 2:
                raise Exception("No enough automata for DOT operator..")
            a = self.automataStack.pop()
            b = self.automataStack.pop()
            res = Automata()
            res = dotConcat(b, a, Automata.epsilon())
            self.automataStack.append(res)
        if ch == self.orOperator:
            if len(self.automataStack) < 2:
                raise Exception("No enough automata for OR operator..")
            a = self.automataStack.pop()
            b = self.automataStack.pop()
            res = Automata()
            res = orConcat(b, a)
            self.automataStack.append(res)
        if ch == self.starOperator:
            if len(self.automataStack) < 1:
                raise Exception("No automata in stack, ERROR!")
            a = self.automataStack.pop()
            res = Automata()
            res = starConstruct(a)
            self.automataStack.append(res)

    def getNFA(self):
        return self.NFA

    def printNFA(self):
        self.NFA.display()


if __name__ == "__main__":
    regex = input("Enter a regular expression: ")
    trans = RegexToNFA(regex)
    # res = Automata()
    res = trans.RegexToNFA()
    # res.isValid()
    trans.NFA.isValid()
    trans.NFA.isEmpty()
    trans.printNFA()
    drawGraph(res)
            
