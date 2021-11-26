import ply.yacc as yacc
import ply.lex as lex

class Parser(object):

    reservedWordDict = {
        'bool': 'BOOL',
        'true': 'TRUE',
        'false': 'FALSE',
        'and': 'AND',
        'or': 'OR',
        'if': 'IF',
        'elif': 'ELIF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'do': 'DO',
        'int': 'INT',
        'float': 'FLOAT',
        'string': 'STRING',
        'print': 'PRINT'
    }

    tokens = tuple(['ID', 'FLOAT_VAL', 'INT_VAL', 'STR_VAL', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EXP', 'ASSIGN', 'NOT_EQUALS',
                    'EQ_MORE', 'EQ_LESS', 'MORE', 'LESS', 'EQUALS', 'LPAREN', 'RPAREN', 'LKEY', 'RKEY', 'FINISH'] + list(reservedWordDict.values()))

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_EXP = r'\^'
    t_ASSIGN = r'='
    t_EQUALS = r'=='
    t_NOT_EQUALS = r'!='
    t_EQ_MORE = r'>='
    t_EQ_LESS = r'<='
    t_MORE = r'>'
    t_LESS = r'<'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LKEY = r'{'
    t_RKEY = r'}'
    t_FINISH = r';'
    t_ignore = ' \t'

    precedence = (
        ('left', 'AND', 'OR'),
        ('nonassoc', 'EQUALS', 'NOT_EQUALS', 'EQ_MORE', 'EQ_LESS', 'MORE', 'LESS'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIV'),
        ('left', 'EXP'),
        ('right', 'UMINUS'),  
    )

    commands = ()

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def t_FLOAT_VAL(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t


    def t_INT_VAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t


    def t_STR_VAL(self, t):
        r'\"[^\n]+\"'
        t.value = t.value.replace("\"", "")
        return t


    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reservedWordDict.get(t.value, 'ID')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '{}'".format(t.value[0]))
        t.lexer.skip(1)

    def p_start(self, p):
        '''start : statement'''
        self.commands = p[1]


    def p_statement(self, p):
        '''statement : print_stmt FINISH statement
                    | register_stmt FINISH statement
                    | condition_stmt statement
                    | for_stmt statement
                    | while_stmt statement
                    | empty'''
        if len(p) > 2:
            if p[2] == ';':
                p[2] = p[3]
            p[0] = (p[1],) + p[2]
        else:
            p[0] = ()


    def p_expression_operation(self, p):
        '''expression : expression AND expression
                    | expression OR expression
                    | expression PLUS expression
                    | expression MINUS expression
                    | expression MULT expression
                    | expression DIV expression
                    | expression EXP expression
                    | expression EQUALS expression
                    | expression NOT_EQUALS expression
                    | expression EQ_MORE expression
                    | expression EQ_LESS expression
                    | expression MORE expression
                    | expression LESS expression'''
        p[0] = ('operation', p[1], p[2], p[3])


    def p_expression_id(self, p):
        "expression : ID"
        p[0] = p[1]


    def p_expression_val(self, p):
        '''expression : FLOAT_VAL
                    | INT_VAL
                    | STR_VAL
                    | bool_val'''
        p[0] = p[1]


    def p_bool_val(self, p):
        '''bool_val : TRUE
                | FALSE'''
        if p[1] == "true":
            p[0] = True
        elif p[1] == "false":
            p[0] = False


    def p_expression_parenthesis(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]


    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]


    def p_print_stmt(self, p):
        'print_stmt : PRINT expression'
        p[0] = ('print', p[2])


    def p_register_stmt(self, p):
        '''register_stmt : declare_reg
                | declare_assign_reg
                | assign_reg'''
        p[0] = p[1]


    def p_condition_stmt(self, p):
        '''condition_stmt : if_cond elif_cond else_cond'''
        p[0] = ('condition', p[1], p[2], p[3])


    def p_for_stmt(self, p):
        '''for_stmt : FOR LPAREN declare_assign_reg FINISH expression FINISH assign_reg RPAREN LKEY statement RKEY'''
        p[0] = ('for', p[3], p[5], p[7], p[10])


    def p_while_stmt(self, p):
        '''while_stmt : WHILE LPAREN expression RPAREN LKEY statement RKEY
                    | DO LKEY statement RKEY WHILE LPAREN expression RPAREN FINISH'''
        if p[1] == "while":
            p[0] = ('while', p[3], p[6])
        else:
            p[0] = ('do-while', p[7], p[3])


    def p_empty(self, p):
        'empty :'
        pass


    def p_type(self, p):
        '''type : BOOL
            | INT
            | FLOAT
            | STRING'''
        p[0] = p[1]


    def p_declare_reg(self, p):
        '''declare_reg : type ID'''
        p[0] = ('declare', p[1], p[2])


    def p_declare_assign_reg(self, p):
        '''declare_assign_reg : type ID ASSIGN expression'''
        p[0] = ('declare_assign', p[1], p[2], p[4])


    def p_assign_reg(self, p):
        '''assign_reg : ID ASSIGN expression'''
        p[0] = ('assign', p[1], p[3])


    def p_if_cond(self, p):
        '''if_cond : IF LPAREN expression RPAREN LKEY statement RKEY'''
        p[0] = ('if', p[3], p[6])


    def p_elif_cond(self, p):
        '''elif_cond : ELIF LPAREN expression RPAREN LKEY statement RKEY elif_cond
                    | empty'''
        if len(p) > 2:
            p[0] = (('elif', p[3], p[6]), ) + p[8]
        else:
            p[0] = ()


    def p_else_cond(self, p):
        '''else_cond : ELSE LKEY statement RKEY
                    | empty'''
        if len(p) > 2:
            p[0] = ('else', p[3])


    def p_error(self, p):
        if p:
            print("Syntax error at '{}'".format(p.value))
        else:
            print("Syntax error at EOF")

    def parse(self, file_path:str = "input.txt"):
        file = open(file_path, "r")
        s = file.read()
        file.close()
        self.parser.parse(s)
