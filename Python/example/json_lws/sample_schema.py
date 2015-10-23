"""
"""

import sys
import pickle

def ret_schema():
    """Defines dictionary of schema."""

    schema = {
        ('path to directory', str, 'path'): ('path', str, '/apps/homefs1/.*'),
        ('dict of stocks', str, 'stocks'): {
            ('tickers', str, '[A-Z].*', '+'): {
                ('stock price', str, 'price'): ('price', float),
                ('company name', str): ('name', str)
            }
        },
        ('magic number', int, 'magic_number'): ('number', int, 42)
    }

    return schema

def main(filename):
    """Pickle schema."""

    schema = ret_schema()
    with open(filename, 'wb') as f:
        pickle.dump(schema, f)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print 'Call with one argument specifying filename of pickled file.\n'
        print 'e.g. python sample_schema.py sample_schema.pkl\n'
