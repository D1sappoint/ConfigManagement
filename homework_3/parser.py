class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self):
        self.statements = []

class ConstDeclaration(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ConstExpression(ASTNode):
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

class ArrayLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class DictLiteral(ASTNode):
    def __init__(self, pairs):
        self.pairs = pairs

class VariableReference(ASTNode):
    def __init__(self, name):
        self.name = name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if tokens else None

    def error(self, message):
        if self.current_token:
            raise SyntaxError(f"Parser error at line {self.current_token.line}, column {self.current_token.col}: {message}")
        else:
            raise SyntaxError(f"Parser error: {message}")


    def advance(self):
        self.pos +=1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def consume(self, token_type):
        if self.current_token is not None and self.current_token.type == token_type:
            self.advance()
        else:
            self.error(f"Expected token type '{token_type}', got '{self.current_token.type}'")

    def parse(self):
        program = Program()
        while self.current_token is not None:
            if self.current_token.type == 'IDENTIFIER':
                node = self.const_declaration()
                program.statements.append(node)
            else:
                self.error("Expected a constant declaration")
        return program

    def const_declaration(self):
        name = self.current_token.value
        self.consume('IDENTIFIER')
        if self.current_token.type == 'IDENTIFIER' and self.current_token.value == 'is':
            self.consume('IDENTIFIER')  # consume 'is'
        else:
            self.error("Expected 'is' in constant declaration")
        if self.current_token.type in ('NUMBER', 'STRING', 'ARRAY_START', 'DICT_START', 'CONST_EXPR_START', 'IDENTIFIER'):
            value = self.value()
        else:
            self.error("Expected a value in constant declaration")
        self.consume('SEMI')
        return ConstDeclaration(name, value)

    def value(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.advance()
            return token.value
        elif token.type == 'STRING':
            self.advance()
            return token.value
        elif token.type == 'ARRAY_START':
            return self.array_literal()
        elif token.type == 'DICT_START':
            return self.dict_literal()
        elif token.type == 'CONST_EXPR_START':
            return self.const_expression()
        elif token.type == 'IDENTIFIER':
            name = token.value
            self.advance()
            return VariableReference(name)  # Variable reference node
        else:
            self.error(f"Unexpected token '{token.type}' in value")

    def array_literal(self):
        elements = []
        self.consume('ARRAY_START')
        while self.current_token.type != 'RPAREN':
            elements.append(self.value())
            if self.current_token.type == 'COMMA':
                self.consume('COMMA')
            elif self.current_token.type != 'RPAREN':
                self.error("Expected ',' or ')' in array declaration")
        self.consume('RPAREN')
        return ArrayLiteral(elements)

    def dict_literal(self):
        pairs = []
        self.consume('DICT_START')
        while self.current_token.type != 'DICT_END':
            if self.current_token.type != 'IDENTIFIER':
                self.error("Expected identifier in dictionary key")
            key = self.current_token.value
            self.consume('IDENTIFIER')
            self.consume('ARROW')
            value = self.value()
            pairs.append((key, value))
            if self.current_token.type == 'COMMA':
                self.consume('COMMA')
            elif self.current_token.type != 'DICT_END':
                self.error("Expected ',' or ']' in dictionary declaration")
        self.consume('DICT_END')
        return DictLiteral(pairs)

    def const_expression(self):
        operands = []
        self.consume('CONST_EXPR_START')
        if self.current_token.type in ('OPERATOR', 'IDENTIFIER'):
            operator = self.current_token.value
            self.advance()
        else:
            self.error(f"Expected operator, got '{self.current_token.type}'")
        while self.current_token.type != 'RBRACE':
            if self.current_token is None:
                self.error("Unexpected end of input in constant expression")
            operands.append(self.value())
        self.consume('RBRACE')
        return ConstExpression(operator, operands)