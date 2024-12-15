import re

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.col})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self, message):
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.col}: {message}")

    def advance(self):
        self.pos += 1
        self.col += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            if self.current_char == '\n':
                self.line +=1
                self.col = 0
            self.advance()

    def number(self):
        result = ''
        has_dot = False
        start_col = self.col
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    self.error("Invalid number format")
                has_dot = True
            result += self.current_char
            self.advance()
        return Token('NUMBER', float(result) if has_dot else int(result), self.line, start_col)

    def string(self):
        result = ''
        start_col = self.col
        self.advance()  # Skip the '@'
        if self.current_char != '"':
            self.error("Expected '\"' after '@'")
        self.advance()  # Skip the opening quote
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                # Handle escape sequences
                self.advance()
                if self.current_char in ('"', '\\'):
                    result += self.current_char
                else:
                    self.error(f"Invalid escape character: \\{self.current_char}")
            else:
                result += self.current_char
            self.advance()
        if self.current_char != '"':
            self.error("Unterminated string literal")
        self.advance()  # Skip the closing quote
        return Token('STRING', result, self.line, start_col)

    def identifier(self):
        result = ''
        start_col = self.col
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return Token('IDENTIFIER', result, self.line, start_col)

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            self.skip_whitespace()

            if self.current_char is None:
                break
            elif self.current_char.isdigit():
                tokens.append(self.number())
            elif self.current_char == '@':
                tokens.append(self.string())
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.identifier())
            elif self.current_char == '#':
                start_col = self.col
                self.advance()
                if self.current_char == '(':
                    tokens.append(Token('ARRAY_START', '#(', self.line, start_col))
                    self.advance()
                else:
                    self.error("Expected '(' after '#' for array declaration")
            elif self.current_char == '(':
                tokens.append(Token('LPAREN', '(', self.line, self.col))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token('RPAREN', ')', self.line, self.col))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token('DICT_START', '[', self.line, self.col))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token('DICT_END', ']', self.line, self.col))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token('LBRACE', '{', self.line, self.col))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token('RBRACE', '}', self.line, self.col))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token('COMMA', ',', self.line, self.col))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token('SEMI', ';', self.line, self.col))
                self.advance()
            elif self.current_char == '=':
                if self.peek() == '>':
                    start_col = self.col
                    self.advance()
                    self.advance()
                    tokens.append(Token('ARROW', '=>', self.line, start_col))
                else:
                    self.error("Unexpected character '='")
            elif self.current_char == '?':
                start_col = self.col
                self.advance()
                if self.current_char == '{':
                    tokens.append(Token('CONST_EXPR_START', '?{', self.line, start_col))
                    self.advance()
                else:
                    self.error("Expected '{' after '?' for constant expression")
            elif self.current_char in '+-*/':
                tokens.append(Token('OPERATOR', self.current_char, self.line, self.col))
                self.advance()
            else:
                self.error(f"Unexpected character '{self.current_char}'")
        return tokens