"""Convert dict objects from json_lws to pretty print strings.

"""

from collections import defaultdict

# Print Helpers

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

# Data Helpers

def flatten_list(nested):
    """Accepts arbitrarily nested lists and returns generator for flat list."""
    for outer in nested:
        if isinstance(outer, list):
            for inner in flatten_list(outer):
                yield inner
        else:
            yield outer

def filter_errors(vals, error):
    """Helper for filter_keys.
    Return single value from list of values if a non-error term exists; else
    return the error term.
    """
    return (vals[0] if len(vals) == 1 else
            error if set(vals) == {error} else
            [v for v in vals if v != error][0])

def filter_keys(pairs, error):
    """Take list of keys and filter out redundant values.
    Each
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
        val = filter_errors(keys[key], error)
        ret_pairs.append((key, val))

    return ret_pairs

def dict_to_tree(d, key, tree, depth=0, error=''):
    """Transform dict into nested list of values representing tree form.
    Generic function if called
    Args
        d: dict to transform
        key: initial key value ("root" of dict)
        tree: list, usually initialized as singleton [(key, 0)]
        error: error value to filter for, optioanl
    Returns
        Nested list of values.
    """
    if key not in d:
        return tree
    else:
        keys = filter_keys(d[key], error) if error else d[key]
        return tree + [dict_to_tree(d, x, [(x, depth + 1)], depth + 1)
                       for x in keys]

def dict_to_tree(d, mapping={}, config={}):
    """
    Args
        d
        mapping
        config
    Returns

    """

    tree_list = dict_to_tree(d)
    flat_list = flatten_list(list(tree_list))

    sep, indent, trim_key, trim_val = parse_config(config)
    output = [format_node(val, indent, depth) for val, depth in flat_list]

    return '\n'.join(output)

