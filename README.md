[![Build Status](https://travis-ci.com/Nyandams/step_detection.svg?branch=master)](https://travis-ci.com/Nyandams/step_detection)
# Escalator

A small python package to detect stagnation in the values of a signal, sort of **horizontal steps**.

## Installation
```
pip install escalator-nyandams
```

## Example
```python
import step_detection as esc

signal: list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 30, 31, 29, 30, 30, 29, 32, 45, 70, 70, 71, 69, 72, 70, 70, 70, 75, 78, 85, 85, 90, 95, 100, 100, 100, 101, 100, 101, 100, 100, 100, 99, 100, 100]
cost = esc.DistanceMedianCost()
algo = esc.EscalatorRush(cost=cost, min_step_size=3, max_dist=2, jump=1).fit(signal)
stair_steps = algo.predict()
#  [(0, 10, 0.0), (11, 18, 29.833333333333332), (19, 27, 70.28571428571429), (33, 45, 100.0909090909091)]
```
You can then plot easily the result with your favorite package.

![Example 1 of the result](https://raw.githubusercontent.com/Nyandams/step_detection/master/images/plat1.png)
![Example 2 of the result](https://raw.githubusercontent.com/Nyandams/step_detection/master/images/plat2.png)
