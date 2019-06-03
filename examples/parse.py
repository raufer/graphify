import json

from pprint import pprint
from graphify.parsing import parse_filepath

descriptor = {
    'components': ['Chapter', 'Article', 'Paragraph'],
    'patterns': [r'CHAPTER', r'ARTICLE', r'PARAGRAPH']
}

input = '/Users/raulferreira/waymark/experiments/similarity/documents/caversandco-aml-policy-v1.txt'
output = '/Users/raulferreira/waymark/experiments/similarity/documents/caversandco-aml-policy-v1.json'

doc = parse_filepath(input, descriptor)
d = doc.to_dict()

with open(output, 'w') as f:
    json.dump(d, f, indent=4)

for i, n in enumerate(doc.traverse()):
    print(n)
    if i > 2:
        break



