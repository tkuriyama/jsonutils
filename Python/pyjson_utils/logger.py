"""Convert dict objects from json_lws to pretty print strings.

"""

from collections import defaultdict

def trim(n):
    """Return a function that accepts a string and trims it to n chars."""
    def inner(string):
        return string[:n]
    return inner

def parse_config(config):
    """Parse config dictionary, return default values if necessary."""
    sep = config['sep'] if 'sep' in config else ': '
    indent = config['indent'] if 'indent' in config else ' -- '
    trim_key = trim(config['trim_key']) if 'trim_key' in config else trim(20)
    trim_val = trim(config['trim_val']) if 'trim_val' in config else trim(20)
    return sep, indent, trim_key, trim_val

def is_iter(arg):
    """Return True if argument is iterable."""
    return isinstance(arg, list) or isinstance(arg, tuple)

def format_node(text, indent, depth):
    """
    Args
        text: string of node to print
        indent: string of tree indentation chars
        depth: int of tree depth, 0 = root
    Returns
        Formatted string.
    """
    space = ' ' * ((len(indent) + 1) * (depth - 2))
    leader = '|' + indent if depth > 1 else ''
    return space + leader + text

def filter_values(vals, error):
    """Helper for filter_errors.
    Return single value from list of values if a non-error term exists; else
    return the error term.
    """
    return (vals[0] if len(vals) == 1 else
            error if set(vals) == {error} else
            [v for v in vals if v != error][0])

def filter_errors(pairs, error):
    """
    Args
        pairs: list of tuples
        error:
    Returns
        List of
    """
    keys = defaultdict(list)
    for pair in pairs:
        fst, snd = pair
        keys[fst].append(snd)

    ret_pairs = []
    for key in keys:
        val = filter_values(keys[key], error)
        ret_pairs.append((key, val))

    return ret_pairs

def dict_to_list(d, key, list_tree, error=''):
    """
    Args

    Returns

    """
    if key not in d:
        return list_tree
    else:
        keys = filter_errors(d[key].keys(), error) if error else d[key].keys()
        return list_tree + [dict_to_list(d, x, [x]) for x in keys]

def dict_to_tree(d, mapping={}, config={}):
    """
    Args
        d
        mapping
        config
    Returns

    """

