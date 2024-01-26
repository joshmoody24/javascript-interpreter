
from grammar.expressions import *
from typing import Type
from typing_extensions import assert_never

class ParsingException(Exception):
    pass

def reverse_enum_dict(enum: Type[Enum]) -> dict:
    return { member.value: member for member in enum }

def parse(raw_expression: dict) -> Expression:
    return expression(raw_expression)
        
def expression(raw_expression: dict) -> Expression:
    match raw_expression:

        case { "type": "Program", "body": [child_expression] }:
            return expression(child_expression)

        case { "type": "ExpressionStatement", "expression": child_expression }:
            return expression(child_expression)
        
        case { "type": "BinaryExpression", "operator": operator, "left": left, "right": right }:
            if operator in ["+", "-", "/", "*"]:
                return ArithmeticExpression(
                    operator=reverse_enum_dict(ArithmeticOperator)[operator],
                    left=expression(left),
                    right=expression(right)
                )
            elif operator in ["==", "<"]:
                return RelationalExpression(
                    operator=reverse_enum_dict(RelationalOperator)[operator],
                    left=expression(left),
                    right=expression(right)
                )
            raise ParsingException(f"Invalid binary expression operator: {operator}")
        
        case { "type": "LogicalExpression", "operator": operator, "left": left, "right": right }:
            if operator in ["&&", "||"]:
                return LogicalExpression(
                    operator=reverse_enum_dict(LogicalOperator)[operator],
                    left=expression(left),
                    right=expression(right)
                )
            raise ParsingException(f"Invalid logical expression operator: {operator}")

        case { "type": "Literal", "value": value }:
            if isinstance(value, bool):
                return BooleanExpression(value)
            else:
                return NumberExpression(value)
            
        case { "type": "UnaryExpression", "argument": argument }:
            return UnaryExpression(argument=expression(argument))
        
        case { "type": "ConditionalExpression", "test": test, "consequent": consequent, "alternate": alternate }:
            return ConditionalExpression(
                test=expression(test),
                consequent=expression(consequent),
                alternate=expression(alternate)
            )
            
        case _ as unreachable:
            raise ParsingException(f"Unrecognized expression: {unreachable}")
            
def to_string(expression: Expression) -> str:
    match expression:
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
        case _ as unreachable:
            assert_never(unreachable)