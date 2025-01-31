from lark import Lark, Tree, Token, Visitor
import sys

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from . import static  # Read and interpret grammar file.
from .exceptions import SoottyError


class Prune(Visitor):
    """Visitor class used to prune the parse tree to make it easier to interpret."""

    def binexp(self, tree):
        if len(tree.children) == 1:
            tree.data = tree.children[0].data
            tree.children = tree.children[0].children
        else:
            if type(tree.children[1] is Tree):
                tree.data = tree.children[1].children[0]
            else:
                tree.data = tree.children[1]
            tree.children = [tree.children[0], tree.children[2]]

    def expr(self, tree):
        self.binexp(tree)

    def lexp(self, tree):
        self.binexp(tree)

    def rexp(self, tree):
        self.binexp(tree)

    def bexp(self, tree):
        self.binexp(tree)

    def sexp(self, tree):
        self.binexp(tree)

    def aexp(self, tree):
        self.binexp(tree)

    def mexp(self, tree):
        self.binexp(tree)

    def wire(self, tree):
        if len(tree.children) == 1:
            if type(tree.children[0]) is Tree:
                tree.data = tree.children[0].data
                tree.children = tree.children[0].children
        elif len(tree.children) == 2:
            if type(tree.children[0]) is Tree:
                tree.data = tree.children[0].children[0]
                tree.children = [tree.children[1]]
            elif type(tree.children[0]) is Token:
                tree.data = tree.children[0]
                tree.children = [tree.children[1]]
        elif len(tree.children) == 3:
            tree.data = tree.children[1].children[0]
            tree.children = [tree.children[0], tree.children[2]]


class ExpressionParser(Lark):
    """Implementation of Lark parser class for limit expressions."""

    def __init__(self):
        grammar = pkg_resources.open_text(static, "grammar.lark").read()
        super().__init__(grammar, start=["expr", "exprs"])

    def parse(self, expression: str):
        tree = super().parse(expression, start="expr")
        tree = Prune().visit(tree)
        # print(self.tree.pretty(), file=sys.stderr)
        return tree

    def parse_list(self, expressions: str):
        tree = super().parse(expressions, start="exprs")
        tree = Prune().visit(tree)
        return tree.children


parser = ExpressionParser()  # initialize global parser object

def parameter_query(parameter_query, config):
    key_values = parameter_query.replace('\n', '').split(':')

    for key_value in key_values:
        if key_value[0][0] == 's': #start= 0 1 2 3 4 5
            config.set_user_start(int(key_value[6:len(key_value)]))
        elif key_value[0][0] == 'e': #end= 0 1 2 3
             config.set_user_end(int(key_value[4:len(key_value)]))
        elif key_value[0][0] == 'v': #visible_wires 0 1 2 3 4 5 6 7 8 9 10 11 12 13
             val = key_value[14:len(key_value)]
             config.set_visible_wires(val.split(','))

    return config


