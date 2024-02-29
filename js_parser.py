
from grammar import *
from typing import Type, TypeVar
from typing import List

class ParsingException(Exception):
    pass

T = TypeVar('T', bound=Enum)
def reverse_enum_dict(enum: Type[T]) -> dict[str, T]:
    return { member.value: member for member in enum }
        
def parse(raw_expression: dict) -> SyntacticElement:
    match raw_expression:

        case { "type": "Program", "body": child_expressions }:
            children = [parse(e) for e in child_expressions]
            top_level_terms = children[:-1]
            statement = children[-1]
            return Program(
                top_level_terms=top_level_terms,
                statement=statement,
            )

        case { "type": "ExpressionStatement", "expression": child_expression }:
            return parse(child_expression)
        
        case { "type": "BinaryExpression", "operator": operator, "left": left, "right": right }:
            if operator in ["+", "-", "/", "*"]:
                return ArithmeticExpression(
                    operator=reverse_enum_dict(ArithmeticOperator)[operator],
                    left=parse(left),
                    right=parse(right),
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
        
        case { "type": "FunctionExpression", "params": [parameter], "body": body }:
            return FunctionExpression(
                parameter=parse(parameter),
                body=parse(body)
            )
        
        case { "type": "CallExpression", "callee": callee, "arguments": arguments}:
            argument = arguments[0] # as per project spec, we only support one argument
            return CallExpression(
                callee=parse(callee),
                call_expression=parse(argument),
            )
        
        case { "type": "BlockStatement", "body": body }:
            return BlockStatement(
                body=[parse(e) for e in body[:-1]],
                return_statement=parse(body[-1])
            )
        
        case { "type": "ReturnStatement", "argument": argument }:
            return parse(argument)
        
        case { "type": "AssignmentExpression", "left": left, "right": right }:
            return AssignmentExpression(
                left=parse(left),
                right=parse(right)
            )
            
        case _ as unreachable:
            raise ParsingException(f"Unrecognized expression while parsing: {unreachable}")
            
def to_string(element: SyntacticElement) -> str:
    match element:
        case Program(variable_declarations, statement):
            return '\n'.join(to_string(expression) for expression in [*variable_declarations, statement])
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
        case BlockStatement(body, statement):
            return f"(block_statement {', '.join([to_string(expression) for expression in body])} {to_string(statement)})"
        case FunctionExpression(parameter, body):
            return f"(function)"
        case CallExpression(callee):
            return f"(call {to_string(callee)})"
        case AssignmentExpression(left, right):
            return f"(assignment {to_string(left)} {to_string(right)})"
        
        case _ as unreachable:
            raise Exception(f"Unrecognized expression: {unreachable}")
        