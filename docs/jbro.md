
### JSON Browser (jbro) ###

<hr>

#### Introduction ####

<hr>

#### Usage ####

```Shell 
$ jbro -h
usage: jbro [-h] [-q] [-r] [-d] [-s SAMPLE] [-c CHARS] [-f FIND] [-l] filename

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
  -f FIND, --find FIND  find given key's value(s) in file
  -F FIND_RECURSIVE, --find_recursive FIND_RECURSIVE
                        find given key recursively (i.e. all occurrences)
  -l, --less            pipe pretty print of file to less
```

<hr> 

#### Notes ####

If no inspection parameters (-d, -s, -c, -f, -F) are specified, or if the less (-l) flag is specified, the JSON file will be pretty-printed for browsing in less.

The inspection functions are not mutually exclusive. For example, to describe a file and sample the first 5 keys:

```bash
$ jbro sample.json -d -s 5
```

It is not envisioned for inspection functions and the less (-l) flag to be used together, but it is possible. First the JSON will be piped to less; upon exisitng less, any output specified will be available.


The quiet (-q) flag removes additional descriptions in the output. This makes piping the output to some other function a bit nicer.

```bash
$ jbro sample.json -s 100 | less
```

