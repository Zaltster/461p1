import ASTNodeDefs as AST

DEBUG = True

def debug_print(msg, *args):
    if DEBUG:
        if args:
            print(f"DEBUG: {msg}", *args)
        else:
            print(f"DEBUG: {msg}")

class Lexer:
    def __init__(self, code):
        debug_print("Initializing lexer with code length:", len(code))
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    def advance(self):
        debug_print(f"Lexer advancing from position {self.position}")
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        debug_print("Skipping whitespace")
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def identifier(self):
        debug_print("Processing identifier")
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        debug_print(f"Identified token: {result}")
        return ('IDENTIFIER', result)

    def number(self):
        debug_print("Processing number")
        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        debug_print(f"Found number: {num}")
        return ('NUMBER', int(num))

    def token(self):
        debug_print("\n=== Token Processing ===")
        while self.current_char is not None:
            debug_print(f"Current char: {self.current_char}")
            
            if self.current_char.isspace():
                debug_print("Found whitespace")
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                debug_print("Found letter")
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

            # Handle operators and symbols
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    debug_print("Found equals operator")
                    return ('EQUALS', '==')
                debug_print("Found assignment operator")
                return ('ASSIGN', '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    debug_print("Found not equals operator")
                    return ('NEQ', '!=')

            if self.current_char == '<':
                self.advance()
                debug_print("Found less than operator")
                return ('LESS', '<')

            if self.current_char == '>':
                self.advance()
                debug_print("Found greater than operator")
                return ('GREATER', '>')

            if self.current_char == '+':
                self.advance()
                debug_print("Found plus operator")
                return ('PLUS', '+')

            if self.current_char == '-':
                self.advance()
                debug_print("Found minus operator")
                return ('MINUS', '-')

            if self.current_char == '*':
                self.advance()
                debug_print("Found multiply operator")
                return ('MULTIPLY', '*')

            if self.current_char == '/':
                self.advance()
                debug_print("Found divide operator")
                return ('DIVIDE', '/')

            if self.current_char == '(':
                self.advance()
                debug_print("Found left parenthesis")
                return ('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                debug_print("Found right parenthesis")
                return ('RPAREN', ')')

            if self.current_char == ':':
                self.advance()
                debug_print("Found colon")
                return ('COLON', ':')

            if self.current_char == ',':
                self.advance()
                debug_print("Found comma")
                return ('COMMA', ',')
            
            error_msg = f"Illegal character at position {self.position}: {self.current_char}"
            debug_print("ERROR:", error_msg)
            raise ValueError(error_msg)

        debug_print("Reached end of input")
        return ('EOF', None)

    def tokenize(self):
        debug_print("Starting tokenization")
        while True:
            token = self.token()
            self.tokens.append(token)
            debug_print(f"Added token: {token}")

            if token[0] == 'EOF':
                break
        debug_print(f"Tokenization complete. Total tokens: {len(self.tokens)}")
        return self.tokens


class Parser:
    def __init__(self, tokens):
        debug_print("Initializing parser with tokens:", tokens[:5], "...")
        self.tokens = tokens
        self.current_token = tokens.pop(0)

    def advance(self):
        debug_print(f"Advancing from token: {self.current_token}")
        if self.tokens:
            self.current_token = self.tokens.pop(0)
            debug_print(f"Advanced to: {self.current_token}")
        else:
            self.current_token = ('EOF', None)
            debug_print("Advanced to EOF")

    def parse(self):
        debug_print("Starting parsing")
        return self.program()

    def program(self):
        debug_print("\n=== Program Parser ===")
        statements = []
        while self.current_token[0] != 'EOF':
            debug_print(f"Processing program statement, current token: {self.current_token}")
            stmt = self.statement()
            statements.append(stmt)
            debug_print(f"Added statement to program: {stmt}")
        return statements

    def statement(self):
        debug_print("\n=== Statement Parser ===")
        debug_print(f"Current token: {self.current_token}")
        debug_print(f"Next token: {self.peek()}")
        
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'ASSIGN':
                debug_print("Processing assignment")
                return self.assign_stmt()
            elif self.peek() == 'LPAREN':
                debug_print("Processing function call")
                return self.function_call()
            else:
                debug_print("Processing expression")
                return self.expression()
        elif self.current_token[0] == 'IF':
            debug_print("Processing if statement")
            return self.if_stmt()
        elif self.current_token[0] == 'WHILE':
            debug_print("Processing while statement")
            return self.while_stmt()
        else:
            debug_print("Processing expression")
            return self.expression()

    def assign_stmt(self):
        debug_print("\n=== Assignment Statement ===")
        identifier = self.current_token
        self.advance()
        self.expect('ASSIGN')
        expression = self.expression()
        result = AST.Assignment(identifier, expression)
        debug_print(f"Created assignment: {result}")
        return result

    def if_stmt(self):
        debug_print("\n=== If Statement ===")
        self.advance()
        condition = self.boolean_expression()
        debug_print(f"If condition: {condition}")
        
        self.expect('COLON')
        then_block = self.block()
        debug_print(f"Then block: {then_block}")
        
        else_block = None
        if self.current_token[0] == 'ELSE':
            debug_print("Processing else block")
            self.advance()
            self.expect('COLON')
            else_block = self.block()
            debug_print(f"Else block: {else_block}")
        
        result = AST.IfStatement(condition, then_block, else_block)
        debug_print(f"Created if statement: {result}")
        return result

    def while_stmt(self):
        debug_print("\n=== While Statement ===")
        debug_print(f"Current token: {self.current_token}")
        debug_print(f"Next tokens: {self.tokens[:3]}")
        
        self.advance()
        condition = self.boolean_expression()
        debug_print(f"While condition: {condition}")
        
        self.expect('COLON')
        debug_print(f"Before block: {self.current_token}")
        
        block = self.block()
        debug_print(f"While block: {block}")
        
        result = AST.WhileStatement(condition, block)
        debug_print(f"Created while statement: {result}")
        return result

    def block(self):
        debug_print("\n=== Block Parser ===")
        debug_print(f"Starting block with: {self.current_token}")
        statements = []
        
        while self.current_token[0] not in ['EOF', 'ELSE']:
            debug_print(f"Processing block statement: {self.current_token}")
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
                debug_print(f"Added to block: {stmt}")
            
            debug_print(f"After statement - Current: {self.current_token}, Next: {self.peek()}")
            
            if self.current_token[0] == 'EOF' or self.peek() == 'ELSE':
                debug_print("Block end: EOF or ELSE")
                break
            
            if self.peek() == 'WHILE' and self.current_token[0] != 'WHILE':
                debug_print("Block end: new WHILE")
                break
        
        result = AST.Block(statements)
        debug_print(f"Completed block: {result}")
        return result

    def expression(self):
        debug_print("\n=== Expression Parser ===")
        left = self.term()
        debug_print(f"Initial term: {left}")
        
        while self.current_token[0] in ['PLUS', 'MINUS']:
            op = self.current_token
            debug_print(f"Found operator: {op}")
            self.advance()
            right = self.term()
            debug_print(f"Right term: {right}")
            left = AST.BinaryOperation(left, op, right)
            debug_print(f"Created operation: {left}")
        
        return left

    def boolean_expression(self):
        debug_print("\n=== Boolean Expression ===")
        left = self.expression()
        debug_print(f"Left side: {left}")
        
        if self.current_token[0] in ['EQUALS', 'NEQ', 'GREATER', 'LESS']:
            operator = self.current_token
            debug_print(f"Boolean operator: {operator}")
            self.advance()
            right = self.expression()
            debug_print(f"Right side: {right}")
            return AST.BooleanExpression(left, operator, right)
        
        return left

    def term(self):
        debug_print("\n=== Term Parser ===")
        left = self.factor()
        debug_print(f"Initial factor: {left}")
        
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token
            debug_print(f"Found operator: {op}")
            self.advance()
            right = self.factor()
            debug_print(f"Right factor: {right}")
            left = AST.BinaryOperation(left, op, right)
        
        return left

    def factor(self):
        debug_print("\n=== Factor Parser ===")
        debug_print(f"Current token: {self.current_token}")
        
        if self.current_token[0] == 'NUMBER':
            val = self.current_token
            self.advance()
            debug_print(f"Found number: {val}")
            return val
        elif self.current_token[0] == 'IDENTIFIER':
            val = self.current_token
            self.advance()
            debug_print(f"Found identifier: {val}")
            return val
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.expression()
            debug_print(f"Parsed parenthesized expression: {expr}")
            self.expect('RPAREN')
            return expr
        else:
            error_msg = f"Unexpected token in factor: {self.current_token}"
            debug_print("ERROR:", error_msg)
            raise ValueError(error_msg)

    def function_call(self):
        debug_print("\n=== Function Call ===")
        func_name = self.current_token
        debug_print(f"Function name: {func_name}")
        
        self.advance()
        self.expect('LPAREN')
        
        args = []
        if self.current_token[0] != 'RPAREN':
            args = self.arg_list()
        debug_print(f"Function arguments: {args}")
        
        self.expect('RPAREN')
        result = AST.FunctionCall(func_name, args)
        debug_print(f"Created function call: {result}")
        return result

    def arg_list(self):
        debug_print("\n=== Argument List ===")
        args = [self.expression()]
        debug_print(f"First argument: {args[0]}")
        
        while self.current_token[0] == 'COMMA':
            self.advance()
            arg = self.expression()
            args.append(arg)
            debug_print(f"Added argument: {arg}")
        
        return args

    def expect(self, token_type):
        debug_print(f"Expecting token type: {token_type}")
        if self.current_token[0] == token_type:
            self.advance()
        else:
            error_msg = f"Expected {token_type} but got {self.current_token[0]}"
            debug_print("ERROR:", error_msg)
            raise ValueError(error_msg)

    def peek(self):
        if self.tokens:
            debug_print(f"Peeking at next token: {self.tokens[0][0]}")
            return self.tokens[0][0]
        debug_print("No more tokens to peek at")
        return None