"""JSON Lightweight Schema (LWS).

Validate both schema against data and data against schema, where
schema is a pickled dictionary object and data is JSON.

Generate graph of data as adjacency list and pass to lws_logger for
generating a string of validation report.
"""

from collections import defaultdict
import sys
import re
import json
import pickle
import lws_logger


ERRORS = {'key': hash('error key'),
          'key_str': '*** Key error',
          'val': hash('error value'),
          'val_str': '*** Value error'}


# Testing Helper


def return_errors():
    """Return error dict for testing purposes."""
    return ERRORS


# Type Validation


def valid_text(val, rule):
    """Return True if regex fully matches non-empty string of value."""
    if callable(rule):
        match = rule(val)
    else:
        match = re.findall(rule, val)
    return (False if not match or not val else
            True if match is True else
            match[0] == val)


def valid_num(val, rule):
    """Default True, check against rule if provided."""
    return (rule(val) if callable(rule) else
            val == rule if rule else
            True)


def valid_list(val, rule):
    """Default True, check against rule if provided."""
    return (rule(val) if callable(rule) else
            val == rule if rule else
            True)


def valid_bool(val, rule):
    """Default True, check against rule if provided."""
    return val is rule if rule != '' else True


def valid_null(val, rule):
    """Always True."""
    return True


def is_text(val):
    """Return True if val is text, i.e. string or uniode."""
    return isinstance(val, str) or isinstance(val, unicode)


def is_num(val):
    """Return True if val is number, i.e. int of float."""
    return isinstance(val, int) or isinstance(val, float)


def classify(dtype):
    """Take data type and classify into string of JSON data type.
    Boolean check should occur before int since bool is subclass of int.
    """
    return ('text' if dtype in (str, unicode) else
            'bool' if dtype is bool else
            'num' if dtype in (int, float) else
            'dict' if dtype is dict else
            'list' if dtype is list else
            'null' if dtype is None else
            False)


def classify_val(val):
    """Take value and classify into string of JSON data type."""
    return ('text' if is_text(val) else
            'bool' if isinstance(val, bool) else
            'num' if is_num(val) else
            'dict' if isinstance(val, dict) else
            'list' if isinstance(val, list) else
            'null' if val is None else
            False)


# Validate Values


def parse_schema_val(val):
    """Unpack tuple of the schema value."""
    _, dtype = val[:2]
    if len(val) == 3:
        rule = val[2]
    else:
        rule = '.*' if classify(dtype) == 'text' else ''
    return dtype, rule


def match_types(schema_type, data_val):
    """Return True if data types match between schema and data value.
    The difference between string and unicode is ignored.
    """
    if classify(schema_type) == 'text' and is_text(data_val):
        return True
    return isinstance(data_val, schema_type)


def match_vals(schema_rule, data_val):
    """Call type-specific function to verify data value matches schema rule."""
    dtype = classify_val(data_val)
    return (valid_text(data_val, schema_rule) if dtype is 'text' else
            valid_num(data_val, schema_rule) if dtype is 'num' else
            valid_list(data_val, schema_rule) if dtype is 'list' else
            valid_bool(data_val, schema_rule) if dtype is 'bool' else
            valid_null(data_val, schema_rule) if dtype is 'null' else
            False)


def valid_data_val(schema_val, data_val):
    """Verify data value validates against schema."""
    schema_type, schema_rule = parse_schema_val(schema_val)
    type_match = match_types(schema_type, data_val)
    val_match = match_vals(schema_rule, data_val)
    return type_match and val_match


# Validate Keys


def parse_schema_key(key):
    """Unpack tuple of schema key."""
    _, dtype = key[:2]
    rule = '.*' if len(key) <= 2 else key[2]
    repeat = '' if len(key) <= 3 else key[3]
    return dtype, rule, repeat


def valid_data_key(data_key, dtype, rule):
    """Verify key is text (string or unicode) and matches regex."""
    return (valid_text(data_key, rule) if classify(dtype) == 'text' else
            False)


def valid_length(repeat, keys):
    """Check for valid combo of repeat and length of keys."""
    return (True if not repeat or repeat == '*' else
            True if repeat == '+' and len(keys) > 1 else
            True if repeat == '?' and len(keys) < 2 else
            False)


def find_data_keys(data, schema_key):
    """Return all keys in data that match the schema key definition.
    Args
        data: dict of data
        schema_key: tuple of schema key definition
    Returns
        list of found keys
    """
    dtype, rule, repeat = parse_schema_key(schema_key)
    found_keys = [data_key for data_key in data
                  if valid_data_key(data_key, dtype, rule)]

    return found_keys if valid_length(repeat, found_keys) else []


def find_schema_keys(schema, data_key):
    """Return all keys in schema that match the data key definition.
    Args
        data: dict of schema
        data_key: string of data key
    Returns
        list of found keys
    """
    found_keys = []
    for schema_key in schema:
        dtype, rule, _ = parse_schema_key(schema_key)
        if valid_data_key(data_key, dtype, rule):
            found_keys.append(schema_key)

    return found_keys


# Validation Helpers


def trim(item, max_len=75):
    """Return string representation of item, trimmed to max length."""
    string = str(item)
    string = string[:max_len] + '...' if len(string) > max_len else string
    return string


def node_to_str(node):
    """Unpack node and convert to string."""
    if len(node) == 2 and isinstance(node, tuple):
        key, val = node
    else:
        key, val = node, ''

    key, val = trim(key), trim(val)
    return ': '.join([key, val])


def walk(d, path):
    """Walk dict d using path as sequential list of keys, return last value."""
    if not path: return d
    return walk(d[path[0]], path[1:])


def update_stack(fst_path, snd_path, fst, fst_key, snd_key):
    """Update validation stack.
    Accepts path walked in fst and snd dicts so far and returns next possible
    keys in fst dict.
    Args
        fst_path: list of fst dict keys walked thus far
        snd_path: list of snd dict keys walked thus far
        fst: dict of fst dict
        fst_key: string of next fst dict key
        snd_key: string of next snd dict key
    Returns
        List of tuples, one tuple per next schema key:
        (updated s_path, string of next schema key, updated d_path).
    """
    new_fst_path = fst_path + [fst_key]
    new_snd_path = snd_path + [snd_key]
    fst_keys = walk(fst, new_fst_path).keys()

    return [(new_fst_path, new_fst_key, new_snd_path)
            for new_fst_key in fst_keys]


# Schema Validation


def gen_schema_output(log):
    """Call logger.dict_to_str() to generate output."""
    root = ('root', 'root')
    return lws_logger.gen_log(log, root, node_to_str, ERRORS)


def validate_schema(schema, data):
    """Schema-centric validation.
    Args
        schema: dict of schema
        data: dict of data
    Returns
        string of validation graph as adjacency list
    """

    log = defaultdict(list)

    stack = update_stack([], [], schema, ('root', str), 'root')
    while stack:
        s_path, s_key, d_path = stack.pop()
        prev_s, prev_d = s_path[-1][0], d_path[-1]
        schema_sub = walk(schema, s_path)
        data_sub = walk(data, d_path)

        d_keys = find_data_keys(data_sub, s_key)
        # error case: schema key not found in data
        if not d_keys:
            log[(prev_s, prev_d)].append((s_key[0], ERRORS['key']))
            continue

        s_val = schema_sub[s_key]
        for d_key in d_keys:
            d_val = data_sub[d_key]
            # not end of branch, add path to stack
            if isinstance(s_val, dict):
                stack.extend(update_stack(s_path, d_path, schema, s_key,
                                          d_key))
                log[(prev_s, prev_d)].append((s_key[0], d_key))
            # end of branch, check data value against schema
            else:
                val = d_val if valid_data_val(s_val, d_val) else ERRORS['val']
                log[(prev_s, prev_d)].append((s_key[0], val))

    return log


# Data Validation


def gen_data_output(log):
    """Call logger.dict_to_str() to generate output."""
    root = ('root', 'root')
    return lws_logger.gen_log(log, root, node_to_str, ERRORS)


def validate_data(schema, data):
    """Data-centric validation.
    Args
        schema: dict of schema
        data: dict of data
    Returns
        string of validation graph as adjacency list
    """

    log = defaultdict(list)

    stack = update_stack([], [], data, 'root', ('root', str))
    while stack:
        d_path, d_key, s_path = stack.pop()
        prev_d, prev_s = d_path[-1], s_path[-1][0]
        data_sub = walk(data, d_path)
        schema_sub = walk(schema, s_path)

        s_keys = find_schema_keys(schema_sub, d_key)
        # error case: data key not found in schema
        if not s_keys:
            log[(prev_d, prev_s)].append((d_key, ERRORS['key']))
            continue

        d_val = data_sub[d_key]
        for s_key in s_keys:
            s_val = schema_sub[s_key]
            # not end of branch, add path to stack
            if isinstance(d_val, dict):
                stack.extend(update_stack(d_path, s_path, data, d_key, s_key))
                log[(prev_d, prev_s)].append((d_key, s_key[0]))
            # end of branch, check data value against schema
            else:
                val = s_val if valid_data_val(s_val, d_val) else ERRORS['val']
                log[(prev_d, prev_s)].append((d_key, val))

    return log


# Main


def join_logs(schema_log, data_log):
    """Join logs strings into single string."""
    return ('\n> SCHEMA VALIDATION\n\n' + schema_log + '\n\n'
            '\n> DATA VALIDATION\n\n' + data_log + '\n')


def load_schema(schema_path):
    """Load schema from pickle file, adding root node."""
    with open(schema_path, 'r') as f:
        raw = pickle.load(f)
        schema = {('root', str): raw}
    return schema


def load_data(data_path):
    """Load data from JSON file, adding root node."""
    with open(data_path, 'r') as f:
        raw = json.load(f)
        data = {'root': raw}
    return data


def main(schema_path, data_path):
    """Main.
    Return string of validation results.
    Args
        schema_path: string of path to schema file
        data_path: string of path to data file
    Returns
        Tuple (int of schema key errors, int of schema val errors,
               int of data key errors, in of data val erros,
               string of log output).
    """

    schema = load_schema(schema_path)
    data = load_data(data_path)

    schema_log = validate_schema(schema, data)
    s_key_err, s_val_err, schema_out = gen_schema_output(schema_log)
    data_log = validate_data(schema, data)
    d_key_err, d_val_err, data_out = gen_data_output(data_log)

    output = join_logs(schema_out, data_out)
    return s_key_err, s_val_err, d_key_err, d_val_err, output


if __name__ == '__main__':
    if len(sys.argv) == 3:
        _, _, _, _, output = main(sys.argv[1], sys.argv[2])
        print output
    else:
        print 'Call with two arguments, schema pickle and data filenames.\n'
        print 'e.g. python json_lws_python.py schema.pkl data.json\n'
