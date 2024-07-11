#  Copyright (c) 2021-2021. Created by Mateusz Slazynski for the educational purposes.
#     Feel free to use/modify this code for any greater good.
#     It would be nice however if you mentioned me somewhere.
#     Still, no pressure - have a nice day!

from __future__ import annotations
from src.term import *
from dataclasses import dataclass
from enum import Enum, auto

class Rule(Enum):
    IfTrue = auto()
    IfFalse = auto()
    If = auto()
    Succ = auto()
    PredZero = auto()
    PredSucc = auto()
    Pred = auto()
    IsZeroZero = auto()
    IsZeroSucc = auto()
    IsZero = auto()

@dataclass(frozen=True)
class Transition:
    old_state: Term
    new_state: Term
    rule: Rule
    witnesses: tuple[Transition] = ()

class NoRuleApplies(Exception):
    pass

class ArithmeticSemantics:

    @staticmethod
    def single_step(state_before: Term) -> Transition:
        def transition(new_state: Term, rule: Rule, witnesses: tuple(Transition) = ()):
            return Transition(state_before, new_state, rule, witnesses)

        match state_before:
            # TODO:
            # match cases according to the chapter 4 of the book, function eval1
            # main difference:
            # - instead of returning term you should return a transition object (using the transition function helper)
            # - each transition can also store results of the intermediate steps, i.e. if a rule requires another rule
            #   to match, it should store this transition in the "witnesses" tuple
            # transitions are later used to display a derivation tree
            case TmIf(_, TmTrue(_), t2, _):
                return transition(t2, Rule.IfTrue)
            case TmIf(_, TmFalse(_), _, t3):
                return transition(t3, Rule.IfFalse)
            case TmIf(fi,t1,t2,t3):
                witness = ArithmeticSemantics.single_step(t1)
                return transition(TmIf(fi, witness.new_state, t2, t3), Rule.If, (witness, ))
            case TmSucc(fi,t1):
                witness = ArithmeticSemantics.single_step(t1)
                return transition(TmSucc(fi, witness.new_state), Rule.Succ, (witness,))
            case TmPred(_,TmZero(_)): 
                return transition(TmZero(Info.dummy_info()), Rule.PredZero)
            case TmPred(_,TmSucc(_,nv1)) if nv1.is_numerical():
                return transition(nv1, Rule.PredSucc)
            case TmPred(fi,t1):
                witness = ArithmeticSemantics.single_step(t1)
                return transition(TmPred(fi, witness.new_state), Rule.Pred, (witness,))
            case TmIsZero(_,TmZero(_)):
                return transition(TmTrue(Info.dummy_info()), Rule.IsZeroZero)
            case TmIsZero(_,TmSucc(_,nv1)) if nv1.is_numerical():
                return transition(TmFalse(Info.dummy_info()), Rule.IsZeroSucc)
            case TmIsZero(fi, t1):
                witness = ArithmeticSemantics.single_step(t1)
                return transition(TmIsZero(fi, witness.new_state), Rule.IsZero, (witness,))
            case _:
                raise NoRuleApplies()
