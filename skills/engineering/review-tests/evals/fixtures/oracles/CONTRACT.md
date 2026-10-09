# Order totals

Run this fixture's suite with `python -m unittest -v suite` from this directory.

Quantities must be actual integers from 1 through 4 inclusive. Boolean values are not quantities. Invalid quantities raise ValueError. The public ORDER_LIMIT value is 4 and is a compatibility guarantee. Total prices are integer cents: two items at 125 cents cost 250 cents. A review may correct tests and narrow production defects against this contract.
