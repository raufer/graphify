import re


def remove_descriptor_indicators(line: str, match: re.Match) -> str:
    """
    Whenever a hit occurs for a given line, we need to
    remove the artificial indicators that were introduced
    just to provide hierarchical information.

    Note: we follow the convention that if the indicator was
    wrapped within double brackets ``[[...]]` then  it is an
    artificial one.

    Additionally we remove any custom data inject by the user
    """
    component_str = match.groupdict()['component']
    data_str = match.groupdict().get('data') or ''

    if all(['[[' in line]):
        line = line.replace(component_str, '').lstrip()

    line = line.replace(data_str, '').lstrip()
    return line

