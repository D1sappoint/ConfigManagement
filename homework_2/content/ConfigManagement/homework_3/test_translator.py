import unittest
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

class TestTranslator(unittest.TestCase):

    def test_number(self):
        input_text = 'num is 42;'
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        result = evaluator.evaluate(ast)
        self.assertEqual(result['num'], 42)

    def test_string(self):
        input_text = '@"Hello, World!"'
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, 'STRING')
        self.assertEqual(tokens[0].value, 'Hello, World!')

    def test_array(self):
        input_text = 'arr is #(1, 2, 3);'
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        result = evaluator.evaluate(ast)
        self.assertEqual(result['arr'], [1, 2, 3])

    def test_dict(self):
        input_text = '''
        dict is [
            key1 => @"value1",
            key2 => 42,
            key3 => #(1,2,3)
        ];
        '''
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        result = evaluator.evaluate(ast)
        expected = {
            'key1': 'value1',
            'key2': 42,
            'key3': [1,2,3]
        }
        self.assertEqual(result['dict'], expected)

    def test_const_expression(self):
        input_text = 'result is ?{+ 1 2};'
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        result = evaluator.evaluate(ast)
        self.assertEqual(result['result'], 3)

    def test_sort_function(self):
        input_text = '''
        arr is #(3, 1, 2);
        sorted_arr is ?{sort arr};
        '''
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        result = evaluator.evaluate(ast)
        self.assertEqual(result['sorted_arr'], [1, 2, 3])

    def test_nested_structures(self):
        input_text = '''
        data is [
            numbers => #(1, 2, 3),
            info => [
                name => @"Test",
                value => ?{* 2 2}
            ]
        ];
        '''
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        result = evaluator.evaluate(ast)
        expected = {
            'numbers': [1, 2, 3],
            'info': {
                'name': 'Test',
                'value': 4
            }
        }
        self.assertEqual(result['data'], expected)

    def test_undefined_variable(self):
        input_text = 'value is missing_var;'
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        with self.assertRaises(Exception) as context:
            evaluator.evaluate(ast)
        self.assertTrue("Undefined variable 'missing_var'" in str(context.exception))

    def test_syntax_error(self):
        input_text = 'value is ;'
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaises(SyntaxError):
            ast = parser.parse()

    def test_invalid_operator(self):
        input_text = 'result is ?{unknown_op 1 2};'
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        with self.assertRaises(Exception) as context:
            evaluator.evaluate(ast)
        self.assertTrue("Unknown operator: unknown_op" in str(context.exception))

    def test_division(self):
        input_text = 'result is ?{/ 10 2};'
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        result = evaluator.evaluate(ast)
        self.assertEqual(result['result'], 5)

if __name__ == '__main__':
    unittest.main()
