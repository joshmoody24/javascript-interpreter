from grammar import *
from dataclasses import dataclass

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

def interpret(syntactic_element: SyntacticElement, variables: dict[str, int] = {}):
    match syntactic_element:
        case Program(variable_declarations, statement):
            for declaration in variable_declarations:
                variables = interpret(declaration, variables)
                if isinstance(variables, ErrorResult):
                    return variables
            return interpret(statement, variables)
        
        case VariableDeclaration(declarators):
            for declarator in declarators:
                result = interpret(declarator.expression, variables)
                if isinstance(result, ErrorResult):
                    return result
                if declarator.identifier.name in variables:
                    return ErrorResult(f"variable `{declarator.identifier.name}` already declared - banana")
                variables[declarator.identifier.name] = result.value
            return variables

        case BooleanExpression(value):
            return ValueResult(value=value)

        case NumberExpression(value):
            return ValueResult(value)

        case ArithmeticExpression(operator, left, right):
            left_result = interpret(left, variables)
            right_result = interpret(right, variables)
            if isinstance(left_result, ErrorResult):
                return left_result
            if isinstance(right_result, ErrorResult):
                return right_result
            if isinstance(left_result.value, bool):
                return ErrorResult(f"left value of arithmetic expression ({left_result.value}) must be number - banana")
            if isinstance(right_result.value, bool):
                return ErrorResult(f"right value of arithmetic expression ({right_result.value}) must be number - banana")
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
                    raise Exception(f"unrecognized arithmetic operator: {operator}")

        case LogicalExpression(operator, left, right):
            left_result = interpret(left, variables)
            if isinstance(left_result, ErrorResult):
                return left_result
            if not isinstance(left_result.value, bool):
                return ErrorResult(f"left value of logical expression ({left_result.value}) must be boolean - banana")
            if operator == LogicalOperator.AND and not left_result.value:
                return ValueResult(False) # short-circuit
            if operator == LogicalOperator.OR and left_result.value:
                return ValueResult(True)

            right_result = interpret(right, variables)
            if isinstance(right_result, ErrorResult):
                return right_result
            if not isinstance(right_result.value, bool):
                return ErrorResult(f"right value of logical expression ({right_result.value}) must be boolean - banana")
            return ValueResult(right_result.value)
        
        case RelationalExpression(operator, left, right):
            left_result = interpret(left, variables)
            right_result = interpret(right, variables)
            if isinstance(left_result, ErrorResult):
                return left_result
            if isinstance(right_result, ErrorResult):
                return right_result
            # isinstance(False, int) == True, so we need to check for bool first (bool is a subclass of int
            if not isinstance(left_result.value, int) or isinstance(left_result.value, bool):
                return ErrorResult(f"left value of relational expression ({left_result.value}) must be number - banana")
            if not isinstance(right_result.value, int) or isinstance(right_result.value, bool):
                return ErrorResult(f"right value of relational expression ({right_result.value}) must be number - banana")
            match operator:
                case RelationalOperator.EQUALS:
                    return ValueResult(left_result.value == right_result.value)
                case RelationalOperator.LESS_THAN:
                    return ValueResult(left_result.value < right_result.value)
                case _:
                    raise Exception(f"unrecognized relational operator: {operator}")

        case UnaryExpression(argument):
            argument_result = interpret(argument, variables)
            if isinstance(argument_result, ErrorResult):
                return argument_result
            if not isinstance(argument_result.value, bool):
                return ErrorResult(f"argument value of unary expression ({argument_result.value}) must be boolean - banana")
            return ValueResult(not argument_result.value)

        case ConditionalExpression(test, consequent, alternate):
            test_result = interpret(test, variables)
            if isinstance(test_result, ErrorResult):
                return test_result
            if not isinstance(test_result.value, bool):
                return ErrorResult(f"test value of conditional expression ({test_result.value}) must be boolean - banana")
            return interpret(consequent, variables) if test_result.value else interpret(alternate, variables)

        case Identifier(name):
            if name not in variables:
                return ErrorResult(f"unbound identifier `{name}` - banana")
            return ValueResult(variables[name])
        
        case FunctionExpression(parameter, body):
            return ValueResult(lambda argument: interpret(body, {**variables, parameter.name: argument}))
        
        case CallExpression(callee, call_expression):
            callee_func = interpret(callee, variables)
            if isinstance(callee_func, ErrorResult):
                return callee_func
            parameter = interpret(call_expression, variables)
            if isinstance(parameter, ErrorResult):
                return parameter
            if not callable(callee_func.value):
                return ErrorResult(f"callee `{callee}` is not a function - banana")
            call_expression_result = callee_func.value(parameter.value)
            if isinstance(call_expression_result, ErrorResult):
                return call_expression_result
            return ValueResult(call_expression_result.value)
        
        # same as Program
        case BlockStatement(body, return_statement):
            for declaration in body:
                variables = interpret(declaration, variables)
                if isinstance(variables, ErrorResult):
                    return variables
            return interpret(return_statement, variables)

        case _ as unreachable:
            raise Exception(f"unreachable code reached: {unreachable}")