import pygraphviz as pgv

from Parser.Nodes.Literal import Literal
from Parser.Operators.ArithmeticOp import ArithmeticOp
from Parser.Operators.BinaryOp import BinaryOp
from Parser.Operators.ComparisonOp import ComparisonOp


def ast_to_dot(ast, dot=None, parent_id=None):
    if dot is None:
        dot = pgv.AGraph(strict=False, directed=True)

    node_id = str(id(ast))

    if (
        isinstance(ast, BinaryOp)
        or isinstance(ast, ComparisonOp)
        or isinstance(ast, ArithmeticOp)
    ):
        name = ast.op
    elif isinstance(ast, Literal):
        name = ast.value
    else:
        name = ast.name

    label = f'{ast.__class__.__name__} {name}'
    dot.add_node(node_id, label=label)

    if parent_id is not None:
        dot.add_edge(parent_id, node_id)

    if (
        isinstance(ast, BinaryOp)
        or isinstance(ast, ComparisonOp)
        or isinstance(ast, ArithmeticOp)
    ):
        ast_to_dot(ast.left, dot, node_id)
        ast_to_dot(ast.right, dot, node_id)
    return dot


def visualize_ast(ast, name: str = 'ast.png') -> None:
    dot = ast_to_dot(ast)
    dot.draw(name, format='png', prog='dot')
