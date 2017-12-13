import re


def compile_patterns(descriptor):
    """
    Compile the description components that are regex patterns
    This will increase the both speed and easiness in using the descriptor
    """
    descriptor_copy = dict(descriptor)

    for k, v in descriptor_copy.items():

        if 'pattern' in k.lower():
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
