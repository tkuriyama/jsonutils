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
        """"""

    def test_truncate(self):
        """"""

    
