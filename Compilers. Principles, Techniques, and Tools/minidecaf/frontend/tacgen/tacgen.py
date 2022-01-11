from frontend.ast import node
from frontend.ast.tree import *
from frontend.ast.visitor import Visitor
from utils.tac import tacop
from utils.tac.funcvisitor import FuncVisitor
from utils.tac.programwriter import ProgramWriter
from utils.tac.tacprog import TACProg, GlobalVarInfo

"""
The TAC generation phase: translate the abstract syntax tree into three-address code.
"""


# step-8 add visitFor, visitDowhile,visitContinue

class TACGen(Visitor[FuncVisitor, None]):
    def __init__(self) -> None:
        pass

    # Entry of this phase
    def transform(self, program: Program) -> TACProg:
        glob_var = []
        for name, decl in program.variables_list():
            if decl.var_t.type.is_array():
                glob_var.append(GlobalVarInfo(name, decl.var_t.type.size, None))
            elif isinstance(decl.init_expr, IntLiteral):
                glob_var.append(GlobalVarInfo(name, 4, decl.init_expr.value))
            else:
                glob_var.append(GlobalVarInfo(name, 4, 0))

        mainFunc = program.mainFunc()
        pw = ProgramWriter(program.functions().keys(), glob_var)
        # The function visitor of 'main' is special.
        mv = pw.visitMainFunc()

        mainFunc.body.accept(self, mv)
        # Remember to call mv.visitEnd after the translation a function.
        mv.visitEnd()

        for ident, func in program.functions_list():
            if ident == 'main' or func.body == NULL:
                continue
            # Clear global var addr & value temp
            for name, decl in program.variables_list():
                symbol = decl.getattr('symbol')
                symbol.temp = None
                symbol.addr = None
            func_para_num = len(func.para)
            mv = pw.visitFunc(ident, func_para_num)
            func.accept(self, mv)
            mv.visitEnd()

        # Remember to call pw.visitEnd before finishing the translation phase.
        return pw.visitEnd()

    def visitFunction(self, func: Function, mv: FuncVisitor) -> None:
        for index, para in enumerate(func.para):
            para.accept(self, mv)
            para.getattr("symbol").temp.para_id = index
        func.body.accept(self, mv)

    def visitParameter(self, para: Parameter, mv: FuncVisitor) -> None:
        para.getattr("symbol").temp = mv.freshTemp()

    def visitCall(self, expr: FuncCall, mv: FuncVisitor) -> None:
        for index, para in enumerate(expr.para):
            para.accept(self, mv)
        for index, para in enumerate(expr.para):
            mv.visitSetupPara(para.getattr("val"), len(expr.para) - index)
        expr.setattr("val", mv.visitCall(mv.ctx.getFuncLabel(expr.func.value), mv.freshTemp(), len(expr.para)))

    def visitBlock(self, block: Block, mv: FuncVisitor) -> None:
        for child in block:
            child.accept(self, mv)

    def visitReturn(self, stmt: Return, mv: FuncVisitor) -> None:
        stmt.expr.accept(self, mv)
        mv.visitReturn(stmt.expr.getattr("val"))

    def visitBreak(self, stmt: Break, mv: FuncVisitor) -> None:
        mv.visitBranch(mv.getBreakLabel())

    def visitIdentifier(self, ident: Identifier, mv: FuncVisitor) -> None:
        """
        1. Set the 'val' attribute of ident as the temp variable of the 'symbol' attribute of ident.
        """
        var = ident.getattr('symbol')
        if var.isGlobal:
            if var.addr is None:
                var.addr = mv.freshTemp()
                mv.visitLoadAddress(var.addr, ident.value)
            if var.temp is None:
                var.temp = mv.freshTemp()
            mv.visitLoad(var.temp, var.addr, 0)
        ident.setattr('val', var.temp)

    def visitDeclaration(self, decl: Declaration, mv: FuncVisitor) -> None:
        """
        1. Get the 'symbol' attribute of decl.
        2. Use mv.freshTemp to get a new temp variable for this symbol.
        3. If the declaration has an initial value, use mv.visitAssignment to set it.
        """
        t = mv.freshTemp()
        decl.getattr('symbol').temp = t
        if decl.init_expr != NULL:
            decl.init_expr.accept(self, mv)
            mv.visitAssignment(t, decl.init_expr.getattr('val'))

    def visitAssignment(self, expr: Assignment, mv: FuncVisitor) -> None:
        """
        1. Visit the right hand side of expr, and get the temp variable of left hand side.
        2. Use mv.visitAssignment to emit an assignment instruction.
        3. Set the 'val' attribute of expr as the value of assignment instruction.
        """
        expr.rhs.accept(self, mv)

        if isinstance(expr.lhs, ArrayRef):
            arr: ArrayRef = expr.lhs
            arr.accept(self, mv)
            mv.visitStore(expr.rhs.getattr('val'), arr.getattr('addr'), 0)
        else:
            var = expr.lhs.getattr('symbol')
            if var.isGlobal:
                if var.addr is None:
                    var.addr = mv.freshTemp()
                    mv.visitLoadAddress(var.addr, expr.lhs.value)
                if var.temp is None:
                    var.temp = mv.freshTemp()
                mv.visitStore(expr.rhs.getattr('val'), var.addr, 0)
            mv.visitAssignment(var.temp, expr.rhs.getattr('val'))

        expr.setattr('val', expr.rhs.getattr('val'))

    def visitIf(self, stmt: If, mv: FuncVisitor) -> None:
        stmt.cond.accept(self, mv)

        if stmt.otherwise is NULL:
            skipLabel = mv.freshLabel()
            mv.visitCondBranch(
                tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), skipLabel
            )
            stmt.then.accept(self, mv)
            mv.visitLabel(skipLabel)
        else:
            skipLabel = mv.freshLabel()
            exitLabel = mv.freshLabel()
            mv.visitCondBranch(
                tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), skipLabel
            )
            stmt.then.accept(self, mv)
            mv.visitBranch(exitLabel)
            mv.visitLabel(skipLabel)
            stmt.otherwise.accept(self, mv)
            mv.visitLabel(exitLabel)

    def visitWhile(self, stmt: While, mv: FuncVisitor) -> None:
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()
        mv.openLoop(breakLabel, loopLabel)

        mv.visitLabel(beginLabel)
        stmt.cond.accept(self, mv)
        mv.visitCondBranch(tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), breakLabel)

        stmt.body.accept(self, mv)
        mv.visitLabel(loopLabel)
        mv.visitBranch(beginLabel)
        mv.visitLabel(breakLabel)
        mv.closeLoop()

    def visitDoWhile(self, stmt: DoWhile, mv: FuncVisitor) -> None:
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()
        mv.openLoop(breakLabel, loopLabel)

        mv.visitLabel(beginLabel)
        stmt.body.accept(self, mv)

        mv.visitLabel(loopLabel)
        stmt.cond.accept(self, mv)
        mv.visitCondBranch(tacop.CondBranchOp.BNE, stmt.cond.getattr("val"), beginLabel)

        mv.visitLabel(breakLabel)
        mv.closeLoop()

    def visitFor(self, stmt: For, mv: FuncVisitor) -> None:
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()
        mv.openLoop(breakLabel, loopLabel)
        # init
        if not stmt.init is NULL:
            stmt.init.accept(self, mv)
        # loop
        mv.visitLabel(beginLabel)
        if not stmt.cond is NULL:
            stmt.cond.accept(self, mv)
            mv.visitCondBranch(tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), breakLabel)

        stmt.body.accept(self, mv)
        mv.visitLabel(loopLabel)

        if not stmt.update is NULL:
            stmt.update.accept(self, mv)

        mv.visitBranch(beginLabel)
        # exit
        mv.visitLabel(breakLabel)
        mv.closeLoop()

    def visitContinue(self, stmt: Continue, mv: FuncVisitor) -> None:
        mv.visitBranch(mv.getContinueLabel())

    def visitUnary(self, expr: Unary, mv: FuncVisitor) -> None:
        expr.operand.accept(self, mv)

        op = {
            node.UnaryOp.Neg: tacop.UnaryOp.NEG,
            node.UnaryOp.BitNot: tacop.UnaryOp.NOT,
            node.UnaryOp.LogicNot: tacop.UnaryOp.SEQZ,
        }[expr.op]
        expr.setattr("val", mv.visitUnary(op, expr.operand.getattr("val")))

    def visitBinary(self, expr: Binary, mv: FuncVisitor) -> None:

        expr.lhs.accept(self, mv)
        expr.rhs.accept(self, mv)
        op = {
            node.BinaryOp.Add: tacop.BinaryOp.ADD,
            node.BinaryOp.Sub: tacop.BinaryOp.SUB,
            node.BinaryOp.Mul: tacop.BinaryOp.MUL,
            node.BinaryOp.Div: tacop.BinaryOp.DIV,
            node.BinaryOp.Mod: tacop.BinaryOp.REM,

            node.BinaryOp.LT: tacop.BinaryOp.SLT,
            node.BinaryOp.GT: tacop.BinaryOp.SGT,

            node.BinaryOp.LogicOr: tacop.BinaryOp.OR,
            node.BinaryOp.LogicAnd: tacop.BinaryOp.AND,

            node.BinaryOp.EQ: tacop.BinaryOp.EQ_HELP,
            node.BinaryOp.NE: tacop.BinaryOp.NE_HELP,

            node.BinaryOp.LE: tacop.BinaryOp.LE_HELP,

            node.BinaryOp.GE: tacop.BinaryOp.GE_HELP,

            # You can add binary operations here.
        }[expr.op]
        expr.setattr(
            "val", mv.visitBinary(op, expr.lhs.getattr("val"), expr.rhs.getattr("val"))
        )

    def visitCondExpr(self, expr: ConditionExpression, mv: FuncVisitor) -> None:
        """
        1. Refer to the implementation of visitIf and visitBinary.
        """
        exitLabel = mv.freshLabel()
        skipLabel = mv.freshLabel()
        expr.cond.accept(self, mv)
        mv.visitCondBranch(tacop.CondBranchOp.BEQ, expr.cond.getattr('val'), skipLabel)
        expr.then.accept(self, mv)
        t = mv.freshTemp()
        mv.visitAssignment(t, expr.then.getattr('val'))
        mv.visitBranch(exitLabel)
        mv.visitLabel(skipLabel)
        expr.otherwise.accept(self, mv)
        mv.visitAssignment(t, expr.otherwise.getattr('val'))
        expr.setattr('val', t)
        mv.visitLabel(exitLabel)

    def visitIntLiteral(self, expr: IntLiteral, mv: FuncVisitor) -> None:
        expr.setattr("val", mv.visitLoadImm4(expr.value))

    def visitArrayRef(self, arr: ArrayRef, mv: FuncVisitor) -> None:
        var = arr.getattr('symbol')

        # Load array base address
        if var.addr is None:
            var.addr = mv.freshTemp()
            if var.isGlobal:
                mv.visitLoadAddress(var.addr, arr.value)
            else:
                mv.visitAlloc(var.addr, var.type.size)

        # Calculate element address
        arr_type = var.type
        idx_temp = mv.freshTemp()
        mv.visitAssignment(idx_temp, var.addr)
        for idx in arr.indexes:
            arr_type = arr_type.base
            idx.accept(self, mv)
            dim_size = mv.visitLoadImm4(arr_type.size)
            mv.visitBinarySelf(tacop.BinaryOp.MUL, dim_size, idx.getattr('val'))
            mv.visitBinarySelf(tacop.BinaryOp.ADD, idx_temp, dim_size)
        arr.setattr('addr', idx_temp)

    def visitArrayExpr(self, arr: ArrayExpr, mv: FuncVisitor) -> None:
        arr.array.accept(self, mv)

        value = mv.freshTemp()
        mv.visitLoad(value, arr.array.getattr('addr'), 0)
        arr.setattr('val', value)
