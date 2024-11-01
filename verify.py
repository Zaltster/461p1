import Parser as p0

count = 0
def run_test(test_input, expected_output):
    """
    This function runs the lexer and parser on the test input,
    compares the parsed AST with the expected output, and returns the result.
    """
    global count
    # Initialize the lexer and tokenize the input
    lexer = p0.Lexer(test_input)
    tokens = lexer.tokenize()

    # Initialize the parser and generate the AST
    parser = p0.Parser(tokens)
    ast = parser.parse()

    # Convert the AST to string format using to_string() for comparison
    result = ""
    for node in ast:
        result += node.to_string()  # Use to_string() method for each AST node

    # Remove all spaces and newlines from both result and expected_output for comparison
    result = result.replace(" ", "").replace("\n", "")
    expected_output = expected_output.replace(" ", "").replace("\n", "")

    # Compare the result with the expected output
    if result == expected_output:
        print("Test passed.")
        count += 1
    else:
        print("Test failed.")
        print("Expected:")
        print(expected_output)
        print("Got:")
        print(result)


# Example visible test case
test_input_1 = """
x = 5
y = y + x
"""

expected_output_1 = """
Assignment(('IDENTIFIER', 'x'), ('NUMBER', 5))
Assignment(('IDENTIFIER', 'y'), BinaryOperation(('IDENTIFIER', 'y'), ('PLUS', '+'), ('IDENTIFIER', 'x')))
"""

# Run the test
run_test(test_input_1, expected_output_1)


test_input_2 = """
x = 1
y = 2
foo(x + y)
"""

expected_output_2 = """
Assignment(('IDENTIFIER', 'x'), ('NUMBER', 1))
Assignment(('IDENTIFIER', 'y'), ('NUMBER', 2))
FunctionCall(('IDENTIFIER', 'foo'), [BinaryOperation(('IDENTIFIER', 'x'), ('PLUS', '+'), ('IDENTIFIER', 'y'))])
"""

run_test(test_input_2, expected_output_2)

test_input_3 = """
x10Small = 10
xVar20 = 20
y = x10Small * xVar20 / 10
"""

expected_output_3 = """
Assignment(('IDENTIFIER', 'x10Small'), ('NUMBER', 10))
Assignment(('IDENTIFIER', 'xVar20'), ('NUMBER', 20))
Assignment(('IDENTIFIER', 'y'), BinaryOperation(BinaryOperation(('IDENTIFIER', 'x10Small'), ('MULTIPLY', '*'), ('IDENTIFIER', 'xVar20')), ('DIVIDE', '/'), ('NUMBER', 10)))
"""

run_test(test_input_3, expected_output_3)

test_input_4 = """
x = 1
y = 2
z = 3
x = x * y + z
y = y + x / z
if x != y:
  z = 100
"""

expected_output_4 = """
Assignment(('IDENTIFIER', 'x'), ('NUMBER', 1))
Assignment(('IDENTIFIER', 'y'), ('NUMBER', 2))
Assignment(('IDENTIFIER', 'z'), ('NUMBER', 3))
Assignment(('IDENTIFIER', 'x'), BinaryOperation(BinaryOperation(('IDENTIFIER', 'x'), ('MULTIPLY', '*'), ('IDENTIFIER', 'y')), ('PLUS', '+'), ('IDENTIFIER', 'z')))
Assignment(('IDENTIFIER', 'y'), BinaryOperation(('IDENTIFIER', 'y'), ('PLUS', '+'), BinaryOperation(('IDENTIFIER', 'x'), ('DIVIDE', '/'), ('IDENTIFIER', 'z'))))
IfStatement(BooleanExpression(('IDENTIFIER', 'x'), ('NEQ', '!='), ('IDENTIFIER', 'y')), Block([Assignment(('IDENTIFIER', 'z'), ('NUMBER', 100))]), None)
"""

run_test(test_input_4, expected_output_4)

test_input_5 = """
x = 10
y = 20
foo(x, y)
bar(x)
if x > 10:
  y = 20
else:
  y = 0
"""

expected_output_5 = """
Assignment(('IDENTIFIER', 'x'), ('NUMBER', 10))
Assignment(('IDENTIFIER', 'y'), ('NUMBER', 20))
FunctionCall(('IDENTIFIER', 'foo'), [('IDENTIFIER', 'x'), ('IDENTIFIER', 'y')])
FunctionCall(('IDENTIFIER', 'bar'), [('IDENTIFIER', 'x')])
IfStatement(BooleanExpression(('IDENTIFIER', 'x'), ('GREATER', '>'), ('NUMBER', 10)), Block([Assignment(('IDENTIFIER', 'y'), ('NUMBER', 20))]), Block([Assignment(('IDENTIFIER', 'y'), ('NUMBER', 0))]))
"""

run_test(test_input_5, expected_output_5)

test_input_6 = """
x = 1
while x < 100:
  foo(x)
"""

expected_output_6 = """
Assignment(('IDENTIFIER', 'x'), ('NUMBER', 1))
WhileStatement(BooleanExpression(('IDENTIFIER', 'x'), ('LESS', '<'), ('NUMBER', 100)), Block([FunctionCall(('IDENTIFIER', 'foo'), [('IDENTIFIER', 'x')])]))
"""

run_test(test_input_6, expected_output_6)

test_input_7 = """
foo(x)
bar(z)
"""


expected_output_7 = """
FunctionCall(('IDENTIFIER', 'foo'), [('IDENTIFIER', 'x')])
FunctionCall(('IDENTIFIER', 'bar'), [('IDENTIFIER', 'z')])
"""

run_test(test_input_7, expected_output_7)


print(count)