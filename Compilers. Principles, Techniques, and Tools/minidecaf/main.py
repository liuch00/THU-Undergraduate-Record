import argparse
import sys

from backend.asm import Asm
from backend.reg.bruteregalloc import BruteRegAlloc
from backend.riscv.riscvasmemitter import RiscvAsmEmitter
from frontend.ast.tree import Program
from frontend.lexer import lex, lexer
from frontend.parser import parser
from frontend.tacgen.tacgen import TACGen
from frontend.typecheck.namer import Namer
from frontend.typecheck.typer import Typer
from utils.printtree import TreePrinter
from utils.riscv import Riscv
from utils.tac.tacprog import TACProg


def parseArgs():
    parser = argparse.ArgumentParser(description="MiniDecaf compiler")
    parser.add_argument("--input", type=str, help="the input C file")
    parser.add_argument("--parse", action="store_true",
                        help="output parsed AST")
    parser.add_argument("--tac", action="store_true",
                        help="output transformed TAC")
    parser.add_argument("--riscv", action="store_true",
                        help="output generated RISC-V")
    return parser.parse_args()


def readCode(fileName):
    with open(fileName, "r") as f:
        return f.read()


# The parser stage: MiniDecaf code -> Abstract syntax tree
def step_parse(args: argparse.Namespace):
    code = readCode(args.input)
    r: Program = parser.parse(code, lexer=lexer)

    errors = parser.error_stack
    if errors:
        print("\n".join(map(str, errors)), file=sys.stderr)
        exit(1)

    return r


# IR generation stage: Abstract syntax tree -> Three-address code
def step_tac(p: Program):
    namer = Namer()
    p = namer.transform(p)
    typer = Typer()
    p = typer.transform(p)

    tacgen = TACGen()
    tac_prog = tacgen.transform(p)

    return tac_prog


# Target code generation stage: Three-address code -> RISC-V assembly code
def step_asm(p: TACProg):
    riscvAsmEmitter = RiscvAsmEmitter(Riscv.AllocatableRegs, Riscv.CallerSaved, p.glob_vars)
    asm = Asm(riscvAsmEmitter, BruteRegAlloc(riscvAsmEmitter))
    prog = asm.transform(p)
    return prog


def main():
    args = parseArgs()

    def _parse():
        r = step_parse(args)
        #print("\nParsed AST:\n")
        #printer = TreePrinter(indentLen=2)
        # printer.work(r)
        return r

    def _tac():
        tac = step_tac(_parse())
        #print("\nGenerated TAC:\n")
        # tac.printTo()
        return tac

    def _asm():
        asm = step_asm(_tac())
        #print("\nGenerated ASM:\n")
        # print(asm)
        return asm

    if args.riscv:
        prog = _asm()
    elif args.tac:
        prog = _tac()
    elif args.parse:
        prog = _parse()

    if args.tac:
        prog.printTo()
    else:
        print(prog)

    return


if __name__ == "__main__":
    main()
