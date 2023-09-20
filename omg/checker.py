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


class IdentifierConsistencyAssertion(object):
    def __init__(self, identifier, attribute):
        self.identifier = identifier
        self.attribute = attribute
        self.name = f'Identifier consistency {identifier}, {attribute}'

    def get_name(self):
        return self.name

    def check_errors(self, inps, outs):
        errors = []
        seen_pairs = defaultdict(lambda: defaultdict(list))
        for idx, ((_, inp), (_, out)) in enumerate(zip(inps.iterrows(), outs.iterrows())):
            seen_pairs[self.identifier][out[self.attribute]].append(idx)

        for iden_val, attr_to_idx in seen_pairs.items():
            if len(attr_to_idx) > 1:
                err = []
                for attr, idx_list in attr_to_idx.items():
                    err.append(idx_list[0])
                errors.append(err)

        return errors

    def get_assertion(self):
        return self.check_errors


class TimeConsistencyAssertion(object):
    def __init__(self, identifier, timestamp, window=3, allowed_transitions=1):
        self.identifier = identifier
        self.timestamp = timestamp
        self.window = window
        self.allowed_transitions = allowed_transitions
        self.name = f'Time consistency {identifier}, {window}'

    def get_name(self):
        return self.name

    def check_errors(self, inps, outs):
        errors = []
        groups = inps[[self.timestamp, self.identifier]].groupby(self.identifier)
        for iden_val, group in groups:
            timestamp_vals = group[self.timestamp].values
            timestamp_vals.sort()
            timestamp_vals.sort()
            for i, ts_start in enumerate(timestamp_vals):
                nb_transitions = 0
                for j, ts_other in enumerate(timestamp_vals[i + 1:]):
                    j += i + 1
                    if ts_other - ts_start > self.window:
                        break
                    if timestamp_vals[j] != timestamp_vals[j - 1] + 1:
                        nb_transitions += 2
                if nb_transitions > self.allowed_transitions:
                    err = group[self.timestamp].index[0]
                    errors.append(err)
        return errors

    def get_assertion(self):
        return self.check_errors