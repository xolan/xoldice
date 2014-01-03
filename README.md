XolDice v1.0.0
--------------

Script for calculating the number of occurrences of a, or all, values given n dice with m sides.

Usage
=====
```
xoldice.py <num_of_dice> <sides> <value> [(-V | -O) -R] [-c]
xoldice.py (-h | --help)
xoldice.py --version
```

Example
=======
`xoldice.py 2 6 all`
Lists all number of outcomes for every possible dice roll.

`xoldice.py 2 6 all -O`
Same as above, but sorts by number of outcomes.

`xoldice.py 2 6 6`
Returns the number of outcomes which yield the value six (6), using two (2) dice
with six (6) sides.

Options
=======
 * `-V --sort-by-value`      Sort by value if `<value>` is 'all' (default)
 * `-O --sort-by-outcome`    Sort by outcome if `<value>` is 'all'
 * `-R --reversed`
 * `-c`                      Show calculation progress
 * `-h --help`               Show this help
 * `--version`               Show script version

Dependencies
============
 * `python`    >= 3.0
 * `clint`     >= 0.3.1
 * `docopt`    >= 0.6.1
