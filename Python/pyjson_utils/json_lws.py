"""JSON Lightweight Schema.
"""

import sys
import re
import json
import pickle
from collections import defaultdict
import logger

ERR_KEY = hash('KEY ERROR')
ERR_VAL = hash('VAL ERROR')

# Type Validation Helpers

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
    if classify(schema_type) == 'text' and is_text(data_val): return True
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
    """
    dtype, rule, repeat = parse_schema_key(schema_key)
    found_keys = [data_key for data_key in data
                  if valid_data_key(data_key, dtype, rule)]

    return found_keys if valid_length(repeat, found_keys) else []

# Schema Validation

def gen_output(log):
    """Call logger.dict_to_str() to generate output."""
    mapping = {ERR_KEY: '*** Key error.', ERR_VAL: '*** Value error.'}
    config = {'sep': ': ', 'indent': '--  ', 'trim_key': 20, 'trim_val': 10}
    return logger.dict_to_tree(log, mapping, config)

def walk(d, path):
    """Walk dict d using path as sequential list of keys, return last value."""
    if not path: return d
    return walk(d[path[0]], path[1:])

def update_stack(s_path, d_path, schema, s_key, d_key):
    """Update validation stack.
    Accepts schema and data path so far and returns next possible schema keys.
    Args
        s_path: list of schema keys walked thus far
        d_path: list of data keys walked thus far
        schema: dict of schema
        s_key: string of next schema key
        d_key: string of next data key
    Returns
        List of tuples, one tuple per next schema key:
        (updated s_path, string of next schema key, updated d_path).
    """
    new_s_path = s_path + [s_key]
    new_d_path = d_path + [d_key]
    schema_keys = walk(schema, new_s_path).keys()
    return [(new_s_path, new_s_key, new_d_path) for new_s_key in schema_keys]

def validate_schema(schema, data):
    """Schema-centric validation.
    """

    log = defaultdict(list)

    stack = update_stack([], [], schema, ('root', str), 'root')
    while stack:
        s_path, s_key, d_path = stack.pop()
        prev_s, prev_d = s_path[-1][0], d_path[-1]
        schema_sub = walk(schema, s_path)
        data_sub = walk(data, d_path)

        # error case: schema key not found in data
        d_keys = find_data_keys(data_sub, s_key)
        if not d_keys:
            log[(prev_s, prev_d)].append((s_key[0], ERR_KEY))
            continue

        s_val = schema_sub[s_key]
        for d_key in d_keys:
            d_val = data_sub[d_key]
            # not end of branch, add path to stack
            if isinstance(s_val, dict):
                stack.extend(update_stack(s_path, d_path, schema, s_key, d_key))
                log[(prev_s, prev_d)].append((s_key[0], d_key))
            # end of branch, check data value against schema
            else:
                node = d_val if valid_data_val(s_val, d_val) else ERR_VAL
                log[(prev_s, prev_d)].append((s_key[0], node))

    return log, gen_output(log)

# Data Validation

def validate_data(schema, data):
    """
    """
    return ''

# Main

def join_logs(schema_log, data_log):
    """Join logs strings into single string."""
    return ('\n>>> SCHEMA VALIDATION\n' + schema_log + '\n'
            '\n>>> DATA VALIDATION\n' + data_log + '\n')

def main(schema_path, data_path):
    """Main.
    Print and return string of validation results.
    Args
        schema_path: string of path to schema file
        data_path: string of path to data file
    """

    with open(schema_path, 'r') as f:
        raw = pickle.load(f)
        schema = {('root', str): raw}

    with open(data_path, 'r') as f:
        raw = json.load(f)
        data = {'root': raw}

    _, schema_log = validate_schema(schema, data)
    data_log = validate_data(schema, data)
    log = join_logs(schema_log, data_log)

    print log
    return log

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print 'Call with two arguments, schema pickle and data filenames.\n'
        print 'e.g. python json_lws_python.py schema.pkl data.json\n'
