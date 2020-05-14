import pandas as pd
from omg.consistency import ConsistencyChecker

checker = ConsistencyChecker(
        timestamp='timestamp',
        identifiers=['iden1', 'iden2'],
        attributes=['iden2', 'atr1', 'atr2'],
        window=3,
        allowed_transitions=1
)

df = pd.read_csv('./data.csv', comment='#')
errors = checker.check(df)
for error in errors:
    print(error)
