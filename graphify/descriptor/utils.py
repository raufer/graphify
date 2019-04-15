import re

from typing import Dict


def compile_patterns(descriptor):
    """
    Compile the description components that are regex patterns
    This will increase the both speed and easiness in using the descriptor
    """
    descriptor_copy = dict(descriptor)

    to_compile = ['patterns', 'exclude']

    for k, v in descriptor_copy.items():

        if k.lower() in to_compile:
            compiled = [_compile(p) if isinstance(p, str) else p for p in v]
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

    return descriptor


def extend_internal_patterns(descriptor: Dict) -> Dict:
    """
    Utility method. Given a descriptor configuration extend the patterns to support internal patterns
    e.g. 'patterns': [r'(?:\[\[A\]\]|A)', r'(?:\[\[B\]\]|B)', r'(?:\[\[C\]\]|C)']
    If the pattern has the following pattern '[[X]]' we also mark them to be excluded after parsing
    """
    patterns = [rf"(?:\[\[({p})\]\]|({p}))" for p in descriptor['patterns']]
    exclude = [rf"\[\[{p}\]\]\s?" for p in descriptor['patterns']]

    descriptor['patterns'] = patterns
    descriptor['exclude'] = descriptor.get('exclude', []) + exclude
    return descriptor
