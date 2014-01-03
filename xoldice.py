#!/usr/env python
'''
XolDice

Usage:
    xoldice.py <num_of_dice> <sides> <value> [(-V | -O) -R] [-c]
    xoldice.py (-h | --help)
    xoldice.py --version

Example:
    xoldice.py 2 6 all
        Lists all number of outcomes for every possible dice roll.

    xoldice.py 2 6 all -O
        Same as above, but sorts by number of outcomes.

    xoldice.py 2 6 6
        Returns the number of outcomes which yield the value six (6),
        using two (2) dice with six (6) sides.

Options:
    -V --sort-by-value      Sort by value if <value> is 'all' (default)
    -O --sort-by-outcome    Sort by outcome if <value> is 'all'
    -R --reversed
    -c                      Show calculation progress
    -h --help               Show this help
    --version               Show script version

Dependencies:
    python    >= 3.0
    clint     >= 0.3.1
    docopt    >= 0.6.1
'''

from clint.textui import progress
from docopt import docopt
from itertools import product

ERROR_VALUE_TOO_HIGH = 1
ERROR_VALUE_TOO_LOW = 2
ERROR_DICE_TOO_LOW = 3
ERROR_SIDES_TOO_LOW = 4
ERROR_DICE_NOT_INT = 5
ERROR_SIDES_NOT_INT = 6
ERROR_VALUE_NOT_VALID = 7

class XolDice:

    def __init__(self, arguments):
        self.arguments = arguments
        self.has_error = False
        try:
            self.num_of_dice = int(arguments['<num_of_dice>'])
        except:
            self.num_of_dice = 'ERROR'
            self.has_error = ERROR_DICE_NOT_INT
            self.printError(ERROR_DICE_NOT_INT)
        try:
            self.sides = int(arguments['<sides>'])
        except:
            self.sides = 'ERROR'
            self.has_error = ERROR_SIDES_NOT_INT
            self.printError(ERROR_SIDES_NOT_INT)
        self.value = self.parseValue(arguments['<value>'])
        
        self.main()

    def parseValue(self, value):
        # Generate hash of all possible outcomes
        if value.lower() == 'all':
            # Print all possible outcomes
            return value.lower()
        else:
            # Print the num of outcomes for <value>
            try:
                return int(value)
            except:
                value = 'ERROR'
                self.has_error = ERROR_VALUE_NOT_VALID
                self.printError(ERROR_VALUE_NOT_VALID)
                return value

    def createDataStructure(self):
        indices = [i for i in range(1, (self.sides * self.num_of_dice) + 1)]
        self.lookup = {i:0 for i in indices}

    def populateLookupWithAll(self):
        products = product([s for s in range(1, self.sides + 1)], repeat=self.num_of_dice)
        if self.arguments['-c']: print('\nCalculating  : ', end='')
        for p in products:
            outcome = []
            if self.arguments['-c']: print('.', end='')
            for v in p:
                outcome.append(v)
            self.lookup[sum(outcome)] += 1
        if self.arguments['-c']: print('\n')
        return self.lookup

    def populateLookup(self):
        return self.populateLookupWithAll()[self.value]

    def printResults(self, outcome):
        if type(outcome) == type({}):
            # <value> == 'all'
            results = sorted(outcome.items(), key=lambda x: x[1 if self.arguments['--sort-by-outcome'] else 0], reverse=not self.arguments['--reversed'])
            print('{0:=>18}={0:=>18}'.format('='))
            print('|{1: ^35}|'.format('', 'Results'))
            print('{0:=>18}={0:=>18}'.format('='))
            print('|{0: >16} | {1: <16}|'.format('<value>', 'outcomes'))
            print('{0:->18}-{0:->18}'.format('-'))
            for k,v in results:
                print('|{0:>16} | {1: <16}|'.format(k,v))
            print('{0:->18}-{0:->18}'.format('-'))
        elif type(outcome) == type(int()):
            # <value> == integer
            print('%s outcome(s) yields the value %s.' % (outcome, self.value))

    def main(self):
        print('<num_of_dice>: %s' % self.num_of_dice)
        print('<sides>      : %s' % self.sides)
        print('<value>      : %s\n' % self.value)

        if self.sides != 'ERROR' and self.num_of_dice != 'ERROR':
            if self.value != 'all' and self.value > (self.num_of_dice * self.sides):
                self.printError(ERROR_VALUE_TOO_HIGH)
                self.has_error = ERROR_VALUE_TOO_HIGH
            if self.value != 'all' and self.value <= 0:
                self.printError(ERROR_VALUE_TOO_LOW)
                self.has_error = ERROR_VALUE_TOO_LOW
            if self.num_of_dice <= 1:
                self.printError(ERROR_DICE_TOO_LOW)
                self.has_error = ERROR_DICE_TOO_LOW
            if self.sides < 3:
                self.printError(ERROR_SIDES_TOO_LOW)
                self.has_error = ERROR_SIDES_TOO_LOW
        if self.has_error != False:
                self.fail_with_error(self.has_error)

        self.createDataStructure()

        if self.value == 'all':
            outcomes = self.populateLookupWithAll()
        else:
            outcomes = self.populateLookup()
        
        self.printResults(outcomes)

    def printError(self, code):
        print('Error with status code %d' % code)
        if code == ERROR_VALUE_TOO_HIGH:
            print('Value out of range! It is too high.')
            print('  0 < %s <= %s' % (self.value, self.num_of_dice * self.sides))
            print('  0 < <value> <= (<num_of_dice> * <sides>)')
        if code == ERROR_VALUE_TOO_LOW:
            print('Value out of range! It is too low.')
            print('  0 < %s <= %s' % (self.value, self.num_of_dice * self.sides))
            print('  0 < <value> <= (<num_of_dice> * <sides>)')
        if code == ERROR_DICE_TOO_LOW:
            print('Not enough number of dice. A minimum of two (2) is required.')
        if code == ERROR_SIDES_TOO_LOW:
            print('Not enough number of sides. A minimum of four (4) is required.')
        if code == ERROR_DICE_NOT_INT:
            print('<num_of_dice> must be a valid number; 1 < <num_of_dice> <= n')
        if code == ERROR_SIDES_NOT_INT:
            print('<sides> must be a valid number; 3 < <sides> <= n')
        if code == ERROR_VALUE_NOT_VALID:
            print('<value> must be a valid number or "all".')
        print('')

    def fail_with_error(self, code):
        exit(code)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='xoldice v1.0.0')
    xd = XolDice(arguments)
    exit(0)
