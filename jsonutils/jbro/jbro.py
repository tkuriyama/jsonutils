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
            len(d) + sum(count_keys(v) for v in d.itervalues()))

def max_depth(d):
    """Return maximum depth of given dict."""
    return (0 if not isinstance(d, dict) else
            1 + max(max_depth(v) for v in d.itervalues()))

# Functions

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

def sample(data):
    """"""
    
    return

def chars(data, n, quiet):
    """Print first n chars of file."""
    data_str = json.dumps(data, indent=2, sort_keys=True)
    if not quiet:
        print '\n> Show first {:,d} chars of file'.format(n)
    print data_str[:n]
    return True

def keys(data):
    """"""
    return

def find(data, key):
    """"""
    return

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
        sample(data)
    if args.chars:
        chars(data, args.chars, args.quiet)
    if args.keys:
        keys(data)
    if args.find:
        find(data)

    print '\n'

    other_args = [args.describe, args.sample, args.chars, args.keys, args.find]
    if args.less or not any(other_args):
        data_str = json.dumps(data, indent=2, sort_keys=True)
        less(data_str)

    return True
