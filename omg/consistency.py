class InconsistentAttributeError(object):
    def __init__(
            self,
            identifier,
            iden_val,
            attribute,
            atr_val1,
            atr_val2,
    ):
        self.identifier = identifier
        self.iden_val = iden_val
        self.attribute = attribute
        self.atr_val1 = atr_val1
        self.atr_val2 = atr_val2

    def __str__(self):
        return 'Attribute error in identify value {} ({}), attribute {} has: {}, {}'.format(
                self.iden_val,
                self.identifier,
                self.attribute,
                self.atr_val1,
                self.atr_val2
        )

    def __repr__(self):
        return 'Attribute error, {}, {}: {}, {}, {}'.format(
                self.identifier,
                self.attribute,
                self.iden_val,
                self.atr_val1,
                self.atr_val2
        )


class TransitionError(object):
    def __init__(
            self,
            identifier,
            iden_val,
            start_ts,
            row_id
    ):
        self.identfier = identifier
        self.iden_val = iden_val
        self.start_ts = start_ts
        self.row_id = row_id

    def __str__(self):
        return 'Transition error for identity value {} ({}), at timestamp {} (row {})'.format(
                self.iden_val,
                self.identfier,
                self.start_ts,
                self.row_id
        )

    def __repr__(self):
        return 'Transition error, {} {}: {} ({})'.format(
                self.identfier,
                self.iden_val,
                self.start_ts,
                self.row_id
        )


class ConsistencyChecker(object):
    def __init__(
            self,
            timestamp,
            identifiers,
            attributes,
            window=1,
            allowed_transitions=1
    ):
        self.timestamp = timestamp
        self.identifiers = identifiers
        self.attributes = attributes
        self.window = window
        self.allowed_transitions = allowed_transitions

    def _get_attr_errors(self, identfier, iden_val, attribute, group):
        errors = []
        atr_vals = group[attribute].unique()
        for i, atr_val1 in enumerate(atr_vals[:-1]):
            for atr_val2 in atr_vals[i + 1]:
                error = InconsistentAttributeError(
                        identfier,
                        iden_val,
                        attribute,
                        atr_val1,
                        atr_val2
                )
                errors.append(error)
        return errors

    def _check_attrs(self, df):
        errors = []
        for identifier in self.identifiers:
            for attribute in self.attributes:
                if identifier == attribute:
                    continue
                groups = df[[identifier, attribute]].groupby(identifier)
                for iden_val, group in groups:
                    atr_vals = group[attribute].unique()
                    if len(atr_vals) != 1:
                        errors += self._get_attr_errors(identifier, iden_val, attribute, group)
        return errors

    def _check_transitions(self, df):
        errors = []
        for identifier in self.identifiers:
            groups = df[[self.timestamp, identifier]].groupby(identifier)
            for iden_val, group in groups:
                timestamp_vals = group[self.timestamp].values
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
                        row_id = group[self.timestamp].index[0]
                        error = TransitionError(identifier, iden_val, ts_start, row_id)
                        errors.append(error)
        return errors

    def check(self, df):
        errors = []
        errors += self._check_attrs(df)
        errors += self._check_transitions(df)
        return errors
