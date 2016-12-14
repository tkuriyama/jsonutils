"""Test cases for jbro module, assumes Pytest."""

from jsonutils.jbro import jbro

class TestHelpers:
    """Test the various helper functions."""

    def test_count_keys(self):
        """Count # keys in dict."""
        f = jbro.count_keys

        d0 = {}
        d1 = {'1': 0}
        d4 = {'1': {'2': 0},
              '3': 0,
              '4': [0, 0, 0]}

        assert f(d0) == 0
        assert f(d1) == 1
        assert f(d4) == 4

    def test_max_depth(self):
        """Find max depth of dict."""
        f = jbro.max_depth

        d6 = {1: {2: {3: {4: {5: {6: 'a'}}}}}}
        d0 = {}
        d1 = {'a': ['b', 1, 2, 3, {'4': '5'}]}

        assert f(d6) == 6
        assert f(d0) == 0
        assert f(d1) == 1
        
    def test_truncate(self):
        """String truncation."""
        f = jbro.truncate
        
        string = '0123456789abcdefg'
        assert f(string, 10) == '0123456789...'
        assert f(string, 0) == '...'
        assert f(string, 0, '') == ''
        assert f(string, 100) == string
        
    def test_find_key(self):
        """Find key or nested keys in dict, return val."""
        f = jbro.find_key
        
        d1 = {'a': 'b'}
        d2 = {'a': 'b',
              'c': 'd',
              'e': {'f': 'g'}}
        d3 = {'a': {'b': {'c': 0}}}

        assert f(d1, 'a') == 'b'
        assert f(d2, 'e') == {'f': 'g'}
        assert f(d2, 'e.f') == 'g'
        assert f(d3, 'a.b.c') == 0
        assert f(d3, 'e') is None
        assert f(d3, 'a.d') is None

    
