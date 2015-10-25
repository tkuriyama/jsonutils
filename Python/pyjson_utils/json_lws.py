"""JSON Lightweight Schema.
"""

import sys
import re
import json
import pickle

TAB = ' ' * 4

# Type Validation Helpers

def valid_text(val, regex):
    """Return True if regex fully matches string of value."""
    match = re.findall(regex, val)
    return False if not match else match[0] == val

def valid_num(val, rule):
    """Default True, check against rule if provided."""
    return val == rule if rule else True

def valid_list(val, rule):
    """Default True, check against rule if provided."""
    return val == rule if rule else True

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
    """Take data type and classify into string of JSON data type."""
    return ('text' if dtype in (str, unicode) else
            'num' if dtype in (int, float) else
            'dict' if dtype is dict else
            'list' if dtype is list else
            'bool' if dtype is bool else
            'null' if dtype is None else
            False)

def classify_val(val):
    """Take value and classify into string of JSON data type."""
    return ('text' if is_text(val) else
            'num' if is_num(val) else
            'dict' if isinstance(val, dict) else
            'list' if isinstance(val, list) else
            'bool' if isinstance(val, bool) else
            'null' if val is None else
            False)

# Validate Values

def parse_schema_val(val):
    """Unpack tuple of the schema value."""
    _, dtype = val[:2]
    if len(val) == 3:
        match = val[2]
    else:
        match = '.*' if classify(dtype) == 'text' else ''
    return dtype, match

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
    regex = '.*' if len(key) <= 2 else key[2]
    repeat = '' if len(key) <= 3 else key[3]
    return dtype, regex, repeat

def valid_data_key(data_key, dtype, pattern):
    """Verify key is text (string or unicode) and matches regex."""
    return (valid_text(data_key, pattern) if classify(dtype) == 'text' else
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
    dtype, regex, repeat = parse_schema_key(schema_key)
    found_keys = [data_key for data_key in data
                  if valid_data_key(data_key, dtype, regex)]

    return found_keys if valid_length(repeat, found_keys) else []

# Main Validation

def walk(d, path):
    """Walk dict d using path as sequential list of keys, return last value."""
    if not path: return d
    return walk(d[path[0]], path[1:])

def log_path(path, schema_key, error=False):
    """Return string, logger function for paths."""
    offset = len(path) * TAB
    error_str = TAB + '*** Key not found.' if error else ''
    return offset + '|-- ' + schema_key + error_str

def log_value(path, schema_val, data_val=''):
    """Return string, logger function for values."""
    SHOW = 10
    offset = len(path) * TAB
    if data_val:
        val = str(data_val)
        error_val = val if len(val) < SHOW else val[:SHOW] + '...'
    else:
        error_val = ''
    error_str = TAB + '*** Unexpected value: ' + error_val if error_val else ''
    return offset + '|-- ' + schema_val + error_str

def gen_log(log, errors):
    """Combine log components into single string.
    Args
        title: string
        log: list of strings
        errors: dict of {string: int} pairs
    """
    ret = '\n> Errors\n\n'
    for key in sorted(errors):
        ret += TAB + key + ': ' + str(errors[key]) + '\n'
    ret += '\n> Tree\n\n'
    ret += '\n'.join(log)
    return ret

def update_stack(s_path, d_path, schema, new_s_key, new_d_key):
    """"""
    new_s_path = s_path + [new_s_key]
    new_d_path = d_path + [new_d_key]
    schema_keys = walk(schema, new_s_path).keys()
    return [(new_s_path, s_key, new_d_path) for s_key in schema_keys]

def validate_schema(schema, data):
    """Schema-centric validation.
    """

    log = ['root']
    errors = {'key': 0, 'value': 0}

    stack = update_stack([], [], schema, 'root', 'root')
    while stack:
        print '\nCURRENT STACK', stack
        print '\nCURRENT OUTPUT', '\n'.join(log)
        print '\n'
        s_path, s_key, d_path = stack.pop()
        schema_sub = walk(schema, s_path)
        data_sub = walk(data, d_path)

        # error case: schema key not found in data
        d_keys = find_data_keys(data_sub, s_key)
        if not d_keys:
            log.append(log_path(s_path, s_key[0], True))
            errors['key'] += 1
            print 'error', s_key
            continue

        print '\nEntering d_keys loop', d_keys
        s_val = schema_sub[s_key]
        for d_key in d_keys:
            d_val = data_sub[d_key]
            # not end of branch, add path to stack
            if isinstance(s_val, dict):
                stack.extend(update_stack(s_path, d_path, schema, s_key, d_key))
                log.append(log_path(s_path, s_key[0]))
                print 'dict', s_key, d_key
            # end of branch, check data value against schema
            else:
                node = '' if valid_data_val(s_val, d_val) else d_val
                log.append(log_value(s_path, s_val[0], node))
                print 'not dict', s_key, d_key

    return gen_log(log, errors)

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
        schema = {'root': raw}

    with open(data_path, 'r') as f:
        raw = json.load(f)
        data = {'root': raw}

    schema_log = validate_schema(schema, data)
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
