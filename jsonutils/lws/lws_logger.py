"""Convert validation graphs from JSON lws to pretty print strings."""

from collections import defaultdict

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
    Return singleton list of error term if only errors are in sequence; else
    return all non-error items in sequence.
    Args
        seq: list of strings
        errors: dict representing error values
    Returns
        List of filtered items.
    """
    key_err, val_err = errors['key'], errors['val']
    key_err_str, val_err_str = errors['key_str'], errors['val_str']

    return ([key_err_str] if set(seq) == set([key_err]) else
            [val_err_str] if set(seq) == set([val_err]) else
            [s for s in seq if s not in (key_err, val_err)])

def filter_keys(pairs, errors):
    """Take list of (key, value) tuples and filter out redundant values.
    For every key, error values are redundant if there is a non-error value.
    Args
        pairs: list of (key, value) tuples
        errors: dict representing error values
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
        errors: dict representing error values
        depth: current depth of tree / recursive call; root is 0
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
    """Count errors in nodes.
    Args
        nodes: list of tuples of two items
        errors: dict representing error values
    Returns
        Tuple (int of key erros, int of val errors, string of error output).
    """
    key_errors = len([1 for fst, snd in nodes if snd == errors['key_str']])
    val_errors = len([1 for fst, snd in nodes if snd == errors['val_str']])

    output = 'Key Errors:\t' + str(key_errors)
    output += '\nValue Errors:\t' + str(val_errors)
    return key_errors, val_errors, output

def format_node(node, indent, depth, to_str=str):
    """Return string of graph node based on arguments.
    Args
        node: tuple of two items
        indent: string of tree indentation chars
        depth: int of tree depth, 0 = root
        to_str: function to convert node to string, by default str
    Returns
        String representaiton of node.
    """
    space = ' ' * ((len(indent) + 1) * (depth - 1))
    leader = '|' + indent if depth > 0 else ''
    return space + leader + to_str(node)

def gen_log(graph, root, node_to_str, errors, indent=' -- '):
    """Generate string of log and capture errors from lws graph.
    Args
        graph: dict of graph generated by lws
        root: root node of the graph
        node_to_str: function to represent node as string
        errors: dict representing error values
        indent: string of indent to use when printing tree depths
    Returns
        Tuple (int of key erros, int of val errors, string of log output).
    """

    base_tree = [(root, 0)]
    tree_list = dict_to_tree(graph, root, base_tree, errors)
    flat_list = list(flatten_list(tree_list))

    output = [format_node(node, indent, depth, node_to_str)
              for node, depth in flat_list]
    k_err, v_err, err = parse_errors([node for node, _ in flat_list], errors)
    log = err + '\n\n' + '\n'.join(output)

    return k_err, v_err, log
