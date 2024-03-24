Experiments with generating models for 3D printing using Python with `numpy-stl`.

# basic idea

All models use "X-shape" as a base building block:
![X Shape](img/x.png)

X-shapes can be stacked to form a grid:
![X Shape](img/3x2.png)

If stacked at an angle, they might form cylindrical or spiral shapes:
![Cylindrical stack](img/toy.png)
![Spiral stack](img/roll-demo.png)

Each cell might have its own "fullness":
![Variable fullness](img/variable-fullness.png)

# How to use

1. install python >=3.9
2. install dependencies from requirements.txt
3. `PYTHONPATH=. python configs/<config>.py`

See the list of configs in the config folder

You can change any parameters in the config to adjust model.


# models



