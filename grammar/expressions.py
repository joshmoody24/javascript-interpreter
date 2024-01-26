from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .operators import *

@dataclass
class BooleanExpression:
    value: bool

@dataclass    
class NumberExpression:
    value: float | int

@dataclass    
class ArithmeticExpression:
    operator: ArithmeticOperator
    left: Expression
    right: Expression

@dataclass
class LogicalExpression:
    operator: LogicalOperator
    left: Expression
    right: Expression

@dataclass
class RelationalExpression:
    operator: RelationalOperator
    left: Expression
    right: Expression

@dataclass
class UnaryExpression:
    argument: Expression

@dataclass
class ConditionalExpression:
    test: Expression
    consequent: Expression
    alternate: Expression

Expression = (
    BooleanExpression
    | NumberExpression
    | LogicalExpression
    | RelationalExpression
    | UnaryExpression
    | ConditionalExpression
    | ArithmeticExpression
)