"""Test cases for JSON lws module, assumes Pytest."""

from pytextutils.json import lws

class TestTypeValidation:
    """Test the various type validation helper functions."""

    def test_valid_text_str(self):
        """Regex/function matches non-empty text (string)."""
        f = lws.valid_text
        assert f('string', r'[a-z]*') is True
        assert f('string', r'string') is True
        assert f('string', r'[0-9]*') is False
        assert f('', r'.*') is False
        assert f('abcde', lambda x: 'e' in x) is True
        assert f('abcde', lambda x: 'f' in x) is False

    def test_valid_text_unicode(self):
        """Regex/function matches non-empty text (unicode)."""
        f = lws.valid_text
        assert f(u'string', r'[a-z]*') is True
        assert f(u'string', r'string') is True
        assert f(u'string', r'[0-9]*') is False
        assert f(u'', r'.*') is False
        assert f(u'abcde', lambda x: 'e' in x) is True
        assert f(u'abcde', lambda x: 'f' in x) is False

    def test_valid_list(self):
        """Basic test cases."""
        f = lws.valid_list
        assert f([1, 2, 3], lambda x: 2 in x) is True
        assert f([1, 2, 3], [1, 2, 3]) is True
        assert f([1, 2, 3], [1, 2]) is False
        assert f([1, 2, 3], lambda x: sum(x) < 2) is False

    def test_valid_bool(self):
        """Basic test cases."""
        f = lws.valid_bool
        assert f(True, True) is True
        assert f(True, False) is False
        assert f(False, True) is False
        assert f(False, False) is True

    def test_valid_null(self):
        """Always return True, as NoneType is assumed to be a given."""
        f = lws.valid_null
        assert f(None, '') is True
        assert f('asdasdasd', '') is True

    def test_is_text(self):
        """Basic test cases."""
        f = lws.is_text
        assert f('test') is True
        assert f(u'test') is True
        assert f(True) is False

    def test_is_num(self):
        """Basic test cases."""
        f = lws.is_num
        assert f(2) is True
        assert f(2.0) is True
        assert f('tests') is False

    def test_classify(self):
        """Basic tests cases."""
        f = lws.classify
        assert f(str) == 'text'
        assert f(unicode) == 'text'
        assert f(int) == 'num'
        assert f(float) == 'num'
        assert f('test') is False

    def test_classify_val(self):
        """Basic test cases."""
        f = lws.classify_val
        assert f('test') == 'text'
        assert f(u'test') == 'text'
        assert f(123) == 'num'
        assert f(456.001) == 'num'
        assert f(True) == 'bool'
        assert f(None) == 'null'
        assert f(lambda x: x + 1) is False

class TestValidateValues:
    """Test functions that validate values."""

    def test_unpack_1(self):
        """Ordinary value."""
        val = ('item name', str, r'name')
        assert lws.parse_schema_val(val) == (str, 'name')

    def test_unpack_2(self):
        """String value with no matching provided."""
        val = ('item name', str)
        assert lws.parse_schema_val(val) == (str, '.*')

    def test_unpack_3(self):
        """Non-string value with no matching provided."""
        val = ('item number', int)
        assert lws.parse_schema_val(val) == (int, '')

    def test_match_types(self):
        """Test cases for type matching."""
        f = lws.match_types
        assert f(str, u'test') is True
        assert f(str, 'test') is True
        assert f(int, 123) is True
        assert f(int, 123.00) is False
        assert f(bool, [1, 2, 3]) is False

    def test_match_vals(self):
        """Test basic cases for match_vals."""
        f = lws.match_vals
        schema_rule = r'[a-z]*'
        assert f(schema_rule, 'abc') is True
        assert f(schema_rule, 'ABC') is False
        schema_rule = 7
        assert f(schema_rule, 7) is True
        assert f(schema_rule, 7.00) is True
        assert f(r'abc', None) is True
        assert f(lambda x: x < 10, 5) is True
        assert f(lambda x: x > 10, 9) is False

    def test_match_valid_data_val(self):
        """Test basic cases for schema validation against data values."""
        f = lws.valid_data_val
        schema_val = ('some text', unicode, u'text')
        assert f(schema_val, 'text') is True
        assert f(schema_val, u'text') is True
        schema_val = ('some number', float, 7.00)
        assert f(schema_val, 7) is False
        assert f(schema_val, 7.00) is True
        schema_val = ('True', bool, True)
        assert f(schema_val, True) is True
        assert f(schema_val, False) is False
        schema_val = ('even', int, lambda x: x % 2 == 0)
        assert f(schema_val, 2) is True
        assert f(schema_val, 257) is False

class TestValidateKeys:
    """Test functions that validate keys."""

    def test_unpack_1(self):
        """Ordinary key."""
        key = ('item name', str, r'name', '+')
        assert lws.parse_schema_key(key) == (str, 'name', '+')

    def test_unpack_2(self):
        """Key with no repetition pattern specified."""
        key = ('item name', str, r'name')
        assert lws.parse_schema_key(key) == (str, 'name', '')

    def test_unpack_3(self):
        """Key with no regex or repetition pattern specified."""
        key = ('item name', str)
        assert lws.parse_schema_key(key) == (str, '.*', '')

    def test_valid_key(self):
        """Valid key is a string that matches the regex."""
        f = lws.valid_data_key
        assert f('string', int, r'string') is False
        assert f('string', str, r'test') is False
        assert f(123, int, '123') is False
        assert f(123.00, float, '123') is False
        assert f('123', str, r'[0-9]*') is True

    def test_valid_length(self):
        """Validate repetition pattern checking."""
        f = lws.valid_length
        assert f('', [1]) is True
        assert f('+', [1, 1]) is True
        assert f('?', []) is True
        assert f('?', [1]) is True
        assert f('?', [1, 1, 1]) is False
        assert f('*', []) is True
        assert f('*', [1, 1, 1]) is True

    def test_find_data_keys(self):
        """Test basic scenario."""
        data = {'C': 'Citigroup',
                'BAC': 'Bank of America',
                'random': 'random company'}
        schema_key = ('ticker', str, r'[A-Z]+', '+')
        assert lws.find_data_keys(data, schema_key) == ['C', 'BAC']

    def test_find_schema_keys(self):
        """Test basic scenario."""
        schema = {('ticker', str, r'[A-Z]+', '+'),
                  ('name', str, 'name'),
                  ('alphabet', str, r'[A-Z][a-z]+')}
        data_key = 'C'
        expected = [('ticker', str, r'[A-Z]+', '+'),
                    ('alphabet', str, r'[A-Z][a-z]+')]
        lws.find_schema_keys(schema, data_key) == expected

class TestValidationHelpers:
    """Test the schema and data validation helpers."""

    def test_trim(self):
        """Test basic string trimming."""
        s1 = 'esrdctfvubfiqisqwduonq'
        assert lws.trim(s1, 5) == 'esrdc...'
        assert lws.trim(s1) == 'esrdctfvubfiqisqwduo...'
        s2 = 'asdasdasd'
        assert lws.trim(s2) == 'asdasdasd'

    def test_node_to_str(self):
        """Test node unpacking for printing schema validation log."""
        f = lws.node_to_str
        # normal
        assert f(('a', 'b')) == 'a: b'
        # exception
        assert f(('a',),) == "('a',): "
        assert f('a') == 'a: '

    def test_walk(self):
        """Test dictionary walking."""
        f = lws.walk
        d = {'a': {'b': 'c'}}
        assert f(d, []) == d
        assert f(d, ['a']) == {'b': 'c'}
        assert f(d, ['a', 'b']) == 'c'

    def test_update_stack(self):
        """Test stack updating."""
        f = lws.update_stack
        s_path = [('a', str), ('b', str)]
        d_path = ['a', 'b']
        schema = {('a', str): {('b', str): {('c', str): {('d', str): 'e'}}}}
        s_key = ('c', str)
        d_key = 'c'
        expected = [([('a', str), ('b', str), ('c', str)],
                     ('d', str),
                     ['a', 'b', 'c'])]
        assert f(s_path, d_path, schema, s_key, d_key) == expected

