import sys
import json
import js_parser

raw_in = sys.stdin.read()
es_tree = json.loads(raw_in)
parsed = js_parser.parse(es_tree)
string_representation = js_parser.to_string(parsed)

print(string_representation)