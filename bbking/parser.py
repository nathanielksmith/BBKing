
import ply.yacc as yacc

from lexer import tokens

class Tagged(object):
    def __init__(self, name, contents, arg=None, **kwargs): 
        self.name = name
        self.contents = contents
        self.arg = arg
        self.kwargs = kwargs

def p_main(p):
    '''content : content tagged
               | content untagged
               | empty
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_tagged(p):
    '''tagged : opentag content closetag'''
    name, arg, kwargs = p[1]
    if name != p[3]:
        raise SyntaxError, "Unbalanced tags: [%s] [/%s]"%(name, p[3])
    p[0] = Tagged(name, p[2], arg, **kwargs)

def p_untagged(p):
    '''untagged : SYMBOL
                | WHITESPACE
                | MISC
                | RBRACKET
                | EQ
                | SLASH
    '''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_text(p):
    '''text : text term 
            | term
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_term(p):
    '''
       term : WHITESPACE 
            | SYMBOL
            | MISC
    '''
    p[0] = p[1]

def p_term_no_ws(p):
    ''' term_no_ws : SYMBOL
                   | MISC
    '''
    p[0] = p[1]

def p_close_tag(p):
    'closetag : LBRACKET SLASH SYMBOL RBRACKET'
    p[0] = p[3]

def p_simple_tag(p):
    'opentag : LBRACKET SYMBOL RBRACKET'
    p[0] = (p[2], None, {})

def p_single_arg_tag(p):
    'opentag : LBRACKET SYMBOL EQ text RBRACKET'
    p[0] = (p[2], p[4], {})

def p_multi_arg_tag(p):
    'opentag : LBRACKET SYMBOL WHITESPACE args RBRACKET'
    p[0] = (p[2], None, p[4])

def p_tag_args(p):
    '''args : args WHITESPACE arg
            | arg
    '''
    if len(p) == 4:
        key,value = p[3]
        p[0] = dict(p[1],**{ key : value})
    else:
        key,value = p[1]
        p[0] = { key : value }

def p_tag_arg(p):
    'arg  : SYMBOL EQ term_no_ws'
    p[0] = (p[1],p[3])

def p_error(p):
    # ignore errors for now simply don't run bbcode if it does not parse
    pass 

parser = yacc.yacc()