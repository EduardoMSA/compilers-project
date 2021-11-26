import ply.lex as lex

class Lexer(object):

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

    def __init__(self):
        self.lexer = lex.lex(module=self)

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
