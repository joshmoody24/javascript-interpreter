from grammar import *
from dataclasses import dataclass
from typing import Callable

@dataclass
class ErrorResult:
    message: str

@dataclass
class Void:
    pass

@dataclass
class ValueResult:
    value: bool | int | Callable | Void

Result = ErrorResult | ValueResult

def to_string(result: Result) -> str:
    match result:
        case ErrorResult(message):
            return f'(error "{message}")'
        case ValueResult(value):
            if type(value) is bool:
                return f'(value (boolean {str(value).lower()}))'
            elif type(value) is int:
                return f'(value (number {value}))'
            elif type(value) is Void:
                return f'(value (void))'
            elif callable(value):
                return f'(value (function))'
            else:
                return f'(value (unknown))'
            
def free_heap_address(heap: dict[int, int]) -> int:
    return max(heap.keys(), default=0) + 1

def interpret(syntactic_element: SyntacticElement, variables: dict[str, int] = {}, heap: dict[int, int] = {}):
    match syntactic_element:
        case Program(variable_declarations, statement):
            for declaration in variable_declarations:
                result, variables, heap = interpret(declaration, variables, heap)
                if isinstance(result, ErrorResult):
                    return result
            return interpret(statement, variables, heap)
        
        case VariableDeclaration(declarators):
            for declarator in declarators:
                result, variables, heap = interpret(declarator.expression, variables, heap)
                if isinstance(result, ErrorResult):
                    return result
                if declarator.identifier.name in variables:
                    return ErrorResult(f"variable `{declarator.identifier.name}` already declared - banana"), variables, heap
                address = free_heap_address(heap)
                variables = {**variables, declarator.identifier.name: address}
                heap = {**heap, address: result.value}
            return ValueResult(Void()), variables, heap

        case BooleanExpression(value):
            return ValueResult(value=value), variables, heap

        case NumberExpression(value):
            return ValueResult(value), variables, heap

        case ArithmeticExpression(operator, left, right):
            left_result, variables, heap = interpret(left, variables, heap)
            right_result, variables, heap = interpret(right, variables, heap)
            if isinstance(left_result, ErrorResult):
                return left_result, variables, heap
            if isinstance(right_result, ErrorResult):
                return right_result, variables, heap
            if isinstance(left_result.value, bool) or isinstance(left_result.value, Void):
                return ErrorResult(f"left value of arithmetic expression ({left_result.value}) must be number - banana"), variables, heap
            if isinstance(right_result.value, bool) or isinstance(right_result.value, Void):
                return ErrorResult(f"right value of arithmetic expression ({right_result.value}) must be number - banana"), variables, heap
            match operator:
                case ArithmeticOperator.ADD:
                    return ValueResult(left_result.value + right_result.value), variables, heap
                case ArithmeticOperator.SUBTRACT:
                    return ValueResult(left_result.value - right_result.value), variables, heap
                case ArithmeticOperator.MULTIPLY:
                    return ValueResult(left_result.value * right_result.value), variables, heap
                case ArithmeticOperator.DIVIDE:
                    if right_result.value == 0:
                        return ErrorResult("division by zero banana"), variables, heap
                    return ValueResult(left_result.value // right_result.value), variables, heap
                case _:
                    raise Exception(f"unrecognized arithmetic operator: {operator}")

        case LogicalExpression(operator, left, right):
            left_result, variables, heap = interpret(left, variables, heap)
            if isinstance(left_result, ErrorResult):
                return left_result, variables, heap
            if not isinstance(left_result.value, bool):
                return ErrorResult(f"left value of logical expression ({left_result.value}) must be boolean - banana"), variables, heap
            if operator == LogicalOperator.AND and not left_result.value:
                return ValueResult(False), variables, heap # short-circuit
            if operator == LogicalOperator.OR and left_result.value:
                return ValueResult(True), variables, heap

            right_result, variables, heap = interpret(right, variables, heap)
            if isinstance(right_result, ErrorResult):
                return right_result, variables, heap
            if not isinstance(right_result.value, bool):
                return ErrorResult(f"right value of logical expression ({right_result.value}) must be boolean - banana"), variables, heap
            return ValueResult(right_result.value), variables, heap
        
        case RelationalExpression(operator, left, right):
            left_result, variables, heap = interpret(left, variables, heap)
            right_result, variables, heap = interpret(right, variables, heap)
            if isinstance(left_result, ErrorResult):
                return left_result, variables, heap
            if isinstance(right_result, ErrorResult):
                return right_result, variables, heap
            # isinstance(False, int) == True, so we need to check for bool first (bool is a subclass of int
            if not isinstance(left_result.value, int) or isinstance(left_result.value, bool):
                return ErrorResult(f"left value of relational expression ({left_result.value}) must be number - banana"), variables, heap
            if not isinstance(right_result.value, int) or isinstance(right_result.value, bool):
                return ErrorResult(f"right value of relational expression ({right_result.value}) must be number - banana"), variables, heap
            match operator:
                case RelationalOperator.EQUALS:
                    return ValueResult(left_result.value == right_result.value), variables, heap
                case RelationalOperator.LESS_THAN:
                    return ValueResult(left_result.value < right_result.value), variables, heap
                case _:
                    raise Exception(f"unrecognized relational operator: {operator}")

        case UnaryExpression(argument):
            argument_result, variables, heap = interpret(argument, variables, heap)
            if isinstance(argument_result, ErrorResult):
                return argument_result, variables, heap
            if not isinstance(argument_result.value, bool):
                return ErrorResult(f"argument value of unary expression ({argument_result.value}) must be boolean - banana"), variables, heap
            return ValueResult(not argument_result.value), variables, heap

        case ConditionalExpression(test, consequent, alternate):
            test_result, variables, heap = interpret(test, variables, heap)
            if isinstance(test_result, ErrorResult):
                return test_result, variables, heap
            if not isinstance(test_result.value, bool):
                return ErrorResult(f"test value of conditional expression ({test_result.value}) must be boolean - banana"), variables, heap
            if test_result.value:
                return interpret(consequent, variables, heap)
            else:
                return interpret(alternate, variables, heap)

        case Identifier(name):
            if name not in variables:
                return ErrorResult(f"unbound identifier `{name}` - banana"), variables, heap
            return ValueResult(heap[variables[name]]), variables, heap
        
        case FunctionExpression(parameter, body):
            def function(argument, heap):
                address = free_heap_address(heap)
                return interpret(
                    body,
                    {**variables, parameter.name: address},
                    {**heap, address: argument}
                )
            return ValueResult(function), variables, heap
        
        case CallExpression(callee, call_expression):
            callee_func, variables, heap = interpret(callee, variables, heap)
            if isinstance(callee_func, ErrorResult):
                return callee_func, variables, heap
            parameter, variables, heap = interpret(call_expression, variables, heap)
            if isinstance(parameter, ErrorResult):
                return parameter, variables, heap
            if not callable(callee_func.value):
                return ErrorResult(f"callee `{callee}` is not a function - banana"), variables, heap
            call_expression_result, _, heap = callee_func.value(parameter.value, heap)
            if isinstance(call_expression_result, ErrorResult):
                return call_expression_result, variables, heap
            return ValueResult(call_expression_result.value), variables, heap
        
        # same as Program
        case BlockStatement(body, return_statement):
            for declaration in body:
                result, variables, heap = interpret(declaration, variables, heap)
                if isinstance(result, ErrorResult):
                    return result, variables, heap
            return interpret(return_statement, variables, heap)
        
        case AssignmentExpression(left, right):
            right_result, variables, heap = interpret(right, variables, heap)
            if isinstance(right_result, ErrorResult):
                return right_result, variables, heap
            if left.name not in variables:
                return ErrorResult(f"unbound identifier `{left.name}` - banana"), variables, heap
            heap = {**heap, variables[left.name]: right_result.value}
            return ValueResult(Void()), variables, heap

        case _ as unreachable:
            raise Exception(f"unreachable code reached: {unreachable}")