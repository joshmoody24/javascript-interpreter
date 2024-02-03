import sys
import json
import js_parser
import js_interpreter

parse_only = sys.argv[1] == "parse"

raw_in = sys.stdin.read()
if not raw_in:
    print("No input provided. Exiting.")
    sys.exit(1)
es_tree = json.loads(raw_in)
parsed = js_parser.parse(es_tree)
if parse_only:
    print(js_parser.to_string(parsed))
    sys.exit(0)
result = js_interpreter.interpret(parsed)
print(js_interpreter.to_string(result))