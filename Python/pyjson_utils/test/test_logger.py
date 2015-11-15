"""Test cases for logger module, assumes Pytest."""

from pyjson_utils import logger

class TestDictToTreeHelpers:
    """Test the helper functions for dict_to_tree."""

    def test_trim(self):
        """Test trimming function with different parameters."""
        f = logger.trim(10)
        assert f('0123456789abcdefg') == '0123456789'
        f = logger.trim(5)
        assert f('abcdefghijk') == 'abcde'
        f = logger.trim(0)
        assert f('qweouhqno') == ''

    def test_parse_config_default(self):
        """Test hard-coded defaults in parse_config with empty dict passed."""
        f = logger.parse_config
        sep, indent, trim_key, trim_val = f({})
        test = 'oahdubowbfocbqeocq18boqbsf8g19oubwdoqbs9c91brqsdc'
        test_trim = logger.trim(20)
        assert sep == ': '
        assert indent == ' -- '
        assert trim_key(test) == test_trim(test)
        assert trim_val(test) == test_trim(test)

    def test_is_iter(self):
        """Test iterable type tester."""
        f = logger.is_iter
        assert f([1, 2, 3]) is True
        assert f((1, 2, 3)) is True
        assert f({'a': 1}) is False

    def test_format_node(self):
        """Test node to string function."""
        f = logger.format_node
        assert f('a', '----', 1) == 'a'
        assert f('a', '----', 2) == '|----a'

    def test_filter_values(self):
        """Test value filtering (helper function to filter_errors)."""
        f = logger.filter_values
        vals = [1, 0, 0, 0, 0, 0]
        assert f(vals, 0) == 1
        vals = [0, 0, 0, 0]
        assert f(vals, 0) == 0

    def test_filter_errors_single(self):
        """Test list error term filtering, single error."""
        f = logger.filter_errors
        pairs = [('a', 'hi'), ('a', 'error'), ('b', 'hi')]
        filtered = [('a', 'hi'), ('b', 'hi')]
        assert f(pairs, 'error') == filtered

    def test_filter_errors_multiple(self):
        """Test list error term filtering, multiple errors."""
        f = logger.filter_errors
        pairs = [('a', 'hi'), ('a', 'error'), ('a', 'error'),
                 ('b', 'hi'), ('b', 'error')]
        filtered = [('a', 'hi'), ('b', 'hi')]
        assert f(pairs, 'error') == filtered

    def test_filter_errors_only(self):
        """Test list error term filtering, only errors."""
        f = logger.filter_errors
        pairs = [('a', 'error'), ('b', 'error')]
        filtered = [('a', 'error'), ('b', 'error')]
        assert f(pairs, 'error') == filtered

    def test_dict_to_list_basic(self):
        """Test dict_to_list using normal dicts."""
        f = logger.dict_to_list
        simple_d = {'root': ['a', 'b']}
        flat_list = ['root', ['a'], ['b']]
        assert f(simple_d, 'root', ['root']) == flat_list
        nested_d = {'root': ['a', 'b'],
                    'a': ['one', 'two']}
        nested_list = ['root', ['a', ['one'], ['two']], ['b']]
        assert f(nested_d, 'root', ['root']) == nested_list

    def test_dict_to_list_error(self):
        """"""
