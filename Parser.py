import ASTNodeDefs as AST

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    def advance(self):
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return ('IDENTIFIER', result)

    def number(self):
        num = ''
        while self.current_char and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return ('NUMBER', int(num))

    def token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                if ident[1] == 'else':
                    return ('ELSE', 'else')
                if ident[1] == 'while':
                    return ('WHILE', 'while')
                return ident

            if self.current_char.isdigit():
                return self.number()

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
            
            raise ValueError(f"Invalid character: {self.current_char}")

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
            statements.append(self.statement())
        return statements

    def statement(self):
        token = self.current_token[0]
        if token == 'IDENTIFIER':
            peek = self.peek()
            if peek == 'ASSIGN':
                return self.assign_stmt()
            if peek == 'LPAREN':
                return self.function_call()
            return self.expression()
        if token == 'IF':
            return self.if_stmt()
        if token == 'WHILE':
            return self.while_stmt()
        return self.expression()

    def assign_stmt(self):
        identifier = self.current_token
        self.advance()
        self.expect('ASSIGN')
        expr = self.expression()
        return AST.Assignment(identifier, expr)

    #COME BACK TO LATER, Test case is not showing
    def if_stmt(self):
        self.advance()
        condition = self.boolean_expression()
        self.expect('COLON')
        then_block = self.block()
        
        else_block = None
        if self.current_token[0] == 'ELSE':
            self.advance()
            self.expect('COLON')
            else_block = self.block()
        
        return AST.IfStatement(condition, then_block, else_block)

    def while_stmt(self):
        self.advance()
        condition = self.boolean_expression()
        self.expect('COLON')
        block = self.block()
        return AST.WhileStatement(condition, block)
    
    def block(self):
        statements = []
        while self.current_token[0] not in ['EOF', 'ELSE']:
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            if self.current_token[0] == 'EOF' or self.peek() == 'ELSE':
                break
            if self.peek() == 'WHILE' and self.current_token[0] != 'WHILE':
                break
        return AST.Block(statements)

    def expression(self):
        left = self.term()
        while self.current_token[0] in ['PLUS', 'MINUS']:
            op = self.current_token
            self.advance()
            right = self.term()
            left = AST.BinaryOperation(left, op, right)
        return left

    def boolean_expression(self):
        left = self.expression()
        if self.current_token[0] in ['EQUALS', 'NEQ', 'GREATER', 'LESS']:
            op = self.current_token
            self.advance()
            right = self.expression()
            return AST.BooleanExpression(left, op, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token
            self.advance()
            right = self.factor()
            left = AST.BinaryOperation(left, op, right)
        return left

    def factor(self):
        token = self.current_token
        if token[0] == 'NUMBER':
            self.advance()
            return token
        
        if token[0] == 'IDENTIFIER':
            self.advance()
            return token
        
        if token[0] == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        
        raise ValueError(f"Unexpected token: {token}")

    def function_call(self):
        func_name = self.current_token
        self.advance()
        self.expect('LPAREN')
        args = []
        if self.current_token[0] != 'RPAREN':
            args = self.arg_list()
        self.expect('RPAREN')

        return AST.FunctionCall(func_name, args)

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
            raise ValueError(f"Expected {token_type}, got {self.current_token[0]}")

    def peek(self):
        return self.tokens[0][0] if self.tokens else None