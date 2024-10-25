import ASTNodeDefs as AST

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    # Move to the next position in the code.
    def advance(self):
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None
    # Skip whitespaces.
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace(): 
            self.advance()
    # Tokenize an identifier.
    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
    
        if result == 'if':
            return ('IF', result)
        elif result == 'else':
            return ('ELSE', result)
        elif result == 'while':
            return ('WHILE', result)
        else:
            return ('IDENTIFIER', result)

    # Tokenize a number.
    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ('NUMBER', int(result))
    

    def token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
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

            raise ValueError(f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)

    # Collect all tokens into a list.
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
        self.current_token = tokens.pop(0)  # Start with the first token

    def advance(self):
        # Move to the next token in the list.
        

        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = ('EOF', None)
    def parse(self):
        """
        Entry point for the parser. It will process the entire program.
        """
        return self.program()

    def program(self):
        """
        Program consists of multiple statements.
        """
        statements = []
        while self.current_token[0] != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return statements

    def statement(self):
        """
        Determines which type of statement to parse.
        - If it's an identifier, it could be an assignment or function call.
        - If it's 'if', it parses an if-statement.
        - If it's 'while', it parses a while-statement.
        
        """
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':  # Assignment
                return self.assign_stmt() #AST of assign_stmt
            elif self.peek() == 'LPAREN':  # Function call
                return self.function_call() #AST of function call
            else:
                raise ValueError(f"Unexpected token after identifier: {self.current_token}")
        elif self.current_token[0] == 'IF':
            return self.if_stmt()#AST of if stmt
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt()#AST of while stmt
        else:
            return self.expression()
            # raise ValueError(f"Unexpected token: {self.current_token}")

    def assign_stmt(self):
        """
        Parses assignment statements.
        Example:
        x = 5 + 3
        
        """
        identifier = self.current_token
        self.advance()  # Skip identifier
        self.expect('ASSIGN')  # Skip =
        expression = self.expression()
        return AST.Assignment(identifier, expression)

    

    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition:
            # statements
        else:
            # statements
        """
        self.advance()  # Skip 'if'
        condition = self.boolean_expression()
        self.expect('COLON')
        then_block = self.block()
        else_block = None
        
        if self.current_token[0] == 'ELSE':
            self.advance()  # Skip 'else'
            self.expect('COLON')
            else_block = self.block()
        
        return AST.IfStatement(condition, then_block, else_block)

    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition:
            # statements
       
        """
        
        
        self.advance()  # Skip 'while'
        condition = self.boolean_expression()
        self.expect('COLON')
        block = self.block()
        return AST.WhileStatement(condition, block)


    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by indentation.
        Example:
        if condition:
            # This is a block
            x = 5
            y = 10
        
        """
        statements = []
        while self.current_token[0] not in ['EOF', 'ELSE'] and self.peek() != 'ELSE':
            stmt = self.statement()
            statements.append(stmt)
        return AST.Block(statements)

    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        
        """
        left = self.term()
        while self.current_token[0] in ['PLUS', 'MINUS']:  # Handle + and -
            
            op = self.current_token  # Capture the operator
            self.advance()  # Skip the operator
            right = self.term()  # Parse the next term
            left = AST.BinaryOperation(left, op, right)
    
        return left
        
    

    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        
        """
        # write your code here, for reference check expression function
        left = self.term()
        while self.current_token[0] in ['EQUALS', 'NEQ', 'GREATER', 'LESS']:
            op = self.current_token
            self.advance()
            right = self.term()
            left = AST.BooleanExpression(left, op, right)
        return left

    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        
        """
        # write your code here, for reference check expression function
        left = self.factor()
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token
            self.advance()
            right = self.factor()
            left = AST.BinaryOperation(left, op, right)
        return left 

    def factor(self):
        """
        Parses a factor. Factors are the basic building blocks of expressions.
        Example:
        - A number
        - An identifier (variable)
        - A parenthesized expression
        
        """
        if self.current_token[0] == 'NUMBER':
            token = self.current_token
            self.advance()
            return token
        elif self.current_token[0] == 'IDENTIFIER':
            token = self.current_token
            self.advance()
            return token
        elif self.current_token[0] == 'LPAREN':
            self.advance()  # Skip '('
            expr = self.expression()
            self.expect('RPAREN')  # Expect and skip ')'
            return expr
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        """
        Parses a function call.
        Example:
        myFunction(arg1, arg2)
        
        """
        func_name = self.current_token
        self.advance()  # Skip function name
        self.expect('LPAREN')
    
        args = []
        if self.current_token[0] != 'RPAREN':
            args = self.arg_list()
    
        self.expect('RPAREN')
        
        return AST.FunctionCall(func_name, args)

    def arg_list(self):
        """
        Parses a list of arguments in a function call.
        Example:
        arg1, arg2, arg3
        
        """
        args = []
        args.append(self.expression())
    
        while self.current_token[0] == 'COMMA':
            self.advance()  # Skip comma
            args.append(self.expression())
    
        return args

    def expect(self, token_type):
       
        if self.current_token[0] == token_type:
            self.advance()  # Move to the next token
        else:
            raise ValueError(f"Expected {token_type} but got {self.current_token[0]}")

    def peek(self):
        if self.tokens:
            return self.tokens[0][0]
        else:
            return None
