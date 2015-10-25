"""Test cases for json_lws module, assumes Pytest."""

from pyjson_utils import json_lws

class TestValidateValues:
    """Test functions that validate values."""

    def test_valid_text_str(self):
        """Regex matches non-empty text (string)."""
        assert json_lws.valid_text('string', r'[a-z]*') is True
        assert json_lws.valid_text('string', r'string') is True
        assert json_lws.valid_text('string', r'[0-9]*') is False
        assert json_lws.valid_text('', r'.*') is False

    def test_valid_text_unicode(self):
        """Regex matches non-empty text (unicode)."""
        assert json_lws.valid_text(u'string', r'[a-z]*') is True
        assert json_lws.valid_text(u'string', r'string') is True
        assert json_lws.valid_text(u'string', r'[0-9]*') is False
        assert json_lws.valid_text(u'', r'.*') is False

class TestTypeHelpers:
    """"""

    def test_classify(self):
        assert json_lws.classify(str) == 'text'
        assert json_lws.classify(unicode) == 'text'
        assert json_lws.classify(int) == 'num'
        assert json_lws.classify(float) == 'num'
        assert json_lws.classify('test') is False

class TestValidateKeys:
    """Test functions that validate keys."""

    def test_unpack_1(self):
        """Ordinary key."""
        key = ('item name', str, r'name', '+')
        assert json_lws.parse_key(key) == (str, 'name', '+')

    def test_unpack_2(self):
        """Key with no repetition pattern specified."""
        key = ('item name', str, r'name')
        assert json_lws.parse_key(key) == (str, 'name', '')

    def test_unpack_3(self):
        """Key with no regex or repetition pattern specified."""
        key = ('item name', str)
        assert json_lws.parse_key(key) == (str, '.*', '')

    def test_valid_key(self):
        """Valid key is a string that matches the regex."""
        assert json_lws.valid_key('string', int, r'string') is False
        assert json_lws.valid_key('string', str, r'test') is False
        assert json_lws.valid_key(123, int, '123') is False
        assert json_lws.valid_key(123.00, float, '123') is False
        assert json_lws.valid_key('123', str, r'[0-9]*') is True

    def test_valid_length(self):
        """Validate repetition pattern checking."""
        assert json_lws.valid_length('', [1]) is True
        assert json_lws.valid_length('+', [1, 1]) is True
        assert json_lws.valid_length('?', []) is True
        assert json_lws.valid_length('?', [1]) is True
        assert json_lws.valid_length('?', [1, 1, 1]) is False
        assert json_lws.valid_length('*', []) is True
        assert json_lws.valid_length('*', [1, 1, 1]) is True
