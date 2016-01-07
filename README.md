## Text Utils ##

A set of experimental utilities for working with conventionally structured text files.

<hr>

It is often useful to examine and validate structured text data like CSV and JSON. This library intends to provide a simple, customizable framework for running quick (but hopefully not so dirty) analysis.

It should be possible to answer questions like:
* Do all JSON files in this subdirectory conform to a simple schema?
* Do all the values in this CSV column match expectations?
* What is the range of numerical values in this set of TSV file columns?

The implementations and interfaces are deliberately specific to the programming language being used (e.g. a JSON schema is defined in Python when using the Python implementation). This favors simplicity over generalization.

The repo is organized by language; each language-specific repo has its own documentation for the utilities that it implements.
