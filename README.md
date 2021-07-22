# Model Assertions for Monitoring and Improving Machine Learning

This is the project page for [Model Assertions for Monitoring and Improving Machine Learning](https://arxiv.org/abs/2003.01668).

Please read the [paper](https://arxiv.org/abs/2003.01668) for full technical details.


# Installation

```
pip install model_assertions
```


# Examples

We provide two examples.


## Housing price prediction

The first example (`Tabular.ipynb`) shows an example of predicting house prices from features.
This example trains a lienar model to predict the house price. 

We define a model assertion that asserts the predicted house price should be positive.
While seemingly simple, the predictions violate this assertion!


## Predicting people and attributes

The second example (`Consistency.ipynb`) shows an example of predcting people in a TV show and several attributes of the person (gender and hair color).
In this example, we assume that the predictions are already provided.

This example shows how to use the attribute- and time-consistency APIs.
It asserts that the same person in the same scene should have the same gender and hair color.
It also asserts that a person in the same scene should appear across consecutive frames without gaps.


# Citation 

If you find this project useful, please cite us at
```
@article{kang2020model,
  title={Model assertions for monitoring and improving ML model},
  author={Kang, Daniel and Raghavan, Deepti and Bailis, Peter and Zaharia, Matei},
  journal={MLSys},
  year={2020}
}
```
and contact us if you deploy model assertions!
