from frontend.ast.tree import *
from frontend.ast.visitor import Visitor
from frontend.scope.globalscope import GlobalScope
from frontend.scope.scope import Scope, ScopeKind
from frontend.scope.scopestack import ScopeStack
from frontend.symbol.funcsymbol import FuncSymbol
from frontend.symbol.varsymbol import VarSymbol
from utils.error import *
from utils.riscv import MAX_INT

"""
The namer phase: resolve all symbols defined in the abstract syntax tree and store them in symbol tables (i.e. scopes).
"""


# step-8 :add visitDoWhile , visitFor, visitContinue


class Namer(Visitor[ScopeStack, None]):

    def __init__(self) -> None:
        pass

    # Entry of this phase
    def transform(self, program: Program) -> Program:
        # Global scope. You don't have to consider it until Step 9.
        program.globalScope = GlobalScope
        ctx = ScopeStack(program.globalScope)

        program.accept(self, ctx)
        return program

    def visitProgram(self, program: Program, ctx: ScopeStack) -> None:
        # Check if the 'main' function is missing
        if not program.hasMainFunc():
            raise DecafNoMainFuncError

        for ident, decl in program.variables_list():
            decl.accept(self, ctx)

        for ident, func in program.functions_list():
            func.accept(self, ctx)

        # program.mainFunc().accept(self, ctx)

    def visitFunction(self, func: Function, ctx: ScopeStack) -> None:
        if ctx.findConflict(func.ident.value):
            raise DecafDeclConflictError(func.ident.value)
        func_symbol = FuncSymbol(True, func.ident.value, func.ret_t.type, ctx.currentScope())
        ctx.declare(func_symbol)
        for para in func.para:
            func_symbol.addParaType(para.var_t)

        ctx.open(Scope(ScopeKind.LOCAL))
        # add paras
        for para in func.para:
            para.accept(self, ctx)

        func.body.scope = False
        func.body.accept(self, ctx)
        ctx.close()

    def visitParameter(self, para: Parameter, ctx: ScopeStack) -> None:

        varSymbol = ctx.findConflict(para.ident.value)
        if varSymbol:
            raise DecafDeclConflictError(para.ident.name)
        else:
            varSymbol = VarSymbol(name=para.ident.value, type=para.var_t.type)
            ctx.declare(varSymbol)
            para.setattr("symbol", varSymbol)
            # if para.init_expr:
            #     para.init_expr.accept(self, ctx)

    def visitBlock(self, block: Block, ctx: ScopeStack) -> None:
        # step-7
        if block.scope:
            ctx.open(Scope(ScopeKind.LOCAL))
        for child in block:
            child.accept(self, ctx)
        if block.scope:
            ctx.close()

    def visitReturn(self, stmt: Return, ctx: ScopeStack) -> None:
        stmt.expr.accept(self, ctx)

    def visitFor(self, stmt: For, ctx: ScopeStack) -> None:
        """
        1. Open a local scope for stmt.init.
        2. Visit stmt.init, stmt.cond, stmt.update.
        3. Open a loop in ctx (for validity checking of break/continue)
        4. Visit body of the loop.
        5. Close the loop and the local scope.
        """
        ctx.open(Scope(ScopeKind.LOCAL))
        if not stmt.init is NULL:
            stmt.init.accept(self, ctx)
        if not stmt.cond is NULL:
            stmt.cond.accept(self, ctx)
        if not stmt.update is NULL:
            stmt.update.accept(self, ctx)
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()
        ctx.close()

    def visitIf(self, stmt: If, ctx: ScopeStack) -> None:
        stmt.cond.accept(self, ctx)
        stmt.then.accept(self, ctx)

        # check if the else branch exists
        if not stmt.otherwise is NULL:
            stmt.otherwise.accept(self, ctx)

    def visitWhile(self, stmt: While, ctx: ScopeStack) -> None:
        stmt.cond.accept(self, ctx)
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()

    def visitDoWhile(self, stmt: DoWhile, ctx: ScopeStack) -> None:
        """
        1. Open a loop in ctx (for validity checking of break/continue)
        2. Visit body of the loop.
        3. Close the loop.
        4. Visit the condition of the loop.
        """
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()
        stmt.cond.accept(self, ctx)

    def visitBreak(self, stmt: Break, ctx: ScopeStack) -> None:
        if not ctx.inLoop():
            raise DecafBreakOutsideLoopError()

    def visitContinue(self, stmt: Continue, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBreak.
        """
        if not ctx.inLoop():
            raise DecafBreakOutsideLoopError()

    def visitDeclaration(self, decl: Declaration, ctx: ScopeStack) -> None:
        """
        1. Use ctx.findConflict to find if a variable with the same name has been declared.
        2. If not, build a new VarSymbol, and put it into the current scope using ctx.declare.
        3. Set the 'symbol' attribute of decl.
        4. If there is an initial value, visit it.
        """
        varSymbol = ctx.findConflict(decl.ident.value)
        if varSymbol:
            raise DecafDeclConflictError(decl.ident.name)
        else:
            varSymbol = VarSymbol(name=decl.ident.value, type=decl.var_t.type,
                                  isGlobal=ctx.currentScope().isGlobalScope())
            ctx.declare(varSymbol)
            decl.setattr("symbol", varSymbol)

            if decl.init_expr:
                decl.init_expr.accept(self, ctx)
                if varSymbol.isGlobal:
                    if varSymbol.type.is_array():
                        raise DecafBadAssignTypeError()
                    elif not isinstance(decl.init_expr, IntLiteral):
                        raise DecafGlobalVarBadInitValueError(decl.ident.name)

    def visitCall(self, expr: FuncCall, ctx: ScopeStack) -> None:
        varSymbol = ctx.lookup(expr.func.value)
        if not varSymbol or not varSymbol.isFunc:
            raise DecafUndefinedFuncError(expr.func.value)
        else:
            func_para_num = len(expr.para)
            if varSymbol.parameterNum != func_para_num:
                raise DecafParameterMisMatchError(varSymbol.name, varSymbol.parameterNum, func_para_num)

            for para in expr.para:
                para.accept(self, ctx)

    def visitAssignment(self, expr: Assignment, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBinary.
        """
        expr.lhs.accept(self, ctx)
        expr.rhs.accept(self, ctx)
        # pass

    def visitUnary(self, expr: Unary, ctx: ScopeStack) -> None:
        expr.operand.accept(self, ctx)

    def visitBinary(self, expr: Binary, ctx: ScopeStack) -> None:
        expr.lhs.accept(self, ctx)
        expr.rhs.accept(self, ctx)

    def visitCondExpr(self, expr: ConditionExpression, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBinary.
        """
        expr.cond.accept(self, ctx)
        expr.then.accept(self, ctx)
        if expr.otherwise:
            expr.otherwise.accept(self, ctx)

    def visitIdentifier(self, ident: Identifier, ctx: ScopeStack) -> None:
        """
        1. Use ctx.lookup to find the symbol corresponding to ident.
        2. If it has not been declared, raise a DecafUndefinedVarError.
        3. Set the 'symbol' attribute of ident.
        """
        value = ident.value
        varSymbol = ctx.lookup(value)
        if not varSymbol:
            raise DecafUndefinedVarError(value)
        if varSymbol.isFunc:
            raise DecafUndefinedVarError(value)
        if not varSymbol.type.is_base():
            raise DecafTypeMismatchError()
        ident.setattr("symbol", varSymbol)
        # pass

    def visitIntLiteral(self, expr: IntLiteral, ctx: ScopeStack) -> None:
        value = expr.value
        if value > MAX_INT:
            raise DecafBadIntValueError(value)

    def visitArrayRef(self, arr: ArrayRef, ctx: T) -> None:
        value = arr.value
        varSymbol = ctx.lookup(value)
        if not varSymbol:
            raise DecafUndefinedVarError(value)
        if varSymbol.isFunc:
            raise DecafUndefinedFuncError(value)

        # Array type check
        arr_type = varSymbol.type
        for idx in arr.indexes:
            idx.accept(self, ctx)
            if not arr_type.is_array():
                raise DecafBadIndexError
            arr_type = arr_type.base
        if not arr_type.is_base():
            raise DecafBadIndexError

        arr.setattr("symbol", varSymbol)

    def visitArrayExpr(self, arr: ArrayExpr, ctx: T) -> Optional[U]:
        return arr.array.accept(self, ctx)
