from dataclasses import dataclass
from .variables import VariableDeclaration
from .expressions import Expression

@dataclass
class Program:
    variable_declarations: list[VariableDeclaration]
    statement: Expression