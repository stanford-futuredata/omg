import pandas as pd
from collections import defaultdict


class PerRowAssertion(object):
    def __init__(self, callback, name=None):
        self.callback = callback
        self.name = f'Per-row {name}'

    def get_name(self):
        return self.name

    def check_errors(self, inps, outs):
        errors = []
        for idx, ((_, inp), (_, out)) in enumerate(zip(inps.iterrows(), outs.iterrows())):
            if self.callback(inp, out):
                errors.append(idx)
        return errors

    def get_assertion(self):
        return self.check_errors
