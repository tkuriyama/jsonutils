"""
"""

import sys
import re
import json
import pickle

def unpack(key):
    """Unpack tuple of key."""
    data_type, regex = key[1], key[2]
    repeat = '' if len(key) == 3 else key[3]
    return data_type, regex, repeat

def valid_key(key, data_type, regex):
    """Verify key is of data_type nad matches regex."""
    return isinstance(key, data_type) and re.findall(regex, key)

def valid_length(repeat, keys):
    """Check for valid combo of repeat and length of keys."""
    return (True if not repeat or repeat == '*' else
            True if repeat == '+' and len(keys) > 1 else
            True if repeat == '?' and len(keys) < 2 else
            False)

def find_valid_keys(data, schema_key):
    """
    """
    data_type, regex, repeat = unpack(schema_key)
    found_keys = [data_key for data_key in data
                  if valid_key(data_key, data_type, regex)]

    return found_keys if valid_length(repeat, found_keys) else []

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
        print 'Call with two arguments, schema and data filenames.\n'
        print 'e.g. python json_lws_python.py schema.pkl data.json\n'
