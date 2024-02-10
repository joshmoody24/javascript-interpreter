from dataclasses import dataclass
from typing import List
from .expressions import Expression

@dataclass
class Identifier:
    name: str

@dataclass
class VariableDeclarator:
    identifier: Identifier
    expression: Expression

@dataclass
class VariableDeclaration:
    declarators: List[VariableDeclarator]