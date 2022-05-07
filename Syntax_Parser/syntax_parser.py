import xlwt


# 初始化
class grammar:
    # 定义
    def __init__(self):
        self.productions = []  # 产生式：列表
        self.productions_dict = {}  # 产生式字典用于查询 key: [(表达式右边符号序列，数字)，(表达式右边符号序列，数字)]
        self.term = set()  # 终结符：集合类型
        self.nterm = set()  # 非终结符：集合类型
        self.all_term = set()  # term+nterm：集合类型
        self.first_set = {}  # first集：字典嵌套集合

    # ----------读取txt，转换为产生式-------------
    def init_grammar(self, file_name):
        for line in open(file_name, 'r'):
            line = line[:-1]
            left = line.split(' -> ')[0]
            right = line.split(' -> ')[1]
            right_list = []
            right.strip(' ')
            if right.find('GROUP BY') != -1:
                right_list.append('GROUP BY')
                right = right.replace('GROUP BY ', '')
            if right.find('ORDER BY') != -1:
                right_list.append('ORDER BY')
                right = right.replace('ORDER BY ', '')
            if right.find(' ') == -1:
                right_list.append(right)
            else:
                right_list += right.split(' ')
            production = {left: right_list}
            self.productions.append(production)
        self.get_termornot()
        self.init_firstset()
        self.gram_inf()

    # -----------获取终结符集和非终结符集-------------
    def get_termornot(self):
        for production in self.productions:
            for left in production.keys():
                if left not in self.productions_dict:
                    self.productions_dict[left] = []
                self.productions_dict[left].append((
                    production[left],
                    self.productions.index(production)))
                self.all_term.add(left)
                self.nterm.add(left)
                for right in production[left]:
                    self.all_term.add(right)
        self.term = self.all_term - self.nterm
        self.term.add('#')

    # -------------获取first集-------------
    def get_firstset(self, status, all_elem):
        if status in self.first_set:
            return self.first_set[status]
        all_elem.add(status)
        result = set()
        for right_list in self.productions_dict[status]:  # 先由键值找到表达式元组构成的序列->对序列中每个表达式元组
            for right in right_list[0]:  # 表达式元组[0]->产生式右端符号序列->右端符号序列中每个符号
                if right in all_elem:
                    continue
                if right in self.first_set:
                    right_set = self.first_set[right]
                else:
                    right_set = self.get_firstset(right, all_elem)
                result |= right_set
                if '$' not in right_set:
                    break
        return result

    def init_firstset(self):
        for term in self.term:
            self.first_set[term] = {term}
        for nterm in self.nterm:
            self.first_set[nterm] = self.get_firstset(nterm, set())
        self.first_set['#'] = {'#'}

    # --------------print to txt--------------
    def gram_inf(self):
        f = open('lr1_grammar_information.txt', 'w')
        ff = open('lr1_first_set.txt', 'w')
        # production print
        i = 1
        print('production:', file=f)
        for every in self.productions:
            if i < 10:
                print(' ', i, " :", every, file=f)
            elif i < 100:
                print(i, " : ", every, file=f)
            else:
                print(i, ":", every, file=f)
            i = i + 1
        # production_dict
        print(self.productions_dict, file=f)
        # term print
        print('\nterm:\n', sorted(self.term, key=str.lower), file=f)
        print('\nnterm:\n', sorted(self.nterm, key=str.lower), file=f)
        # first_set print
        print('\nFIRST:', file=f)
        for every in sorted(self.all_term, key=str.lower):
            print("first_set[", every, "]  =  ", list(self.first_set[every]), file=f)
        print('FIRST:', file=ff)
        for every in sorted(self.all_term, key=str.lower):
            print(every, "  =  ", list(self.first_set[every]), file=ff)
        f.close()
        ff.close()


# 生成excel单元样式的方法
def title_style():
    # 创建字体
    font = xlwt.Font()
    # 字体类型
    font.name = 'Times New Roman'
    # 设置字体大小
    font.height = 20 * 18
    font.bold = True  # 加粗
    style = xlwt.XFStyle()  # 创建style
    style.alignment.vert = 1  # 居中
    style.alignment.horz = 2  # 居中
    style.font = font  # style的字体为上面定义的字体
    return style


# lr(1)分析法
class lr1_grammar(grammar):
    def __init__(self):
        super().__init__()
        self.items = []  # 项目集三元组（production ，location，ahead character）
        self.lr1_productions = []
        self.items_family = set()  # 项目集规范族
        self.lr1_analyze_table = [{}]  # 分析表：字典 行是列表的元素 字典为{列：action/go}

    def dic2list(self):
        for every in self.productions:
            leftlist = list(every.keys())
            rightlist = list(every.values())[0]
            ans = leftlist + rightlist
            self.lr1_productions.append(ans)

    # -------------闭包运算--------------
    def closure(self, some_items):
        some_items = some_items[:]
        for (prod_id, dot_pos, ahead) in some_items:
            # 产生式右侧 prod
            prod = self.lr1_productions[prod_id][1:]
            if dot_pos < len(prod):
                cur = prod[dot_pos]  # 点后面的字符
                nss = []  # next symbol 终结符b
                tmpseq = prod[dot_pos + 1:] + [ahead]  # ba
                i = 0
                while i < len(tmpseq):
                    for x in self.first_set[tmpseq[i]]:
                        if (x != '$' or tmpseq[i] == '$') and x not in nss:
                            nss.append(x)
                            # print(x)
                    if '$' not in self.first_set[tmpseq[i]]:
                        break
                    i += 1
                for next_symbol in nss:
                    for ex_prod_id, ex_prod in enumerate(self.productions):
                        if ex_prod.get(cur) is not None:
                            new_item = (ex_prod_id, 0, next_symbol)
                            if new_item not in some_items:
                                some_items.append(new_item)
        return some_items

    # goto函数  a 输入字符
    def goto(self, some_items, a):
        ans = []
        for (i, j, k) in some_items:
            production = self.lr1_productions[i]
            if j + 1 < len(production):
                cur = production[j + 1]
                if cur == a:
                    new_item = (i, j + 1, k)
                    if new_item not in ans:
                        ans.append(new_item)
        return self.closure(ans)

    def init_lr1grammar(self):
        self.dic2list()

    @staticmethod
    def prod2str(prod, dotpos):
        prod = prod[:]
        prod.append("")
        prod[dotpos + 1] = ' · ' + prod[dotpos + 1]
        return prod[0] + ' ->' + ''.join(prod[1:])

    def generate_items(self):
        f = open('lr1_items.txt', 'w')
        self.term = sorted(self.term, key=str.lower)
        self.nterm = sorted(self.nterm, key=str.lower)
        self.lr1_analyze_table = [{}]
        I0 = self.closure([(0, 0, '#')])  # I0 正确
        cc = [I0]  # 项目集规范族
        i = 0
        while i < len(cc):
            ccc = {}
            for j in cc[i]:
                ccc[(j[0], j[1])] = j[2]  # ( j[0] 产生式ID j[1] dot_position)
            ccc = [[i[0], i[1], j] for i, j in ccc.items()]
            print("[I%d]:\n  " % i,
                  '\n   '.join(self.prod2str(self.lr1_productions[j[0]], j[1]) + ' \t' + j[2] for j in ccc),
                  end="\n   ", file=f)
            candiwords = []  # goto的转移的输入字符
            for j in cc[i]:  # I[i]
                prod = self.lr1_productions[j[0]]
                dot_pos = j[1] + 1
                if dot_pos < len(prod) and prod[dot_pos] not in candiwords:
                    candiwords.append(prod[dot_pos])
                if dot_pos == len(prod):
                    if prod[0] != "root":
                        self.lr1_analyze_table[i][j[2]] = 'r%d' % j[0]  # 规约项目
                    else:
                        self.lr1_analyze_table[i]['#'] = 'acc'  # 接受项目
            for j in candiwords:
                tmp = self.goto(cc[i], j)  # tmp 新生成的项目族
                if len(tmp) > 0 and tmp not in cc:
                    cc.append(tmp)
                    self.lr1_analyze_table.append({})
                if len(tmp) > 0:
                    if j in self.term:
                        self.lr1_analyze_table[i][j] = "s%d" % cc.index(tmp)  # 移进项目
                    else:
                        self.lr1_analyze_table[i][j] = "%d" % cc.index(tmp)  # goto
            i += 1
            print("\033[0m", file=f)
        self.analysis_table()
        f.close()

    def analysis_table(self):
        f = open('lr1_analysis_table.txt', 'w')
        head = ['I']
        for j in self.term:
            head.append(j)
        for j in self.nterm:
            if j == "root":
                continue
            head.append(j)
        # txt print
        print('---'.join('' + '-' * 30 for _ in head), file=f)
        print(' | '.join(i + ' ' * (30 - len(i)) for i in head), file=f)
        print('-+-'.join('' + '-' * 30 for _ in head), file=f)
        # excel print
        mystyle = title_style()
        workbook = xlwt.Workbook(encoding='ascii')
        worksheet = workbook.add_sheet('demo')
        for i, element in enumerate(head):
            worksheet.write(0, i, element, mystyle)
        for i, line in enumerate(self.lr1_analyze_table):
            lo = [str(i)]
            for j in self.term:
                if j in line.keys():
                    lo.append(self.lr1_analyze_table[i][j])
                else:
                    lo.append("")
            for j in self.nterm:
                if j == "root":
                    continue
                if j in line.keys():
                    lo.append(self.lr1_analyze_table[i][j])
                else:
                    lo.append("")
            print(' | '.join(i + ' ' * (30 - len(i)) for i in lo), file=f)
            for ind, e in enumerate(lo):
                worksheet.write(i + 1, ind, e, mystyle)
        f.close()
        workbook.save('lr1_analysis_table.xls')


class parse_grammar(lr1_grammar):
    def __init__(self):
        super().__init__()
        self.tokens = []
        self.tokens_str = []
        self.stack_token = ['#']
        self.stack_state = [0]
        self.cur_token = '#'
        self.cur_state = 0
        self.input_ptr = 0
        self.last_token = '#'
        self.dollar_flg = 0
        self.par_seq = 0
        self.f = open('lr1_parse_sequence.txt', 'w')
        self.f2 = open('33gra.tsv', 'w')
        self.par_times = 1

    def init_parser(self, filename):
        for line in open(filename, "r"):
            line = line[:-1]
            if line != '#':
                self.tokens.append(line)
            else:
                print("times is :%d !!!" % self.par_times)
                # print(self.tokens)
                print("times is :%d !!!\n" % self.par_times, self.tokens, file=self.f)
                self.tokens.append("#")
                self.syntax_parser()
                self.tokens = []

    def syntax_parser(self):
        self.par_times += 1
        self.input_ptr = 0
        self.stack_token = ['#']
        self.stack_state = [0]
        self.dollar_flg = 0
        self.par_seq = 0
        while len(self.stack_token) > 0:
            print("\tstack_token", self.stack_token, file=self.f)
            print("\tcur_str", self.tokens[self.input_ptr:], file=self.f)
            self.cur_token = self.tokens[self.input_ptr]
            self.cur_state = self.stack_state[-1]
            if self.dollar_flg:
                self.cur_token = self.last_token
            if self.cur_token not in self.lr1_analyze_table[self.cur_state].keys():
                if self.lr1_analyze_table[self.cur_state].get('$') is not None:
                    self.last_token = self.cur_token
                    self.dollar_flg = 1
                    action = self.lr1_analyze_table[self.cur_state]['$']
                    self.cur_token = '$'
                    rst = self.stack_action(action)
                    if rst == 0:
                        break
                else:
                    print("\terror!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("error\n\n", file=self.f)
                    print("error", file=self.f2)
                    break
            else:
                self.par_seq += 1
                self.dollar_flg = 0
                action = self.lr1_analyze_table[self.cur_state][self.cur_token]
                rst = self.stack_action(action)
                if rst == 0:
                    break

    def stack_action(self, action):
        if self.dollar_flg == 1:
            face_token = self.last_token
        else:
            face_token = self.cur_token
        ptr = -1
        while self.stack_token[ptr] == '$':
            ptr -= 1
        if action == "acc":
            if self.dollar_flg == 0:
                # print
                print("\t---------------------------------accept----------------------------------")
                print("%d\t1\t%s#%s" % (self.par_seq, self.stack_token[ptr], face_token), "\taccept\n\n", file=self.f)
                #   # print multiple test
                # print("%d\t1\t%s#%s\treduction" % (self.par_seq, self.stack_token[ptr], face_token), file=self.f2)
                # print("%d\t/\troot##\taccept" % (self.par_seq + 1), file=self.f2)
                # print single real version
                print("%d\t1\t%s#%s\treduction" % (self.par_seq, self.stack_token[ptr], face_token), file=self.f2)
                print("%d\t/\troot##\taccept" % (self.par_seq + 1), file=self.f2, end="")
            return 0
        elif action[0] == 's':
            if self.dollar_flg == 0:
                # print to txt
                print("%d\t/\t%s#%s" % (self.par_seq, self.stack_token[ptr], face_token), "\tmove", file=self.f)
                # print to tsv
                print("%d\t/\t%s#%s\tmove" % (self.par_seq, self.stack_token[ptr], face_token), file=self.f2)
            next_state = int(action[1:])
            self.stack_token.append(self.cur_token)
            self.stack_state.append(next_state)
            if self.dollar_flg == 0:
                self.input_ptr += 1
            return 1
        else:
            prod_id = int(action[1:])
            prod_len = len(self.lr1_productions[prod_id]) - 1
            if self.dollar_flg == 0:
                # print to txt
                print("%d\t%d\t%s#%s" % (self.par_seq, prod_id + 1, self.stack_token[ptr], face_token), "\treduction",
                      "%s -> " % self.lr1_productions[prod_id][0], "  ".join(self.lr1_productions[prod_id][1:]),
                      file=self.f)
                # print to tsv
                print("%d\t%d\t%s#%s\treduction" % (self.par_seq, prod_id + 1, self.stack_token[ptr], face_token),
                      file=self.f2)
            self.stack_token = self.stack_token[:-prod_len]
            self.stack_state = self.stack_state[:-prod_len]
            self.cur_state = self.stack_state[-1]
            goto_nt = self.lr1_productions[prod_id][0]
            if goto_nt not in self.lr1_analyze_table[self.cur_state].keys():
                print("error\n\n", file=self.f)
                print("error", file=self.f2)
                print("error！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！")
                return 0
            next_state = int(self.lr1_analyze_table[self.cur_state][goto_nt])
            self.stack_token.append(goto_nt)
            self.stack_state.append(next_state)
            return 1


def main(filename):
    g = parse_grammar()
    g.init_grammar('grammar.txt')
    g.init_lr1grammar()
    g.generate_items()
    g.init_parser(filename)


if __name__ == "__main__":
    main('token.txt')
