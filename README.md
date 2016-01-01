## Text Utils ##

A set of experimental utilities for working with conventionally structured text files (e.g. JSON, CSV).

<hr>

### Philosophy ###

It is often useful to examine and validate structured text data. This library intends to provide a simple, customizable framework for running quick (but hopefully not so dirty) analysis.

It should be possible to answer questions like:
* Do all JSON files in this subdirectory conform to a simple schema?
* Do all the fields in this CSV column match expectations?
* What is the range of numerical values in this set of TSV files?

The implementations and interfaces are deliberately idiomatic to the programming language being used (e.g. a JSON schema is defined in Python when using the Python implementation). This follows from an emphasis on simplicity over a more abstract, generalizable framework.

The repo is organized by language; each language-specific repo has its own documentation for the utilities that it implements.

<hr>

### Example ###

**JSON Lightweight Schema (LWS)**

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
('lower case string value', str, r'[a-z]+')
```
