import pandas as pd


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

    def retrieve_errors(self):
        df = pd.DataFrame()
        for err_idx, (asst_name, inp, out) in enumerate(self.errors):
            df_tmp = pd.concat([inp.reset_index(drop=True), out.reset_index(drop=True)], axis=1)
            df_tmp['assertion'] = asst_name
            df_tmp['err_idx'] = err_idx
            df_tmp = df_tmp.loc[:, ~df_tmp.columns.duplicated()]

            if len(df) > 0:
                df = df.append(df_tmp)
            else:
                df = df_tmp
        return df.reset_index(drop=True)

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
                    if type(err) is not list:
                        err = [err]
                    self.errors.append((asst_name, inps.iloc[err], outs.iloc[err]))
            if self.verbose:
                print(self.retrieve_errors())
            return outs
        return wrapper