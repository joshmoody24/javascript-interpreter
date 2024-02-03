from grammar.expressions import *
from dataclasses import dataclass
from typing_extensions import assert_never

@dataclass
class ErrorResult:
    message: str

@dataclass
class ValueResult:
    value: bool | int

Result = ErrorResult | ValueResult

def to_string(result: Result) -> str:
    match result:
        case ErrorResult(message):
            return f'(error "{message}")'
        case ValueResult(value):
            return f'(value ({"boolean" if type(value) is bool else "number"} {str(value).lower()}))'

def interpret(expression: Expression):
    match expression:
        case BooleanExpression(value):
            return ValueResult(value=value)

        case NumberExpression(value):
            return ValueResult(value)

        case ArithmeticExpression(operator, left, right):
            left_result = interpret(left)
            right_result = interpret(right)
            if isinstance(left_result, ErrorResult):
                return left_result
            if isinstance(right_result, ErrorResult):
                return right_result
            if type(left_result.value) is not int:
                return ErrorResult(f"left value of arithmetic expression ({left_result.value}) must be integer - banana")
            if type(right_result.value) is not int:
                return ErrorResult(f"right value of arithmetic expression ({right_result.value}) must be integer - banana")
            match operator:
                case ArithmeticOperator.ADD:
                    return ValueResult(left_result.value + right_result.value)
                case ArithmeticOperator.SUBTRACT:
                    return ValueResult(left_result.value - right_result.value)
                case ArithmeticOperator.MULTIPLY:
                    return ValueResult(left_result.value * right_result.value)
                case ArithmeticOperator.DIVIDE:
                    if right_result.value == 0:
                        return ErrorResult("division by zero banana")
                    return ValueResult(left_result.value // right_result.value)
                case _:
                    assert_never(operator)

        case LogicalExpression(operator, left, right):
            left_result = interpret(left)
            right_result = interpret(right)
            if isinstance(left_result, ErrorResult):
                return left_result
            if isinstance(right_result, ErrorResult):
                return right_result
            if not isinstance(left_result.value, bool):
                return ErrorResult(f"left value of logical expression ({left_result.value}) must be boolean - banana")
            if not isinstance(right_result.value, bool):
                return ErrorResult(f"right value of logical expression ({right_result.value}) must be boolean - banana")
            
            match operator:
                case LogicalOperator.AND:
                    return ValueResult(right_result).value if left_result.value else ValueResult(False)
                case LogicalOperator.OR:
                    return ValueResult(True) if left_result.value else ValueResult(right_result.value)
                case _:
                    assert_never(operator)

        case RelationalExpression(operator, left, right):
            left_result = interpret(left)
            right_result = interpret(right)
            if isinstance(left_result, ErrorResult):
                return left_result
            if isinstance(right_result, ErrorResult):
                return right_result
            if type(left_result.value) is not int:
                return ErrorResult(f"left value of relational expression ({left_result.value}) must be integer - banana")
            if type(right_result.value) is not int:
                return ErrorResult(f"right value of relational expression ({right_result.value}) must be integer - banana")
            
            match operator:
                case RelationalOperator.EQUALS:
                    return ValueResult(left_result.value == right_result.value)
                case RelationalOperator.LESS_THAN:
                    return ValueResult(left_result.value < right_result.value)
                case _:
                    assert_never(operator)

        case UnaryExpression(argument):
            argument_result = interpret(argument)
            if isinstance(argument_result, ErrorResult):
                return argument_result
            if not isinstance(argument_result.value, bool):
                return ErrorResult(f"argument value of unary expression ({argument_result.value}) must be boolean - banana")
            return ValueResult(not argument_result.value)

        case ConditionalExpression(test, consequent, alternate):
            test_result = interpret(test)
            if isinstance(test_result, ErrorResult):
                return test_result
            if not isinstance(test_result.value, bool):
                return ErrorResult(f"test value of conditional expression ({test_result.value}) must be boolean - banana")
            return interpret(consequent) if test_result.value else interpret(alternate)

        case _ as unreachable:
            assert_never(unreachable)