
from grammar.expressions import *
from grammar.variables import *
from typing import Type, TypeVar, Dict
from typing_extensions import assert_never

class ParsingException(Exception):
    pass

T = TypeVar('T', bound=Enum)
def reverse_enum_dict(enum: Type[T]) -> Dict[str, T]:
    return { member.value: member for member in enum }
        
def parse(raw_expression: dict) -> Expression:
    match raw_expression:

        case { "type": "Program", "body": child_expressions }:
            return [parse(e) for e in child_expressions]

        case { "type": "ExpressionStatement", "expression": child_expression }:
            return parse(child_expression)
        
        case { "type": "BinaryExpression", "operator": operator, "left": left, "right": right }:
            if operator in ["+", "-", "/", "*"]:
                return ArithmeticExpression(
                    operator=reverse_enum_dict(ArithmeticOperator)[operator],
                    left=parse(left),
                    right=parse(right)
                )
            elif operator in ["==", "<"]:
                return RelationalExpression(
                    operator=reverse_enum_dict(RelationalOperator)[operator],
                    left=parse(left),
                    right=parse(right)
                )
            raise ParsingException(f"Invalid binary expression operator: {operator}")
        
        case { "type": "LogicalExpression", "operator": operator, "left": left, "right": right }:
            if operator in ["&&", "||"]:
                return LogicalExpression(
                    operator=reverse_enum_dict(LogicalOperator)[operator],
                    left=parse(left),
                    right=parse(right)
                )
            raise ParsingException(f"Invalid logical expression operator: {operator}")

        case { "type": "Literal", "value": value }:
            if isinstance(value, bool):
                return BooleanExpression(value)
            else:
                return NumberExpression(value)
            
        case { "type": "UnaryExpression", "argument": argument }:
            return UnaryExpression(argument=parse(argument))
        
        case { "type": "ConditionalExpression", "test": test, "consequent": consequent, "alternate": alternate }:
            return ConditionalExpression(
                test=parse(test),
                consequent=parse(consequent),
                alternate=parse(alternate)
            )
        
        case { "type": "VariableDeclaration", "declarations": declarations }:
            return VariableDeclaration(
                declarators=[parse(declaration) for declaration in declarations]
            )
        
        case { "type": "VariableDeclarator", "id": identifier, "init": init_expression }:
            return VariableDeclarator(identifier=parse(identifier), expression=parse(init_expression))
        
        case { "type": "Identifier", "name": name }:
            return Identifier(name=name)
            
        case _ as unreachable:
            raise ParsingException(f"Unrecognized expression: {unreachable}")
            
def to_string(expression: Expression) -> str:
    match expression:
        case list(expressions):
            return '\n'.join(to_string(expression) for expression in expressions)
        case BooleanExpression(value):
            return f"(boolean {str(value).lower()})"
        case NumberExpression(value):
            return f"(number {value})"
        case ArithmeticExpression(operator, left, right):
            return f"(arithmetic {operator.value} {to_string(left)} {to_string(right)})"
        case UnaryExpression(argument):
            return f"(unary ! {to_string(argument)})"
        case RelationalExpression(operator, left, right):
            return f"(relational {operator.value} {to_string(left)} {to_string(right)})"
        case LogicalExpression(operator, left, right):
            return f"(logical {operator.value} {to_string(left)} {to_string(right)})"
        case ConditionalExpression(test, consequent, alternate):
            return f"(conditional {to_string(test)} {to_string(consequent)} {to_string(alternate)})"
        case VariableDeclaration(declarators):
            return f"(variable_declaration {', '.join([to_string(declarator) for declarator in declarators])})"
        case VariableDeclarator(identifier, expression):
            return f"(variable_declarator {to_string(identifier)} {to_string(expression)})"
        case Identifier(name):
            return f"(identifier {name})"
        case _ as unreachable:
            assert_never(unreachable)