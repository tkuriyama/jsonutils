"""Test cases for json_lws module, assumes Pytest."""

from pyjson_utils import json_lws

class TestTypeValidationHelpers:
    """Test the various type validation helper functions."""

    def test_classify(self):
        f =  json_lws.classify
        assert f(str) == 'text'
        assert f(unicode) == 'text'
        assert f(int) == 'num'
        assert f(float) == 'num'
        assert f('test') is False

class TestValidateValues:
    """Test functions that validate values."""

    def test_valid_text_str(self):
        """Regex matches non-empty text (string)."""
        f = json_lws.valid_text
        assert f('string', r'[a-z]*') is True
        assert f('string', r'string') is True
        assert f('string', r'[0-9]*') is False
        assert f('', r'.*') is False

    def test_valid_text_unicode(self):
        """Regex matches non-empty text (unicode)."""
        f = json_lws.valid_text
        assert f(u'string', r'[a-z]*') is True
        assert f(u'string', r'string') is True
        assert f(u'string', r'[0-9]*') is False
        assert f(u'', r'.*') is False

class TestValidateKeys:
    """Test functions that validate keys."""

    def test_unpack_1(self):
        """Ordinary key."""
        key = ('item name', str, r'name', '+')
        assert json_lws.parse_schema_key(key) == (str, 'name', '+')

    def test_unpack_2(self):
        """Key with no repetition pattern specified."""
        key = ('item name', str, r'name')
        assert json_lws.parse_schema_key(key) == (str, 'name', '')

    def test_unpack_3(self):
        """Key with no regex or repetition pattern specified."""
        key = ('item name', str)
        assert json_lws.parse_schema_key(key) == (str, '.*', '')

    def test_valid_key(self):
        """Valid key is a string that matches the regex."""
        f = json_lws.valid_data_key
        assert f('string', int, r'string') is False
        assert f('string', str, r'test') is False
        assert f(123, int, '123') is False
        assert f(123.00, float, '123') is False
        assert f('123', str, r'[0-9]*') is True

    def test_valid_length(self):
        """Validate repetition pattern checking."""
        f = json_lws.valid_length
        assert f('', [1]) is True
        assert f('+', [1, 1]) is True
        assert f('?', []) is True
        assert f('?', [1]) is True
        assert f('?', [1, 1, 1]) is False
        assert f('*', []) is True
        assert f('*', [1, 1, 1]) is True
