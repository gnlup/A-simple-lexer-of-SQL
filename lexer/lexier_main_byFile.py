from utility_regex import *
from entity_regex import *
from definitions import *
from finalDFA import finalDFA

class Lexiyer(object):
    def __init__(self, input_file_path=None, output_file_path=None):
        self.key_words = KEY_WORDS
        self.se = SE
        self.operations = OPERATIONS
        self.vocabulary = VOCABULARY

        self.token_sequence = []
        self.lexeme_sequence = []

        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

        self.lexeme_sequence_file = None
        self.token_sequence_file = None
        self.input_file = None

        self.proc_line = None
        self.line_index = 0
        self.ptr = 0
        self.value = ''
        self.name = ''

        self.kwdict = kwDict
        self.opdict = opDict
        self.sedict = seDict

        finalRes = finalDFA()
        self.dfa = finalRes.dfa
        self.transitionTable = finalRes.transitionTable
        self.finalStateToType = finalRes.finalStateToType
        self.finalStates = self.dfa.finalStates
        self.current_state = 0
        self.now_state = 0
        self.category_in = None

    # initialize the token and lexeme sequence
    def initialize(self):
        self.token_sequence = []
        self.lexeme_sequence = []

    # read file by lines
    def read_file(self, input_file=None):
        if input_file is None:
            print('Input file path not found.')
        else:
            files = [input_file]
        for file in files:
            self.initialize()
            self.input_file = os.path.join(os.path.join(ROOT_PATH, self.input_file_path), file)
            print("read the code in {}.".format(self.input_file))
            with open(self.input_file, 'r') as read_file:
                for line_index, line in enumerate(read_file.readlines()):
                    line_index += 1
                    line = line.strip()
                    line += ' '
                    print(line)
                    if line:
                        self.line_index = line_index
                        self.process_line(line)
            # self.save_lexeme_sequence(file)
            # self.save_token_sequence(file)
            for inst in self.token_sequence:
                print(inst)
        pass

    def back_char(self):
        if self.ptr < len(self.proc_line):
            ch = self.proc_line[self.ptr-1]
            return ch
        else:
            return None

    def isdigitEx0(self, ch=None):
        if ch >= '1' and ch <= '9':
            return True
        else:
            return False

    def isUpperLetter(self, ch=None):
        if ch >= 'A' and ch <= 'Z':
            return True
        else:
            return False

    def isLowerLetter(self, ch=None):
        if ch >= 'a' and ch <= 'z':
            return True
        else:
            return False

    # save the token from the code
    def token_sequence_save(self, name=None, category=None):
        if name:
            self.lexeme_sequence.append(name)
            instance = Token_Seq(token_name=str(name), token_type=category, token_value=str(name), line_index=self.line_index)
            if instance.token_name in self.key_words:
                instance.token_value = self.kwdict[instance.token_name]
            elif instance.token_name in self.operations:
                instance.token_value = self.opdict[instance.token_name]
            elif instance.token_type in self.se:
                instance.token_value = self.sedict[instance.token_name]
            self.token_sequence.append(instance)
        else:
            return

    # process the input line
    def process_line(self, line=None,):
        if line is None:
            return
        elif line.strip().startswith("--"):
            return
        elif line.strip().startswith("#"):
            return
        self.proc_line = line
        self.ptr = 0
        self.name = ''
        str_flag = 0
        print("the length of the line is", (len(self.proc_line)))
        while self.ptr < len(self.proc_line):
            print("the current ptr is", self.ptr)
            ch = self.proc_line[self.ptr]
            print("输入的字符是", (ch))
            if str_flag == 1 and ch != '"':
                input_ch = 'C'
            elif str_flag == 1 and ch == '"':
                str_flag = 0
                input_ch = '"'
            elif str_flag == 0 and ch == '"':
                str_flag = 1
                input_ch = '"'
            elif self.isdigitEx0(ch=ch):
                input_ch = 'd'
            elif self.isUpperLetter(ch=ch):
                input_ch = 'L'
            elif self.isLowerLetter(ch=ch):
                input_ch = 'l'
            else:
                input_ch = ch
            print("格式化后，输入的字符input_ch is", (input_ch))
            print("after input_ch, flag is", (str_flag))

            if ((self.current_state, input_ch) in self.transitionTable):
                print("previous key is", (self.current_state, input_ch))
                self.current_state = self.transitionTable[(self.current_state, input_ch)]
                print("after transition, key is", (self.current_state, input_ch))
                if input_ch != ' ':
                    self.name += ch
                print("current name is", (self.name))
                self.ptr += 1
            else:
                print("previous key which is not in the table is", (self.current_state, input_ch))
                print("current name is", (self.name))
                if self.current_state in self.finalStates:
                    upperName = self.name.upper()
                    if upperName in kwWithWhiteSpace:
                        if self.proc_line[self.ptr:self.ptr + 3] in kwAfterWhiteSpace:
                            print("this is a kw with kwAfterWhiteSpace")
                            self.name += self.proc_line[self.ptr:self.ptr + 3]
                            self.token_sequence_save(name=self.name, category='KW')
                            self.ptr += 3
                            self.current_state = 0
                            self.name = ''
                            str_flag = 0
                            continue
                        else:
                            print("this is an idn with kwWithWhiteSpace")
                            self.token_sequence_save(name=self.name, category='IDN')
                    self.now_state = self.current_state
                    self.category_in = self.finalStateToType[self.now_state]
                    print("the category without kwAfterWhiteSpace is", self.category_in)
                    if self.category_in == IDN:
                        upperName = self.name.upper()
                        if upperName in keyWordList:
                            print("the category is KW")
                            self.token_sequence_save(name=self.name, category='KW')
                        elif upperName in opInIDNList:
                            print("the category is OP")
                            self.token_sequence_save(name=self.name, category='OP')
                        else:
                            print("the category is IDN")
                            self.token_sequence_save(name=self.name, category='IDN')
                    elif self.category_in == INT:
                        self.token_sequence_save(name=self.name, category='INT')
                    elif self.category_in == FLT:
                        self.token_sequence_save(name=self.name, category='FLT')
                    elif self.category_in == OP:
                        self.token_sequence_save(name=self.name, category='OP')
                    elif self.category_in == UNKOWN:
                        back_ch = self.back_char()
                        if back_ch in ['(', ')', ',']:
                            self.token_sequence_save(name=self.name, category='SE')
                        elif back_ch == '"':
                            self.token_sequence_save(name=self.name, category='STR')
                        else:
                            self.token_sequence_save(name=self.name, category='OP')
                    else:
                        print("the DFA fails to identify the type.")
                    self.current_state = 0
                    self.name = ''
                    str_flag = 0
                else:
                    self.current_state = 0
                    self.name = ''
                    str_flag = 0
                    print("the input is wrong.")
                    exit()
                print("after transition, key not in the table is", (self.current_state, ch))

    # save the lexeme_sequence
    def save_lexeme_sequence(self, file=None):
        if file is None:
            return
        else:
            self.lexeme_sequence_file = os.path.join(
                os.path.join(ROOT_PATH, os.path.join(self.output_file_path, 'lexeme_sequence'), file) )
        print("find the lexeme_sequence in {}.".format(self.lexeme_sequence_file))
        with open(self.lexeme_sequence_file, 'w') as output_file:
            for lex in self.lexeme_sequence:
                output_file.write(str(lex)+'\n')

    # save the token_sequence
    def save_token_sequence(self, file = None):
        if file is None:
            return
        else:
            self.token_sequence_file = os.path.join(
                os.path.join(ROOT_PATH, os.path.join(self.output_file_path, 'token_sequence'), file) )
        print("find the token_sequence in {}.".format(self.token_sequence_file))
        with open(self.token_sequence_file, 'w') as output_file:
            for token in self.token_sequence:
                output_file.write(str(token)+'\n')

    #  read a character from the code

    def _in_vocabulary(self, ch = None):
        if ch:
            return ch in self.vocabulary
        else:
            return False

    def next_char(self):
        if self.ptr < len(self.proc_line):
            ch = self.proc_line[self.ptr]
            return ch
        else:
            return None

    def back_to_char(self):
        if self.name:
            self.name = self.name[0:-1]
            self.ptr -=1
        else:
            print("length of the name is 0.")


if __name__ == '__main__':
    INPUT_FILE = 'test_input'
    OUTPUT_FILE = 'test_output'
    LEXICAL_ANYLIZER = Lexiyer(input_file_path=INPUT_FILE, output_file_path=OUTPUT_FILE)
    LEXICAL_ANYLIZER.read_file(input_file='input.txt')
