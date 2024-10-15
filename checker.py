
# Example visible test case
test_input_1 = """
x = 5
y = y + x
"""

expected_output_1 = """
Assignment(('IDENTIFIER', 'x'), ('NUMBER', 5))
Assignment(('IDENTIFIER', 'y'), BinaryOperation(('IDENTIFIER', 'y'), ('PLUS', '+'), ('IDENTIFIER', 'x')))
"""




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


test_input_6 = """
x = 1
while x < 100:
  foo(x)
"""

expected_output_6 = """
Assignment(('IDENTIFIER', 'x'), ('NUMBER', 1))
WhileStatement(BooleanExpression(('IDENTIFIER', 'x'), ('LESS', '<'), ('NUMBER', 100)), Block([FunctionCall(('IDENTIFIER', 'foo'), [('IDENTIFIER', 'x')])]))
"""


test_input_7 = """
foo(x)
bar(z)
"""


expected_output_7 = """
FunctionCall(('IDENTIFIER', 'foo'), [('IDENTIFIER', 'x')])
FunctionCall(('IDENTIFIER', 'bar'), [('IDENTIFIER', 'z')])
"""