mkhosts
=========

Little `/etc/hosts` generator written in Python. Can be used to quickly
download and merge big amount of public lists.

Usage
-------

Populate `sources.list` with hosts files, domainlists URLs and run `mkhosts
sources.list`.  Generated file will be written to stdout.

Room for improvement
----------------------

mkhosts script is just 97 lines of code written in few minutes. It's possible
to improve it, but I don't have enough time.

- [ ] Allow local files in sources
- [ ] Allow to use AdBlock Plus domain-wide rules as source
