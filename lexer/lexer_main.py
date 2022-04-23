from distutils.filelist import findall
from time import strftime
from finalDFA import finalDFA
from definitions import *

class lexer:
    def __init__(self, input_string):
        finalRes = finalDFA()
        self.dfa = finalRes.dfa
        self.input_string = input_string
        self.transitionTable=finalRes.transitionTable
        self.finalStateToType = finalRes.finalStateToType
        self.finalStates = self.dfa.finalStates

    def lexer(self):
        curState = 0
        curLexeme = ""
        input = ""
        # keep scan until it can not move to a new state
        # then check if current state is a final state
        # if is, judge what type the final state match
        # if not, the input is wrong
        i = 0
        strFlag = 0 # identify if it's a string
        self.input_string += ' '
        while i < len(self.input_string):
            ch = self.input_string[i]
            if strFlag==1 and ch!='"':
                input = 'C' # all characters
            elif isdigitEx0(ch):
                input = 'd'
            elif isUpperLetter(ch):
                input = 'L'
            elif isLowerLetter(ch):
                input = 'l' 
            else :
                input = ch
                # print("Going to switch!!!!")
                if ch == '"':
                    strFlag = 1-strFlag # switch
            if (curState, input) in self.transitionTable:
                curState = self.transitionTable[(curState, input)]
                if input != " ":
                    curLexeme += ch
                i += 1
            else :
                if curState in self.finalStates:
                    upperLexeme = curLexeme.upper()
                    if upperLexeme in kwWithWhiteSpace:
                        if self.input_string[i:i+3].upper() in kwAfterWhiteSpace:
                            curLexeme += self.input_string[i:i+3]
                            # self.printToken(KW, curLexeme)
                            i += 3
                            # continue
                        # else :
                            # self.printToken(IDN, curLexeme)
                    self.typeOfLexeme(curState, curLexeme)
                    curState = 0
                    if ch == '"':
                        strFlag = 0
                    curLexeme = ""
                else :
                    print("Current state is", curState)
                    # print("strFlag is : ", strFlag)
                    print("Current lexeme is", curLexeme)
                    print("Current input is", ch)
                    raise Exception("The input may be something wrong")

            
    def typeOfLexeme(self, curState, curLexeme):
        type = self.finalStateToType[curState]
        if type == INT or type == FLT:
            self.printToken(type, curLexeme)
        elif type == IDN:
            upperLexeme = curLexeme.upper()
            if upperLexeme in keyWordList:
                self.printToken(KW, curLexeme)
            elif upperLexeme in opInIDNList:
                self.printToken(OP, curLexeme)
            else:
                self.printToken(IDN, curLexeme)
        elif type == OP:
                self.printToken(OP, curLexeme)
        elif type == UNKOWN:
            lastch = curLexeme[len(curLexeme)-1]
            if lastch == '"':
                self.printToken(STR, curLexeme)
            elif lastch == '*':
                self.printToken(KW, curLexeme)
            elif lastch in opList:
                self.printToken(OP, curLexeme)
            elif lastch in seList:
                self.printToken(SE, curLexeme)
            else :
                print("Current state is", curState)
                print("Current lexeme is", curLexeme)
                raise Exception("It doesn't match any type of UNKOWN")
        else:
            print("Current state is", curState)
            print("Current lexeme is", curLexeme)
            raise Exception("It doesn't match any type")


    def printToken(self, type, lexeme):
        prop=""
        upperLexeme = lexeme.upper()
        if type == INT or type == FLT or type == STR or type == IDN:
            prop = lexeme
        elif type == SE:
            prop = seDict[lexeme]
        elif type == KW:
            prop = kwDict[upperLexeme]
        elif type == OP:
            # if upperLexeme in opInIDNList:
            prop = opDict[upperLexeme]
        else :
            raise Exception("Lexeme is %s, type is %s, no such type", lexeme, type)
        print(lexeme,"\t <",type, ",", prop, ">")


    
def isdigitEx0(ch):
    if ch >='1' and ch <='9':
        return True
    else: 
        return False

def isUpperLetter(ch):
    if ch >= 'A' and ch <= 'Z':
        return True
    else:
        return False

def isLowerLetter(ch):
    if ch >= 'a' and ch <= 'z':
        return True
    else:
        return False

    

if __name__ == "__main__":
    ipt = input("Please input a sql expression: ")
    print("The input is:", ipt)
    sqlLex = lexer(ipt)
    sqlLex.lexer()
