#  Copyright (c) 2021-2021. Created by Mateusz Slazynski for the educational purposes.
#     Feel free to use/modify this code for any greater good.
#     It would be nice however if you mentioned me somewhere.
#     Still, no pressure - have a nice day!

from __future__ import annotations

from typing import Optional

from src.term import Term, TmAbs, TmVar, TmApp, TmTrue, TmFalse, TmZero, TmSucc, TmIf, TmIsZero, Info, TmPred
from src.lambda_program import TypedLambdaProgram
from dataclasses import dataclass
from enum import Enum, auto
from src.type import LambdaType, BaseType, InvalidType, ArrowType


class LambdaTypeErrorType(Enum):
    """
    This enum represent all possible type errors, the typechecker can detect.
    Each type is accompanied with a message template, that can be used to print the error, e.g.
        LambdaTypeErrorType.IfDivergentBranches.value.format("type1", "type2")
    would produce an error message corresponding to IfDivergentBranches.
    The strings also self-document the enum :)
    """
    IfInvalidGuard = "guard of conditional is not a boolean, got '{}'"
    IfDivergentBranches = "branches of conditional have different types: '{}' and '{}'"
    UnnaturalArg = "argument is not a natural number, got '{}'"
    UnknownType = "a variable has no known type"
    InvalidType = "program uses an invalid type: '{}'"
    InvalidArgType = "function expected type '{}', got '{}'"
    InvalidFunType = "expected arrow type, got '{}'"

@dataclass
class LambdaTypeError(Exception):
    """
        A type error class. Nothing fancy,

        Attributes:
        ===========
        msg: str
            a message explaining the error
        term: Term
            the mistyped term
        type_context: TypeContext
            context associated with the error
        error_type: LambdaTypeErrorType
            type of the error
    """
    msg: str
    term: Term
    type_context: TypeContext
    error_type: LambdaTypeErrorType

    def __str__(self):
        return f"[Type Error] {self.msg}\n" \
               f"- program: {self.term}\n" \
               f"- type context: {self.type_context}\n" \
               f"- position: {self.term.info}"


@dataclass(frozen=True)
class TypeContext:
    """
        A typing context, contains info about types of the bound variables.

        Attributes:
        ===========
        _context: List[LambdaType]
            list of types corresponding to the de Bruijn indices

        Static Methods:
        ===============
        empty() -> TypeContext:
            create an empty context

        Methods:
        ========
        type_of(index: int) -> Optional[LambdaType]
            returns type of the variable with a given de Bruijn index
            if the variable is free, the result is None
        extend_with_type(type: LambdaType) -> TypeContext:
            creates a new context with a new type binding
    """
    _context: list[LambdaType]

    @staticmethod
    def empty() -> TypeContext:
        return TypeContext([])

    def type_of(self, index: int) -> Optional[LambdaType]:
        if index < len(self._context):
            return self._context[index]
        return None

    def extend_with_type(self, type: LambdaType) -> TypeContext:
        return TypeContext([type] + self._context)

    def __str__(self) -> str:
        return f"{[str(t) for t in self._context]}"

class TypedLambdaTypechecker:
    '''
        A type-checker for the Typed Lambda Calculus (with Nat and Bool types).

        Methods:
            - typecheck(program: TypedLambdaProgram) -> LambdaType
                returns type returned by the given lambda program
                in case of type error, raises LambdaTypeError
    '''

    def typecheck(self, program: TypedLambdaProgram) -> LambdaType:
        return self._typecheck(program.term, TypeContext.empty())

    def _typecheck(self, term: Term, type_context: TypeContext) -> LambdaType:
        """
        Given a type context, returns a type of a term.
        In case of an error, raises LambdaTypeError

        :param term: a typed lambda calculus term destined to be type-checked
        :param type_context: a type context (contains type info about the bound variables)
        :return: type of the term
        """

        def raise_type_error(error_type: LambdaTypeErrorType, *msg_args) -> None:
            """
            Helper to raise a type error based on its type.

            :param error_type: type of the raised
            :param msg_args: values used to fill format string associated to the error
            """
            error_msg = error_type.value.format(*msg_args)
            raise LambdaTypeError(error_msg, term, type_context, error_type)

        def is_invalid(t: LambdaType) -> bool:
            match t:
                case InvalidType():
                    return True
                case ArrowType(t1, t2):
                    return is_invalid(t1) or is_invalid(t2)
                case _:
                    return False

        # TODO:
        # Fill missing code based on the typeof function (TAPL book, p. 115).
        # Differences:
        # - TAPL handles only the Bool (BaseType.Bool), not the Nat type (BaseType.Nat)
        #   refer to the TAPL p. 93 for the Nat rules
        # - TAPL code doesn't handle "invalid type" (InvalidType), our parser doesn't validate type annotations
        #   just remember that ArrowType with InvalidType on any side is also invalid
        # - use raise_type_error to raise errors
        #   be sure you have handled all the error types from LambdaTypeErrorType

        match term:
            case TmTrue(_) | TmFalse(_):    #chyba dobrze
                return BaseType.Bool

            case TmIf(fi, t1, t2, t3):       #chyba dobrze
                tyT1 = self._typecheck(t1, type_context)
                if tyT1 == BaseType.Bool:
                    tyT2 = self._typecheck(t2, type_context)
                    tyT3 = self._typecheck(t3, type_context)
                    if tyT2 == tyT3:
                        return tyT2
                    else:
                        raise_type_error(LambdaTypeErrorType.IfDivergentBranches, tyT2, tyT3)
                else:
                    raise_type_error(LambdaTypeErrorType.IfInvalidGuard, tyT1)

                '''
                cond_type = self._typecheck(cond, type_context)
                if cond_type == BaseType.Bool:
                    raise_type_error(LambdaTypeErrorType.IfInvalidGuard, cond_type)

                if_true_type = self._typecheck(if_true, type_context)
                if_false_type = self._typecheck(if_false, type_context)
                if if_true_type != if_false_type:
                    raise_type_error(LambdaTypeErrorType.IfDivergentBranches, if_true, if_false)

                return if_true_type
                '''

            case TmVar(_, index, _):        #chyba dobrze
                var_type = type_context.type_of(index)
                if var_type is None:
                    raise_type_error(LambdaTypeErrorType.UnknownType)
                return var_type

            case TmAbs(fi, x, tyT1, t2):
                if is_invalid(tyT1):
                    raise_type_error(LambdaTypeErrorType.InvalidType, tyT1)
                ctx_ = type_context.extend_with_type(tyT1)
                tyT2 = self._typecheck(t2, ctx_)
                return ArrowType(tyT1, tyT2)

            case TmApp(fi, t1, t2):
                tyT1 = self._typecheck(t1, type_context)
                tyT2 = self._typecheck(t2, type_context)
                match tyT1:
                    case ArrowType(tyT11, tyT12):
                        if tyT2 == tyT11:
                            return tyT12
                        else:
                            raise_type_error(LambdaTypeErrorType.InvalidArgType, tyT11, tyT2)
                    case _:
                        raise_type_error(LambdaTypeErrorType.InvalidFunType, tyT1)

            case TmZero():
                return BaseType.Nat

            case TmSucc(fi, cond):
                cond_type = self._typecheck(cond, type_context)
                if cond_type != BaseType.Nat:
                    raise_type_error(LambdaTypeErrorType.UnnaturalArg, cond_type)
                return BaseType.Nat

            case TmPred(fi, cond):
                cond_type = self._typecheck(cond, type_context)
                if cond_type != BaseType.Nat:
                    raise_type_error(LambdaTypeErrorType.UnnaturalArg, cond_type)
                return BaseType.Nat

            case TmIsZero(fi, cond):
                cond_type = self._typecheck(cond, type_context)
                if cond_type != BaseType.Nat:
                    raise_type_error(LambdaTypeErrorType.UnnaturalArg, cond_type)
                return BaseType.Bool


