import ASTNodeDefs as AST

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    # Move to next character if needed
    def advance(self):
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return ('IDENTIFIER', result)

    def number(self):
        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return ('NUMBER', int(num))

    def token(self):
        while self.current_char is not None:
            # Skip any whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Handles the letters and keywords
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
                    return ('WHILE', 'while')
                return ident

            # Handle numbers
            if self.current_char.isdigit():
                return self.number()

            # Handles operators and symbols
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('EQUALS', '==')
                return ('ASSIGN', '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('NEQ', '!=')

            if self.current_char == '<':
                self.advance()
                return ('LESS', '<')

            if self.current_char == '>':
                self.advance()
                return ('GREATER', '>')

            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')

            if self.current_char == '-':
                self.advance()
                return ('MINUS', '-')

            if self.current_char == '*':
                self.advance()
                return ('MULTIPLY', '*')

            if self.current_char == '/':
                self.advance()
                return ('DIVIDE', '/')

            if self.current_char == '(':
                self.advance()
                return ('LPAREN', '(')


            if self.current_char == ')':
                self.advance()
                return ('RPAREN', ')')

            if self.current_char == ':':
                self.advance()
                return ('COLON', ':')


            if self.current_char == ',':
                self.advance()
                return ('COMMA', ',')
            
            raise ValueError(f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)

    def tokenize(self):
        while True:
            token = self.token()
            self.tokens.append(token)

            if token[0] == 'EOF':
                break
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)

    def advance(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)


        else:
            self.current_token = ('EOF', None)

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token[0] != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return statements

    # Parse different types of statements based on the current token
    def statement(self):
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'ASSIGN':
                return self.assign_stmt()
            
            elif self.peek() == 'LPAREN':
                return self.function_call()
            else:
                return self.expression()
        elif self.current_token[0] == 'IF':
            return self.if_stmt()
        
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt()
        else:
            return self.expression()

    # Handle assignment statements like x = 5
    def assign_stmt(self):
        identifier = self.current_token
        self.advance()  
        self.expect('ASSIGN')
        expression = self.expression()
        return AST.Assignment(identifier, expression)

    # Handles the if statements or the eles
    def if_stmt(self):
        self.advance()  # skip 'if'
        condition = self.boolean_expression()
        self.expect('COLON')

        then_block = self.block()
        
        else_block = None
        if self.current_token[0] == 'ELSE':
            self.advance()
            self.expect('COLON')
            else_block = self.block()
        
        return AST.IfStatement(condition, then_block, else_block)

    # Handle while loops
    def while_stmt(self):
        self.advance() 
        condition = self.boolean_expression()
        self.expect('COLON')
        statements = []
        
        # Parse statements in the  while block until the end
        while self.current_token[0] != 'EOF':
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
           
            if self.peek() == 'WHILE' or self.current_token[0] == 'EOF':
                break
        return AST.WhileStatement(condition, AST.Block(statements))   
    
    def block(self):
        statements = []
        
        while self.current_token[0] not in ['EOF', 'ELSE']:
            stmt = self.statement()
            statements.append(stmt)
            
            if self.current_token[0] == 'EOF' or self.peek() == 'ELSE':
                break
        return AST.Block(statements)
    # CHECK LATER
    def expression(self):
        left = self.term()
        while self.current_token[0] in ['PLUS', 'MINUS']:
            op = self.current_token
            self.advance()
            right = self.term()
            left = AST.BinaryOperation(left, op, right)
        return left

    # Handle easy booleans
    def boolean_expression(self):
        left = self.expression()  # Changed from self.term() to self.expression()
        
        # If we have a comparison operator, create a boolean expression
        if self.current_token[0] in ['EQUALS', 'NEQ', 'GREATER', 'LESS']:
            op = self.current_token
            self.advance()
            right = self.expression()  # Changed from self.term() to self.expression()
            return AST.BooleanExpression(left, op, right)
        
        return left

    # / and *
    def term(self):
        left = self.factor()
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token
            self.advance()
            right = self.factor()
            left = AST.BinaryOperation(left, op, right)
        return left

    # factor
    def factor(self):
        if self.current_token[0] == 'NUMBER':
            val = self.current_token
            self.advance()
            return val
        elif self.current_token[0] == 'IDENTIFIER':
            val = self.current_token
            self.advance()
            return val
        elif self.current_token[0] == 'LPAREN':
            self.advance()  # skip (
            expr = self.expression()
            self.expect('RPAREN')  # expect )
            return expr
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    # function call 
    def function_call(self):
        func_name = self.current_token
        self.advance()
        self.expect('LPAREN')
        
        args = []
        if self.current_token[0] != 'RPAREN':
            args = self.arg_list()
        
        self.expect('RPAREN')
        return AST.FunctionCall(func_name, args)

    # Parse function arguments
    def arg_list(self):
        args = [self.expression()]
        
        while self.current_token[0] == 'COMMA':
            self.advance()
            args.append(self.expression())
        
        return args

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise ValueError(f"Expected {token_type} but got {self.current_token[0]}")

    def peek(self):
        if self.tokens:
            return self.tokens[0][0]
        return None