"""Convert dict objects to pretty print strings.
"""

# Dict to Tree

def trim(n):
    """Return a function that accepts a string and trims it to n chars."""
    def inner(string):
        return string[:n]
    return inner

def parse_config(config):
    """Parse config dictionary, return default values if necessary."""
    sep = config['sep'] if 'sep' in config else ': '
    indent = config['indent'] if 'indent' in config else '----'
    trim_key = trim(config['trim_key']) if 'trim_key' in config else trim(20)
    trim_val = trim(config['trim_val']) if 'trim_val' in config else trim(20)
    return sep, indent, trim_key, trim_val

def is_iter(arg):
    """Return True if argument is iterable."""
    return isinstance(arg, list) or isinstance(arg, tuple)

def format_text(text, indent, depth):
    """"""
    return (indent + ' ') * (depth - 1) + ' ' + text

def dict_to_tree(d, mapping={}, config={}):
    """
    Args
        d
        mapping
        config
    Returns

    """

    sep, indent, trim_key, trim_val = parse_config(config)

    output = []

    print_stack = [(key, d[key], 0) for key, val in d.items()]
    while print_stack:
        key, val, depth = print_stack.pop()
        print_key = sep.join(key) if is_iter(key) else key
        output.append((format_text(print_key, indent, depth)))

        if isinstance(val, dict):
            next_keys = [(k, val[d], depth + 1) for k, v in val.items()]
            print_stack.extend(next_keys)
        else:
            print_val = sep.join(val) if is_iter(val) else key
            output.append((format_text(print_val, indent, depth + 1)))

    return '\n'.join(output)
