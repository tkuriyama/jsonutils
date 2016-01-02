"""Convert dict objects from json_lws to pretty print strings.

"""

from collections import defaultdict

def format_node(node, indent, depth, to_str=str):
    """Return string of graph node based on arguments.
    Args
        node: tuple (key, val)
        indent: string of tree indentation chars
        depth: int of tree depth, 0 = root
        to_str: function to convert node to string, by default str
    Returns
        Formatted string.
    """
    space = ' ' * ((len(indent) + 1) * (depth - 1))
    leader = '|' + indent if depth > 0 else ''
    return space + leader + to_str(node)

def flatten_list(nested):
    """Accepts arbitrarily nested lists and returns generator for flat list."""
    for outer in nested:
        if isinstance(outer, list):
            for inner in flatten_list(outer):
                yield inner
        else:
            yield outer

def filter_errors(seq, errors):
    """Helper for filter_keys.
    Return single value from list of values if a non-error term exists; else
    return the string version of the error term.
    """
    key_err, val_err = errors['key'], errors['val']
    key_err_str, val_err_str = errors['key_str'], errors['val_str']

    return ([key_err_str] if set(seq) == set([key_err]) else
            [val_err_str] if set(seq) == set([val_err]) else
            [s for s in seq if s not in (key_err, val_err)])

def filter_keys(pairs, errors):
    """Take list of (key, value) tuples and filter out redundant values.
    For every key, all error values are redundant if there is a non-error value.
    Args
        pairs: list of (key, value) tuples
        errors:
    Returns
        List of filtered (key, value) tuples; the filtered list should contain
        unique keys only.
    """
    keys = defaultdict(list)
    for pair in pairs:
        fst, snd = pair
        keys[fst].append(snd)

    ret_pairs = []
    for key in keys:
        vals = filter_errors(keys[key], errors)
        ret_pairs.extend([(key, val) for val in vals])

    return ret_pairs

def dict_to_tree(d, key, tree, errors={}, depth=0):
    """Transform dict into nested list of values representing tree form.
    Dict should be a graph in adjacency list form, i.e. mapping one node to a
    list of one or more nodes. The resulting nested list is in depth-first
form, with the level of list nesting corresponding to the depth of the
node(s).
    Args
        d: dict to transform
        key: initial key value ("root" of dict)
        tree: list, initialized as singleton [(root value, 0)]
        errors:
        depth:
    Returns
        Nested list of (value, int of depth) pairs.
    """
    if key not in d:
        return tree
    else:
        pairs = filter_keys(d[key], errors) if errors else d[key]
        return tree + [dict_to_tree(d, p, [(p, depth + 1)], errors, depth + 1)
                       for p in pairs]

def parse_errors(nodes, errors):
    """"""
    key_errors = len([1 for schema, data in nodes if data == errors['key_str']])
    val_errors = len([1 for schema, data in nodes if data == errors['val_str']])

    output = 'Key Errors:\t' + str(key_errors)
    output += '\nValue Errors:\t' + str(val_errors)
    return output

def gen_log(graph, root, base_tree, node_to_str, errors, indent=' -- '):
    """
    Args
        graph
        root
        base_tree
        node_to_str
        errors: dict of errors
        indent
    Returns

    """

    tree_list = dict_to_tree(graph, root, base_tree, errors)
    flat_list = list(flatten_list(tree_list))

    error_output = parse_errors([node for node, _ in flat_list], errors)
    output = [format_node(node, indent, depth, node_to_str)
              for node, depth in flat_list]

    return error_output + '\n\n' + '\n'.join(output)

