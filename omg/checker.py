import functools
from collections import defaultdict


class Checker(object):
    def __init__(self, name=None, verbose=True):
        self.name = name
        self.verbose = verbose
        self.assertions = {}
        self.errors = []

    def register_assertion(self, assertion, name=None):
        if name is None:
            name = 'asst_{}'.format(len(self.assertions))
        if name in self.assertions:
            raise RuntimeError('Attempting to add two assertions with the same name!')
        self.assertions[name] = assertion

    def retrive_errors(self):
        return self.errors

    def clear_errors(self):
        self.errors = []

    def wrap(self, predict_fn):
        def wrapper(inps):
            outs = predict_fn(inps)
            for asst_name, asst in self.assertions.items():
                errors = asst(inps, outs)
                if self.verbose:
                    print(f'Assertion {asst_name} failed on {errors}')
                for err in errors:
                    if self.verbose:
                        print(inps.iloc[err], outs.iloc[err])
                    self.errors.append((asst_name, inps.iloc[err], outs.iloc[err]))
            return outs
        return wrapper
