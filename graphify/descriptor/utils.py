import re

from typing import Dict
from graphify.descriptor.constants.patterns import DATA_NAMED_GROUP


def compile_patterns(descriptor):
    """
    Compile the description components that are regex patterns
    This will increase the both speed and easiness in using the descriptor
    """
    descriptor_copy = dict(descriptor)

    to_compile = ['patterns', 'exclude']

    compile = lambda p: _compile(p) if isinstance(p, str) else p

    for k, v in descriptor_copy.items():

        if k.lower() in to_compile:
            compiled = [[compile(i) for i in p] if isinstance(p, (tuple, list)) else compile(p) for p in v]
            descriptor_copy[k] = compiled

    return descriptor_copy


def _compile(pattern):
    """
    Compile a pattern (or list of pattern) into a 're'
    """

    # flags = re.VERBOSE | re.MULTILINE | re.IGNORECASE

    if isinstance(pattern, list):
        result = [re.compile(p) for p in pattern]
    else:
        result = re.compile(pattern)

    return result


def normalize_descriptor(descriptor):
    """
    The parsing logic might assume the user describes specific behaviour on the descriptor
    If not, some defaults can be used to facilitate the use of the parsing

    Returns a new descriptor with default behaviours
    """
    descriptor = descriptor.copy()

    stopParsing = descriptor.get('stopParsing', None)
    if not stopParsing:
        descriptor['stopParsing'] = lambda x: False
    elif isinstance(stopParsing, str):
        compiled = _compile(stopParsing)
        descriptor['stopParsing'] = lambda x: bool(compiled.search(x))

    startParsing = descriptor.get('startParsing', None)
    if not startParsing:
        descriptor['startParsing'] = lambda x: False
    elif isinstance(startParsing, str):
        compiled = _compile(startParsing)
        descriptor['startParsing'] = lambda x: not bool(compiled.search(x))

    if 'padding' not in descriptor:
        descriptor['padding'] = False

    if 'exclude' not in descriptor:
        descriptor['exclude'] = []

    # standard model to process patterns:
    descriptor['patterns'] = [[p] if not isinstance(p, (list, tuple)) else p for p in descriptor['patterns']]

    return descriptor


def extend_internal_patterns(descriptor: Dict) -> Dict:
    """
    Utility method. Given a descriptor configuration extend the patterns to support internal patterns
    e.g. 'patterns': [r'(?:\[\[A\]\]|A)', r'(?:\[\[B\]\]|B)', r'(?:\[\[C\]\]|C)']
    If the pattern has the following pattern '[[X]]' we also mark them to be excluded after parsing
    """
    descriptor = descriptor.copy()

    make_pattern = lambda p: rf"(?:\[\[({p})\]\]|({p}))"
    make_exclude = lambda p: rf"\[\[{p}\]\]\s?"

    patterns = [make_pattern(p) if isinstance(p, str) else [make_pattern(i) for i in p] for p in descriptor['patterns']]
    exclude = [[make_exclude(p)] if isinstance(p, str) else [make_exclude(i) for i in p] for p in descriptor['patterns']]

    descriptor['patterns'] = patterns
    descriptor['exclude'] = descriptor.get('exclude', []) + sum(exclude, [])
    return descriptor


def extend_descriptor_with_data_capture_group(descriptor: Dict) -> Dict:
    """
    Extends each `pattern` of a descriptor with the ability
    to capture a data object of the form data :: {...}

    This would be useful so that the user can inject custom fields
    at construction time of the raw input document

    e.g. a pattern like `[[Chapter]]` would result in `[[Chapter]]{...}`
    The `{...}` is a named capture group and should be a valid
    python dictionary (to be materialized via `eval`)
    """
    descriptor = descriptor.copy()
    make_pattern = lambda pattern: f'(?P<component>{pattern}){DATA_NAMED_GROUP}'

    descriptor['patterns'] = [
        make_pattern(pattern) if isinstance(pattern, str) else [make_pattern(p) for p in pattern]
        for pattern in descriptor['patterns']
    ]

    return descriptor


def parse_custom_data_object(match: re.Match) -> Dict:
    """
    Given a `match` parse its `data` named capture group
    and return a materialized dictionary
    Otherwise return an empty dict
    """
    data_str = match.groupdict().get('data') or '{}'

    try:
        data = eval(data_str)
        return data
    except Exception as e:
        raise ValueError(f"Invalid custom data object in '{data_str}'")


