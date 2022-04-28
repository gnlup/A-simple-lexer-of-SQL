# 初始化
class grammar:
    # 定义
    def __init__(self):
        self.first_set = {}  # first集：字典嵌套子典
        self.productions = []  # 产生式：列表
        self.term = set()  # 终结符：集合类型
        self.nterm = set()  # 非终结符：集合类型
        self.all_term = set()  # term+nterm：集合类型
        self.productions_dict = {}  # 产生式key字典
        self.lr1_analyze_table = {}  # 分析表：字典

    # 读取txt，转换为产生式
    def read_grammar(self, file_name):
        for line in open(file_name, 'r'):
            line = line[:-1]
            left = line.split(' -> ')[0]
            right = line.split(' -> ')[1]
            right_list = []
            right.strip(' ')
            if right.find(' ') == -1:
                right_list.append(right)
            else:
                right_list += right.split(' ')
            production = {left: right_list}
            self.productions.append(production)
        for every in self.productions:
            print(every)

    # 获取终结符集和非终结符集
    def get_termornot(self):
        for production in self.productions:
            for left in production.keys():
                if left not in self.productions_dict:
                    self.productions_dict[left] = []
                self.productions_dict[left].append((
                    tuple(production[left]),
                    self.productions.index(production)))
                self.all_term.add(left)
                self.nterm.add(left)
                for right in production[left]:
                    self.all_term.add(right)
        self.term = self.all_term - self.nterm
        print('term:\n', self.term)
        print('nterm:\n', self.nterm)

    # def termornot(self):
    #     pass

    # 获取first集 (抄的还没改
    def get_firstset(self, status, all_term):
            if status in self.first_set:
                 return self.first_set[status]
          all_term.add(status)
          cur_status_set = set()
          for right_list in self.productions_dict[status]:
              for right in right_list[0]:
                  right_set = None
                  if right in all_term:
                      continue
                  if right in self.first_set:
                      right_set = self.first_set[right]
                  else:
                      right_set = self.get_firstset(right, all_term)
                  cur_status_set |= right_set
                  if '$' not in right_set:
                      break
          return cur_status_set
        # pass
      def init_firstset(self):
          for term in self.term:
              self.first_set[term] = {term}
          for nterm in self.nterm:
              self.first_set[nterm] = self.get_firstset(nterm, set())
          print('firstset:\n', self.first_set)

    # 构造项目集规范族
       def generate_items(self):
        items=items[:]
        for (prod_id, dot_pos, ahead) in self.items:
            prod =self.productions[prod_id]
            if dot_pos + 1 < len(prod):
                cur = prod[dot_pos + 1]
                nss = []
                tmpseq = prod[dot_pos + 2:] + [ahead] # next_symbol = prod[dot_pos+2] if dot_pos+2 < len(prod) else ahead
                i = 0
                #first['$'] = ['$']
                while i < len(tmpseq):
                    for x in self.first_set[tmpseq[i]]:
                        if (x != '$' or tmpseq[i] == '$') and x not in nss:
                            nss.append(x)
                    if '$' not in self.first_set[tmpseq[i]]:
                        break
                    i += 1
                for next_symbol in nss:
                    for ex_prod_id, ex_prod in enumerate(self.productions):
                        if ex_prod[0] == cur:
                            new_item = (ex_prod_id, 0, next_symbol)
                            if new_item not in self.items:
                                self.items.append(new_item)
         return self.items

    # 构造DFA
    def DFA(self):
        pass

    # 构造分析表
    def analysis_table(self):
        pass

    def print_table(self):
        pass

    # class parse_grammar:
    def syntax_parser(self):
        pass


def main():
    g = grammar()
    g.read_grammar('grammar_simple.txt')
    g.get_termornot()
    g.init_firstset()
    # g.get_firstset()
    # g.generate_items()
    # g.DFA()
    # g.analysis_table()


if __name__ == "__main__":
    main()
