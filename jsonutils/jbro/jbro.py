# JSON Browser
# Simple command-line utility for inspecting contents of JSON files

from subprocess import Popen, PIPE
import json

# Helpers

def test_json(filename):
    """Verify that given filename is valid JSON; if not, return None."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except Exception, e:
        print e
        data = None
    return data

def count_keys(d):
    """Count number of keys in given dict."""
    return (0 if not isinstance(d, dict) else
            len(d) + sum(count_keys(v) for v in d.values()))

def max_depth(d):
    """Return maximum depth of given dict."""
    return (0 if not isinstance(d, dict) or len(d) == 0 else
            1 + max(max_depth(v) for v in d.values()))

def truncate(val, n, ellipsis='...'):
    """Truncate value at n chars."""
    val_str = str(val)
    return (val_str[:n] + ellipsis if len(val_str) > n else
            val_str)
    
def make_pair(key, val):
    """Return key, val pair as single string appropriate for printing."""
    return ' -> '.join([truncate(key, 20), truncate(val, 50)])

def find_key(d, nested_key):
    """Attempt to find key in dict, where key may be nested key1.key2..."""
    keys = nested_key.split('.')
    key = keys[0]
    
    return (d[key] if len(keys) == 1 and key in d else
            None if len(keys) == 1 and key not in d else
            None if not isinstance(d[key], dict) else
            find_key(d[key], '.'.join(keys[1:])) if key in d else
            None)

def find_key_rec(search_d, search_key):
    """Find search_key recursively (DFS) in dict, return value and level."""
    hits = []
    dicts = [(0, search_d)]
    
    while dicts:
        level, d = dicts.pop()
        for key in d:
            if key == search_key:
                hits.append((level, d[key]))
            else:
                if isinstance(d[key], dict):
                    dicts.append((level + 1, d[key]))
    
    return hits

# Inspection Functions

def describe(data, quiet):
    """Describe structure of data."""
    if not quiet:
        print '\n> Describe structure of file'
    else:
        print ''
        
    print 'Top-level keys: {:,d}'.format(len(data))
    print 'Total keys: {:,d}'.format(count_keys(data))
    print 'Max depth: {:,d}'.format(max_depth(data))
    print 'Total chars: {:,d}'.format(len(json.dumps(data)))
    
    return True

def sample(data, n, quiet):
    """Sample first n (key, value) pairs of file."""
    if not quiet:
        print '\n> Print first {:,d} keys of file'.format(n)
    else:
        print ''
        
    keys = sorted(data.keys())[:n]
    pairs = [make_pair(key, data[key]) for key in keys]
    print '\n'.join(pairs)
    return True

def chars(data, n, quiet):
    """Print first n chars of file."""
    if not quiet:
        print '\n> Show first {:,d} chars of file'.format(n)
    else:
        print ''
        
    data_str = json.dumps(data, indent=2, sort_keys=True)
    print data_str[:n]
    return True

def find(data, key, quiet):
    """Attempt to find key in dict, where key nesting in form key1.key2..."""
    if not quiet:
        print '\n> Find key {} in data'.format(key)
    else:
        print ''
        
    val = find_key(data, key)
    if val is not None:
        print ' -> '.join([truncate(key, 20), truncate(val, 50)])
    else:
        print 'Key not found.'
    return True

def find_rec(data, key, quiet):
    """Find key recursively in data, return all occurences."""
    if not quiet:
        print '\n> Find key {} recursively in data'.format(key)
    else:
        print ''

    vals = find_key_rec(data, key)
    if vals is not []:
        found = ['Level {:,d} -> {}'.format(level, val) for level, val in vals]
        print '\n'.join(found)
    else:
        print 'Key not found.'
    return True

def less(data_str):
    """Pretty print JSON and pipe to less."""
    p = Popen('less', stdin=PIPE)
    p.stdin.write(data_str)
    p.stdin.close()
    p.wait()
    return True

# Main 

def main(args):
    """Process args from argparse."""
    data = test_json(args.filename)
    if not data: return False

    if args.describe:
        describe(data, args.quiet)
    if args.sample:
        sample(data, args.sample, args.quiet)
    if args.chars:
        chars(data, args.chars, args.quiet)
    if args.find:
        find(data, args.find, args.quiet)
    if args.find_recursive:
        find_rec(data, args.find_recursive, args.quiet)

    print '\n'

    other_args = [args.describe, args.sample, args.chars, args.find,
                  args.find_recursive]
    if args.less or not any(other_args):
        data_str = json.dumps(data, indent=2, sort_keys=True)
        less(data_str)

    return True
