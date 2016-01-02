"""Test cases for logger module, assumes Pytest."""

from pytextutils import logger

class TestDictToTreeHelpers:
    """Test the helper functions for dict_to_tree."""

    def test_format_node(self):
        """Test node to string function."""
        f = logger.format_node
        assert f('a', '----', 1) == '|----a'
        assert f('a', '----', 2) == '     |----a'

    def test_flatten_list(self):
        """Test flattening of nested lists."""
        f = logger.flatten_list
        nested = [1, [2, 3, [[4], 5]]]
        assert list(f(nested)) == [1, 2, 3, 4, 5]
        nested = [[[1]]]
        assert list(f(nested)) == [1]
        flat = [1, 2]
        assert list(f(flat)) == [1, 2]

    def test_filter_errors(self):
        """Test error filtering (helper function to filter_keys)."""
        f = logger.filter_errors
        vals = [1, 0, 0, 0, 0, 0]
        assert f(vals, 0) == 1
        vals = [0, 0, 0, 0]
        assert f(vals, 0) == 0

    def test_filter_errors_single(self):
        """Test list error term filtering, single error."""
        f = logger.filter_keys
        pairs = [('a', 'hi'), ('a', 'error'), ('b', 'hi')]
        filtered = [('a', 'hi'), ('b', 'hi')]
        assert f(pairs, 'error') == filtered

    def test_filter_errors_multiple(self):
        """Test list error term filtering, multiple errors."""
        f = logger.filter_keys
        pairs = [('a', 'hi'), ('a', 'error'), ('a', 'error'),
                 ('b', 'hi'), ('b', 'error')]
        filtered = [('a', 'hi'), ('b', 'hi')]
        assert f(pairs, 'error') == filtered

    def test_filter_errors_only(self):
        """Test list error term filtering, only errors."""
        f = logger.filter_keys
        pairs = [('a', 'error'), ('b', 'error')]
        filtered = [('a', 'error'), ('b', 'error')]
        assert f(pairs, 'error') == filtered

    def test_dict_to_tree_simple(self):
        """Test dict_to_tree simple dicts."""
        f = logger.dict_to_tree
        simple_d = {'root': ['a', 'b']}
        flat_list = [('root', 0), [('a', 1)], [('b', 1)]]
        assert f(simple_d, 'root', [('root', 0)]) == flat_list
        nested_d = {'root': ['a', 'b'], 'a': ['one', 'two']}
        nested_list = [('root', 0), [('a', 1), [('one', 2)], [('two', 2)]],
                       [('b', 1)]]
        assert f(nested_d, 'root', [('root', 0)]) == nested_list

    def test_dict_to_tree_error(self):
        """"""
        f = logger.dict_to_tree
