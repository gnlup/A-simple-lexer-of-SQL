import os

os.chdir('./')

ROOT_PATH = os.getcwd()

KEY_WORDS = ['SELECT', 'FROM', 'WHERE', 'AS',
             'INSERT', 'INTO', 'VALUES',
             'UPDATE', 'DELETE',
             'JOIN', 'LEFT', 'RIGHT'
             'MIN', 'MAX', 'AVG', 'SUM'
             'UNION', 'ALL',
             'GROUP BY', 'HAVING', 'DISTINCT', 'ORDER BY',
             'TRUE', 'FALSE', 'IS', 'NOT', 'NULL']
OPERATIONS = ['=', '>', '<', '<=', '>=', '!=', '<=>',
              'AND', '&&', 'OR', '||', 'XOR', '.']
SE = ['(', ')', ',']
ESCAPING_STRING = ['\0', '\n', '\r', '\t', '\v', '\a', '\b', '\f', "\'", '\"', '\\']
VOCABULARY = '-'.join(
    ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~').split('-')
VOCABULARY.append('-')
VOCABULARY.append('\\')


