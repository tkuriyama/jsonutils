### JSON Utils ###

A set of experimental utilities for working with JSON.

<hr>

#### JSON Lightweight Schema ####

[JSON Schema](http://json-schema.org/) features some nice validation but it can be quite verbose and cumbersome to use. The JSON lightweight schema (LWS) provides a minimal framework that can be implemented in any language of choice.  It is appropriate for describing simple JSON files and aims to produce very succinct schemas.

[JSON is defined](http://www.json.org/) as a series of nested {key: value} pairs, where a key is always a string and a value belongs to a set of possible data types. JSON LWS adds some additional, context-free validation logic:

The building block of a schema key consists of the following items:

1. name, required
2. data validation, optional
3. repetition validation, optional

The building block of a schema value consists of the following item:

1. name, required
2. data type, required
3. data validation, optional

JSON LWS is intentionally abstract and is meant to be implemented in a  language-specific manner, in the sense that the schema can and should reflect the constructs that are paradigmatic to the development language being used.

For example, a Python implementation might permit a combination of exact matches, functions, and regular expressions for data validation:

```python
('magic number', int, 42)                       
('prime number', int, is_prime)             
('large number', int, lambda x: x > 10 ** 10)
('lower case string value', str, r'[a-z]+')
```

<hr>

#### JSON Summarizer ####

Forthcoming.
