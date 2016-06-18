"""Test cases for JSON lws_logger module, assumes Pytest."""

from pytextutils.json import lws_logger


class TestDictToTreeHelpers:
    """Test the helper functions for dict_to_tree."""

    def test_flatten_list(self):
        """Test flattening of nested lists."""
        f = lws_logger.flatten_list
        nested = [1, [2, 3, [[4], 5]]]
        assert list(f(nested)) == [1, 2, 3, 4, 5]
        nested = [[[1]]]
        assert list(f(nested)) == [1]
        flat = [1, 2]
        assert list(f(flat)) == [1, 2]

    def test_filter_errors(self):
        """Test error filtering (helper function to filter_keys)."""
        f = lws_logger.filter_errors
        errors = {'key': 99,
                  'key_str': 'key error',
                  'val': -99,
                  'val_str': 'val error'}
        seq = [100, 99, 99, 99]
        assert f(seq, errors) == [100]
        seq = [99]
        assert f(seq, errors) == ['key error']
        seq = [-99, -99, 100]
        assert f(seq, errors) == [100]
        seq = [-99, -99]
        assert f(seq, errors) == ['val error']

    def test_filter_errors_single(self):
        """Test list error term filtering, single error."""
        f = lws_logger.filter_keys
        errors = {'key': 99,
                  'key_str': 'key error',
                  'val': -99,
                  'val_str': 'val error'}
        pairs = [('a', 'hi'), ('a', 99), ('b', 'hi')]
        filtered = [('a', 'hi'), ('b', 'hi')]
        assert f(pairs, errors) == filtered

    def test_filter_errors_multiple(self):
        """Test list error term filtering, multiple errors."""
        f = lws_logger.filter_keys
        errors = {'key': 99,
                  'key_str': 'key error',
                  'val': -99,
                  'val_str': 'val error'}
        pairs = [('a', 'hi'), ('a', 99), ('a', 99),
                 ('b', 'hi'), ('b', -99)]
        filtered = [('a', 'hi'), ('b', 'hi')]
        assert f(pairs, errors) == filtered

    def test_filter_errors_only(self):
        """Test list error term filtering, only errors."""
        f = lws_logger.filter_keys
        errors = {'key': 99,
                  'key_str': 'key error',
                  'val': -99,
                  'val_str': 'val error'}
        pairs = [('a', 99), ('b', -99)]
        filtered = [('a', 'key error'), ('b', 'val error')]
        assert f(pairs, errors) == filtered


class TestLoggerHelpers:
    """Test the helper functions for logger."""

    def test_dict_to_tree_simple(self):
        """Test dict_to_tree simple dicts."""
        f = lws_logger.dict_to_tree
        simple_d = {'root': ['a', 'b']}
        flat_list = [('root', 0), [('a', 1)], [('b', 1)]]
        assert f(simple_d, 'root', [('root', 0)]) == flat_list
        nested_d = {'root': ['a', 'b'], 'a': ['one', 'two']}
        nested_list = [('root', 0), [('a', 1), [('one', 2)], [('two', 2)]],
                       [('b', 1)]]
        assert f(nested_d, 'root', [('root', 0)]) == nested_list

    def test_parse_errors_one(self):
        """Test scenario with one type of error."""
        f = lws_logger.parse_errors
        errors = {'key_str': 'key error',
                  'val_str': 'val error'}
        nodes = [('one', 'key error'), ('two', 3), ('three', 3)]
        output = 'Key Errors:\t1\nValue Errors:\t0'
        assert f(nodes, errors) == (1, 0, output)

    def test_parse_errors_both(self):
        """Test scenario with two types of errors."""
        f = lws_logger.parse_errors
        errors = {'key_str': 'key error',
                  'val_str': 'val error'}
        nodes = [('one', 'key error'), ('two', 3), ('three', 3),
                 ('four', 'val error')]
        output = 'Key Errors:\t1\nValue Errors:\t1'
        assert f(nodes, errors) == (1, 1, output)

    def test_format_node(self):
        """Test node to string function."""
        f = lws_logger.format_node
        assert f('a', '----', 1) == '|----a'
        assert f('a', '----', 2) == '     |----a'
