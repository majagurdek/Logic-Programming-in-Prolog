#  Copyright (c) 2021. Created by Mateusz Slazynski for the educational purposes.
#     Feel free to use/modify this code for any greater good.
#     It would be nice however if you mentioned me somewhere.
#     Still, no pressure - have a nice day!

from __future__ import annotations
from src.term import Term, TmAbs, TmVar, TmApp
from src.lambda_program import LambdaProgram
from dataclasses import dataclass
from enum import Enum, auto


class Rule(Enum):
    App1 = 0
    App2 = auto()
    AppAbs = auto()

    def __repr__(self):
        return f"Rule.{self.name}"


@dataclass(frozen=True)
class Transition:
    old_state: LambdaProgram
    new_state: LambdaProgram
    rule: Rule
    witnesses: tuple[Transition] = ()


class NoRuleApplies(Exception):
    pass


class LambdaSemantics:
    '''
        Class representing semantics of the untyped lambda calculus.

        Attributes:
            - free_names: list[str]
                This list stores names of the free variables in order to print them in a pretty way :)
    '''
    def __init__(self, free_names: list[str]):
        self.free_names = free_names

    @staticmethod
    def is_term_val(t: Term) -> bool:
        '''
             This static method checks whether the term is a value.
             Based on the 'isval' function from the TAPL p. 87

             :param t: a Lambda Calculus term
             :return: whether the term is a value
        '''
        # TODO:
        # term is a value only when it is an abstraction (TmAbs)
        match t:
            case TmAbs(_, _, _):
                return True
            case _:
                return False


    def single_step(self, state_before: Term) -> Transition:
        '''
             This static method checks whether the term is a value.
             Based on the 'eval1' function from the TAPL p. 87

             :param state_before: a Lambda Calculus term
             :return: a transition applied according the Lambda Calculus semantics
        '''

        def transition(new_state: Term, rule: Rule, witnesses: tuple(Transition) = ()) -> Transition:
            ''' Just a helper function to quickly create a transition'''
            return Transition(LambdaProgram(state_before, self.free_names), LambdaProgram(new_state, self.free_names), rule, witnesses)

        # TODO:
        # fill missing cases:
        # - Rule.AppAbs:
        #   * use LambdaSemantics._term_substitute
        # - Rule.App1
        # - Rule.App2

        match state_before:
            # TODO: missing cases...
            case TmApp(fi, TmAbs(_, x, t12), v2) if self.is_term_val(v2):
                ts = LambdaSemantics._term_substitute(v2, t12)
                return transition(ts, Rule.AppAbs)
            case TmApp(f1, v1, t2) if self.is_term_val(v1):
                t2prim = self.single_step(t2)
                return transition(t2prim, Rule.App2)
            case TmApp(f1, t1, t2):
                t1prim = self.single_step(t1)
                return transition(t1prim, Rule.App1)
            case _:
                raise NoRuleApplies()

                
    @staticmethod
    def _term_substitute(s: Term, t: Term) -> Term:
        '''
             This static makes a substitution in t. [0->s]t
             Based on the 'termSubstTop' function from the TAPL p. 87

             :param s: term that should replace the variable
             :param t: term containing variables to be replaced
             :return: new term create according to the substitution rules
        '''
        # TODO:
        # 1) use _term_shift to shift the variables in s by 1
        # 2) use _term_substitute_step to replace all occurences of 0 in t with result of the step 1)
        # 3) use _term_shift to shift the variables in result of the step 2) by -1
        # return result of the step 3)


        return LambdaSemantics._term_shift(-1,
            LambdaSemantics._term_substitute_step(0, LambdaSemantics._term_shift(1, s), t))

    @staticmethod
    def _term_shift(d: int, term: Term) -> Term:
        '''
             This static method shifts free variable indexes in the term.
             Based on the 'termShift' function from the TAPL p. 86

             :param d: how much the variables should be shifted
             :param term: Lambda Calculus term containing variables to be shifted
             :return: new term with shifted variables
        '''

        # TODO:
        # - define recursive walk function
        #   walk traverses the abstract syntax tree (term) and looks for variables
        #   it has to track the context (how deep we are / how many "abstractions" (TmAbs) is above
        #   a free variable will have index >= the current depth
        #   and such variables need to be shifted by 'd'
        #   tip. all the variables have to be updated when it comes to their context_length (also by 'd')
        # - call 'walk' with initial depth = 0
        def walk(c: int, t: int):
            match t:
                case TmVar(fi, x, n):
                    if x >= c:
                        return TmVar(fi, x + d, n + d)
                    else:
                        return TmVar(fi, x, n + d)
                case TmAbs(fi, x, t1):
                    return TmAbs(fi, x, walk(c + 1,  t1))
                case TmApp(fi, t1, t2):
                    return TmApp(fi, walk(c, t1), walk(c, t2))

        return walk(0, term)

    @staticmethod
    def _term_substitute_step(j: int, s: Term, term: TmAbs) -> Term:
        '''
             This static method substitutes variable with given index
             with a given term.
             Based on the 'termSubst' function from the TAPL p. 86

             :param j: index of the variable to be substituted
             :param s: term to be put at the variable place
             :param term: term containing variables to be substituted
             :return: new term with substituted variables
        '''

        # TODO:
        # - define recursive walk function
        #   walk traverses the abstract syntax tree (term) and looks for variables
        #   it has to track the context (how deep we are / how many "abstractions" (TmAbs) is above use
        #   a variable has to be substituted if its index equals sum of depth and j
        #   the new term is the 's' term shifted (_term_shift) by the current depth
        # - call 'walk' with initial depth = 0
        def walk(c, t):
            match t:
                case TmVar(fi, x, n):
                    if x == j + c:
                        return LambdaSemantics._term_shift(c, s)
                    else:
                        return TmVar(fi, x, n)
                case TmAbs(fi, x, t1):
                    return TmAbs(fi, x, walk(c + 1, t1))
                case TmApp(fi, t1, t2):
                    return TmApp(fi, walk(c, t1), walk(c, t2))

        return walk(0, term)

