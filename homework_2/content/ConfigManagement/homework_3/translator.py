import argparse
import sys
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

def main():
    parser = argparse.ArgumentParser(description='Educational Configuration Language Translator')
    parser.add_argument('--input', required=True, help='Path to the input configuration file')
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.")
        sys.exit(1)

    lexer = Lexer(input_text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    evaluator = Evaluator()
    result = evaluator.evaluate(ast)

    toml_output = evaluator.to_toml(result)
    print(toml_output)

if __name__ == '__main__':
    main()
