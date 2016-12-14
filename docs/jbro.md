
### JSON Browser (jbro) ###

<hr>

#### Introduction ####

<hr>

#### Usage ####

```Shell 
usage: jbro [-h] [-q] [-d] [-s SAMPLE] [-c CHARS] [-f FIND]
            [-F FIND_RECURSIVE] [-l]
            filename

JSON browsing utility

positional arguments:
  filename              filename of JSON file

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           suppress output description
  -d, --describe        describe structure of file
  -s SAMPLE, --sample SAMPLE
                        sample n (key, value) pairs from file
  -c CHARS, --chars CHARS
                        sample n chars from file
  -f FIND, --find FIND  find given key, nesting in form key1.key2
  -F FIND_RECURSIVE, --find_recursive FIND_RECURSIVE
                        find given key recursively (i.e. all occurrences)
  -l, --less            pipe pretty print of file to less
```

<hr> 

#### Notes ####

If no inspection parameters (-d, -s, -c, -f, -F) are specified, or if the less (-l) flag is specified, the JSON file will be pretty-printed for browsing in less.

The inspection functions are not mutually exclusive. For example, to describe a file and sample the first 5 keys:

```bash
$ jbro depth.json -d -s 5

> Describe structure of file
Top-level keys: 2
Total keys: 6
Max depth: 5
Total chars: 46

> Print first 5 keys of file
1 -> {u'2': {u'3': {u'4': {u'5': 0}}}}
a -> b
```

As can be seen from the output above, sample (-s) is not recursive as it operates only on the top level of keys. Output of long values are truncated to cap total line length at under 80 chars:

```bash
$ jbro long_values.json -s 1

> Print first 1 keys of file
a relatively long ke... -> a relatively long value
```

It is not envisioned for inspection functions and the less (-l) flag to be used together, but it is possible. From the user's perspective, irst the JSON will be piped to less; upon exisitng less, any output specified will be available.


The quiet (-q) flag removes additional descriptions in the output. This makes piping the output to some other function a bit nicer.

```bash
$ jbro sample.json -s 100 | less
```

Find (-f) attempts to return a single value given either a key or a nested key in form key1.key2... Recursive find (-F) attempts to find all values associated with a given key at any level of nesting. Although JSON technically has no restriction against duplicate keys at the same level of nesting, jbro makes such a uniqueness assumption (by virtue of using Python dicts).

```python
find1 = {'a': 1,
	     'b': 2,
	     'c': {'d': 3}}
find2 = {'a': 1,
         'b': 2,
	     'c': {'a': 3}}
```

```bash
$ jbro find1.json -f a

> Find key a in data
a -> 1

$ jbro find1.json -f c.d

> Find key c.d in data
c.d -> 3

$ jbro find2.json -f a

> Find key a in data
a -> 1

$ jbro find2.json -F a

> Find key a recursively in data
Level 0 -> 1
Level 1 -> 3
```

