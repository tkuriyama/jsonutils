"""Pytest test cases for json_lws module."""

from json_tools import json_lws

class TestValidateSchemaHelpers:

    def test_unpack_one(self):
        key = ('item name', str, r'name')
        assert json_lws.unpack(key) == (str, 'name', '')

    def test_unpack_two(self):
        key = ('item name', str, r'name', '+')
        assert json_lws.unpack(key) == (str, 'name', '+')

    def test_valid_key(self):
        assert json_lws.valid_key('string', str, r'[a-z]*') is True
        assert json_lws.valid_key('string', str, r'[0-9]*') is False
        assert json_lws.valid_key('string', int, r'string') is False




