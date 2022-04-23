from utility import listTOdict


# ============= type of token =============== #
KW = "KW"
OP = "OP"
SE = "SE"
IDN ="IDN"
INT = "INT"
FLT = "FLOAT"
STR ="STRING"
UNKOWN = "OP, SE, STR"
type = (KW, OP, SE, IDN, INT, FLT, STR)

# =============== list of keyword ============== #
keyWordList = [
    'SELECT','FROM','WHERE','AS','*',
    'INSERT','INTO','VALUES','VALUE','DEFAULT',
    'UPDATE','SET',
    'DELETE',
    'JOIN','LEFT','RIGHT','ON',
    'MIN','MAX','AVG','SUM',
    'UNION','ALL',
    'GROUP BY','HAVING','DISTINCT','ORDER BY',
    'TRUE','FALSE','UNKNOWN','IS','NULL'
]

kwWithWhiteSpace = ["ORDER", "GROUP", "order", "group"]
kwAfterWhiteSpace = [" BY", " by"]

# ============ list of operators =========== #
opList = [
    "=", '>', '<', '!', '&', '|', '.', '-'
]
opInIDNList = [
    "AND", "and", "OR", "or", "XOR", "xor","NOT", "not"
]
opEntityList = [
    '=', '>', '<', '>=', '<=', '!=', '<=>', 
    'AND', '&&', 'OR', '||', 'XOR', 'NOT', '!',
    '-',
    '.'
]
# ============ list of se =========== #
seList = ['(', ')', ',']

# ============ dict of tocken =========== #
kwDict = listTOdict(keyWordList)

opDict = listTOdict(opEntityList)

seDict = {
    '(':1, ')':2, ',':3
}

# ============ regex of SQL =============== #

digit = 'd' # '1-9'
upperLetter = 'L' # 'A-Z'
lowerLetter = 'l' # 'a-z'
allCharacter = 'C' # all characters, used for identify STR
epsilon = 'e' # epsilon, used for identify empty string

underscore = '_'

openingBracket = '['
closingBracket = ']'
orOperator = '+'
starOperator = '~'

# INTreg [0|[1-9][0-9]*]
INTzero = '0'
INTposreg = 'd[0+d]~'
INTreg = INTposreg + orOperator + INTzero

# FLTreg [0|[1-9][0-9]*].[0-9]*
dot = '.'
frontDot = openingBracket + INTreg + closingBracket
afterDot = '[0+d]~'
FLTreg = frontDot + dot + afterDot

# IDNreg [A-Za-z_][A-Za-z0-9_]*
IDNreg = "[L+l+_][L+l+_+0+d]~"

# OPreg "=|>|<|>=|<=|!=|<=>|AND|&&|OR||||XOR|.|!|-" AND OR XOR are will be treated as identity
OPreg = "=+>+<+>=+<=+!=+<=>+&&+||+.+!+-+*"

# SEreg  "(+)+,"
SEreg = '('+ orOperator + ')'+ orOperator + ','

# STRreg "C*"
STRreg = '"' + allCharacter + starOperator + '"'

regexSQL = [
    SEreg, #SE
    INTreg, #INT
    IDNreg, #IDN
    FLTreg, #FLOAT
    # KWreg, #KW
    OPreg, #OP
    STRreg #STR
]

finalRegex = " ~["+'+'.join(regexSQL)+"]"

if __name__ == "__main__":
    print(kwDict)
    print(opDict)
    print(digit)
    print(upperLetter)
    print(lowerLetter)
    print("===== INTreg =======\n", INTreg)
    print("===== IDNreg =======\n", IDNreg)
    print("===== FLTreg =======\n", FLTreg)
    print("===== KWreg =======\n", "No keyword regex, it will be treated as IDN") 
    print("===== OPreg =======\n", OPreg)
    print("===== SEreg =======\n", SEreg)
    print("===== STRreg =======\n", STRreg)
    print("===== regex =======\n", finalRegex)
    