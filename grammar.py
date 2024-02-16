from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

@dataclass
class BooleanExpression:
    value: bool

@dataclass    
class NumberExpression:
    value: int

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
class Identifier:
    name: str

@dataclass
class ConditionalExpression:
    test: Expression
    consequent: Expression
    alternate: Expression

@dataclass
class FunctionExpression:
    parameter: Identifier
    body: BlockStatement

@dataclass
class CallExpression:
    callee: Identifier
    call_expression: Expression

@dataclass
class Program:
    variable_declarations: list[VariableDeclaration]
    statement: Expression

@dataclass
class BlockStatement:
    body: list[VariableDeclaration]
    return_statement: Expression

@dataclass
class VariableDeclarator:
    identifier: Identifier
    expression: Expression

@dataclass
class VariableDeclaration:
    declarators: list[VariableDeclarator]

class ArithmeticOperator(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

class UnaryOperator(Enum):
    NOT = "!"

class RelationalOperator(Enum):
    LESS_THAN = "<"
    EQUALS = "=="

class LogicalOperator(Enum):
    AND = "&&"
    OR = "||"

Expression = (
    BooleanExpression
    | NumberExpression
    | LogicalExpression
    | RelationalExpression
    | UnaryExpression
    | ConditionalExpression
    | ArithmeticExpression
    | FunctionExpression
    | CallExpression
)

SyntacticElement = (
    Program
    | BlockStatement
    | VariableDeclaration
    | Expression
)