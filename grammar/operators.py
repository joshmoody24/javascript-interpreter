from enum import Enum

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