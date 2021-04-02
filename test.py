import sys

def _test(name, condition, expected, actual):
    try:
        assert condition
    except AssertionError:
        sys.exit('!!TEST FAILURE!! - {0}\n\tExpected: {1}\n\tActual: {2}'.format(name, expected, actual))
    return

def is_true(name, value):
    _test(name, value, True, value)

def is_false(name, value):
    _test(name, not value, False, value)

def equal(name, expected, actual):
    _test(name, actual == expected, expected, actual)
    return

def greater_than_equal(name, expected, actual):
    _test(name, actual >= expected, expected, actual)
    return

