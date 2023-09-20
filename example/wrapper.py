import functools
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
import sklearn.datasets
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from omg.checker import Checker

def main():
    # Source: https://medium.com/@amitg0161/sklearn-linear-regression-tutorial-with-boston-house-dataset-cde74afd460a
    # Dataset loading, introspection
    dataset = sklearn.datasets.load_boston()
    print(dataset.DESCR)
    df = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    df['PRICE'] = dataset.target
    print(df.head())

    # Splitting into train, test
    X = df.drop('PRICE', axis=1)
    y = df['PRICE']
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2, random_state=42)

    # Fitting
    reg_all = LinearRegression()
    reg_all.fit(X_train, y_train)

    # Train performance
    y_train_predict = reg_all.predict(X_train)
    rmse = (np.sqrt(mean_squared_error(y_train, y_train_predict)))
    r2 = round(reg_all.score(X_train, y_train), 2)
    print("The model performance for training set")
    print("--------------------------------------")
    print('RMSE is {}'.format(rmse))
    print('R2 score is {}'.format(r2))
    print("\n")


    # Test performance
    y_pred = reg_all.predict(X_test)
    rmse = (np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = round(reg_all.score(X_test, y_test),2)
    print("The model performance for training set")
    print("--------------------------------------")
    print("Root Mean Squared Error: {}".format(rmse))
    print("R^2: {}".format(r2))
    print("\n")

    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual House Prices ($1000)")
    plt.ylabel("Predicted House Prices: ($1000)")
    plt.xticks(range(0, int(max(y_test)), 2))
    plt.yticks(range(0, int(max(y_test)), 2))
    plt.title("Actual Prices vs Predicted prices")
    plt.show()

    print(y_pred.min())

    def pred_fn(df, model=None):
        X = df.values
        y_pred = model.predict(X)
        return y_pred

    def output_pos(inps, outs):
        errors = []
        for idx, out in enumerate(outs):
            if out < 0:
                errors.append(idx)
        return errors

    predictor = functools.partial(pred_fn, model=reg_all)
    checker = Checker(name='Housing price checker')
    checker.register_assertion(output_pos, 'Output positive')
    predictor = checker.wrap(predictor)

    predictor(X_test)

if __name__ == '__main__':
    main()