version--读取一个文件版

输入文件：

	token.txt//词法处理后终结符的序列，最后有一个#和空行！！
	
	grammar.txt//指导书给的语法表
输出文件：

	lr1_grammar_information.txt//first集合，终结符集，非终结符集 production_dict是从0开始的
	
	lr1_items.txt//项目集规范族
	
	lr1_analysis_table.xls//excel版分析表 pip install xlwt
	
	lr1_analysis_table.txt//txt版分析
	
	lr1_parse_sequence.txt//分析的完整过程，debug使用
	
	33gra.tsv//老师要的文件，规约序列，pycharm插件csv plugin可以查看原版格式，体验更好o~~~


----------------------------------------------模块--------------------------------------------------------
syntax_parser文件:

grammar: 

	语法类，对语法处理，获得first，终结符集非终结符集
lr1_grammar: 

	grammar子类，
	closure函数，
	goto函数，
	项目集规范族，
	lr1分析表
parse_grammar:

    lr1_grammar子类，
    分析过程，
    输出文件；


​	