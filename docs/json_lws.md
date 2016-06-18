

### JSON Lightweight Schema (LWS) ###

<hr>

#### Introduction ####

[JSON is defined](http://www.json.org/) as a series of nested {key: value} pairs, where a key is always a string and a value belongs to a set of possible data types. lws follows the same key-value structure, where a schema is defined by a dictionary in Python and serialized to file using [`pickle`](https://docs.python.org/2/library/pickle.html).

A schema key consists of the following items:

1. name, required
2. data type, required
3. data validation, optional
4. repetition validation, optional

A schema value consists of the following item:

1. name, required
2. data type, required
3. data validation, optional

Some example schema value definitions, in which the data validation may be defined in various ways -- in this case, as a fixed integer, as a predicate function `is_prime` that must be satisfied, and as an anonymous function.

```python
('magic number', int, 42)
('prime number', int, is_prime)
('large number', int, lambda x: x > 10 ** 10)
```

#### Validation Logic ####

lws performs two types of validations by default (so "reconciliation" is maybe a better description): schema-centric, and data-centric.

If a data element is specified in the schema and is present in the data, both schema-centric and data-centric validations will return the same results. However, schema-centric validation captures schema keys that are not present in the data (insufficient data), and data-centric validation captures data keys that are not present in the schema (superfluous data).


#### Schema Definition ####

A schema key is defined as a tuple containing between two and four elements.

| Index | Element | Required | Description |  
| ---   | ---     | ---      | ---         |
| 0 | Name                  | Y | name of schema key        |
| 1 | Data Type             | Y | Python data type          |
| 2 | Data Validation       | N | specifies validation for the key |
| 3 | Repetition Validation | N | specifies if the key is repeated |

A schema value is defined as a tuple containing between two and three elements.

| Index | Element | Required | Description |  
| ---   | ---     | ---      | ---         |
| 0 | Name                  | Y | name of schema key        |
| 1 | Data Type             | Y | Python data type          |
| 2 | Data Validation       | N | specifies validation for the key |

Permissible schema data types and mapping to JSON data types:

| Python DType | JSON Dtype |
| ---          | ---        |
| str, unicode | string     |
| int, float   | number     |
| list         | array      |
| dict         | object     |
| bool         | true, false|
| None         | null       |

For data validation, lws will perform an equality check (== operator) if a value is supplied. Alternatively, the following data validation objects may be supplied:

| JSON Dtype | Permissible Validation Object |
| ---        | --- |
| text       | function, regex |
| number     | function |
| array      | function |

A single character is expected for the repetition validation option. The definition follows that of regular expressions:

| Char  | Meaning |
| ---   | --- |
| * | zero or more repetitions |
| + | one or more repetitions |
| ? | zero or one repetitions |


#### Usage and Example ####

See the [lws sample files in the repo](https://github.com/tkuriyama/jsonutils/tree/master/jsonutils/sample/lws)
 for how to generate a schema pickle and examples of normal and error data files.

 ```python
In [1]: from jsonutils.lws import lws

In [2]: ret = lws.main('sample_schema.pkl', 'sample_data_normal.json')

In [3]: ret[:4]
Out[3]: (0, 0, 0, 0)

In [4]: ret = lws.main('sample_schema.pkl', 'sample_data_error.json')

In [5]: ret[:4]
Out[5]: (1, 1, 1, 1)

In [6]: print ret[4]

> SCHEMA VALIDATION

Key Errors:	1
Value Errors:	1

root: root
| -- magic number: *** Key error
| -- dict of stocks: stocks
     | -- ticker: C
          | -- stock price: *** Value error
          | -- company name: Citigroup
     | -- ticker: BAC
          | -- stock price: 25.0
          | -- company name: Bank of America
| -- path to directory: /apps/homefs1/tarokuriyama/stocks


> DATA VALIDATION

Key Errors:	1
Value Errors:	1

root: root
| -- path: ('path', <type 'str'>, '/apps/homefs1/.*')
| -- stocks: dict of stocks
     | -- C: ticker
          | -- price: *** Value error
          | -- name: ('name', <type 'str'>)
     | -- BAC: ticker
          | -- price: ('price', <type 'float'>)
          | -- name: ('name', <type 'str'>)
| -- not in schema: *** Key error
```
