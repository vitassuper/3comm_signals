from Parser.Nodes.AstNode import ASTNode


class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode) -> None:
        self.left: ASTNode = left
        self.op: str = op
        self.right: ASTNode = right
