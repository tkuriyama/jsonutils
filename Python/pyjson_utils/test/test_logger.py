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
        """Test parse_config with empty dict passed."""
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
