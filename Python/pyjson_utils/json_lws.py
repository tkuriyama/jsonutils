"""JSON Lightweight Schema.
"""

import sys
import re
import json
import pickle

# Validate Values

def valid_text(val, regex):
    """Return True if regex matches string of value."""
    return re.findall(regex, val)[:1] not in ([], [''])

def valid_num():
    """"""
    return

def valid_list():
    """"""
    return

def valid_bool():
    """"""
    return

def valid_null():
    """"""
    return

#

def find_valid_func(data_type):
    """"""
    text_type = (str, unicode)
    num_type = (int, float)

    return (valid_text if data_type in text_type else
            valid_num if data_type in num_type else
            valid_list if isinstance(data_type, list) else
            False)

# Validate Keys

def parse_key(key):
    """Unpack tuple of length 3 or optionally length 4, ignore first elem."""
    _, data_type = key[:2]
    regex = '.*' if len(key) <= 2 else key[2]
    repeat = '' if len(key) <= 3 else key[3]
    return data_type, regex, repeat

def valid_key(key, data_type, pattern):
    """Verify key is of data_type and matches regex."""
    return (valid_text(key, pattern) if data_type in (str, unicode) else
            False)

def valid_length(repeat, keys):
    """Check for valid combo of repeat and length of keys."""
    return (True if not repeat or repeat == '*' else
            True if repeat == '+' and len(keys) > 1 else
            True if repeat == '?' and len(keys) < 2 else
            False)

def find_valid_keys(data, schema_key):
    """
    """
    data_type, regex, repeat = parse_key(schema_key)
    found_keys = [data_key for data_key in data
                  if valid_key(data_key, data_type, regex)]

    return found_keys if valid_length(repeat, found_keys) else []

#

def validate_schema(schema, data):
    """
    """

    current = [(data, schema_key) for schema_key in schema]

    while current:
        data, schema_key = current.pop()
        print schema_key
        data_keys = find_valid_keys(data, schema_key)
        print data_keys

    return True

# Main

def main(schema_filename, data_filename):
    """
    """

    with open(schema_filename, 'r') as f:
        schema = pickle.load(f)

    with open(data_filename, 'r') as f:
        data = json.load(f)

    validate_schema(schema, data)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print 'Call with two arguments, schema pickle and data filenames.\n'
        print 'e.g. python json_lws_python.py schema.pkl data.json\n'
