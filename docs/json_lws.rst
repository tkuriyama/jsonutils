

**Example: JSON Lightweight Schema (LWS)**

[JSON Schema](http://json-schema.org/) features some nice validation but it can be quite verbose and cumbersome to use.

[JSON is defined](http://www.json.org/) as a series of nested {key: value} pairs, where a key is always a string and a value belongs to a set of possible data types. JSON LWS adds some additional, context-free validation logic:

The building blocks of a schema key consists of the following items:

1. name, required
2. data validation, optional
3. repetition validation, optional

The building blocks of a schema value consists of the following item:

1. name, required
2. data type, required
3. data validation, optional

Some example schema value definitions in Python, in which the data validation may be defined in various ways including with regular expressions and functions:

```python
('magic number', int, 42)
('prime number', int, is_prime)
('large number', int, lambda x: x > 10 ** 10)
