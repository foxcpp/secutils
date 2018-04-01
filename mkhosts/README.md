mkhosts
=========

Little `/etc/hosts` generator written in Python. Can be used to quickly
download and merge big amount of public lists.

Usage
-------

Populate `sources.list` with hosts files, domain lists URLs and run 
`mkhosts sources.list`.  Generated file will be written to stdout.

- You can reference local files using `file://` scheme.

- In addition to parsing hosts and domain lists mkhosts can extract domain-wide
  ABP rules like these: `||ad.reople.co.kr^` if it detects that input is in ABP
  format.

- You can specify file with whitelists URLs using `-w` argument. If you have 
  only one local whitelist file - use `<(echo file://whitelist)`.

