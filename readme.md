Experiments with generating models for 3D printing using Python with `numpy-stl`.

# basic idea

All models use "X-shape" as a base building block
![X Shape](img/x.png)

X-shapes can be stacked to form a grid
![X Shape](img/3x2.png)

If stacked at an angle, they might form cylindrical or spiral shapes
![Cylindrical stack](img/toy.png)
![Spiral stack](img/roll-demo.png)

Each cell might have its own "fullness". Here fullness increases from the bottom to the top
![Variable fullness](img/variable-fullness.png)

# how to use

1. install python >=3.9
2. install dependencies from requirements.txt
3. `PYTHONPATH=. python configs/<config>.py`

See the list of configs in the config folder

You can change any parameters in the config to adjust model.


# models showcase

Mosquito net roll
![Mosquito net roll](img/roll.png)

Glass with groove
![Glass with groove](img/glass_with_groove.png)

Glass
![Glass](img/glass.png)

Vases
![Vase1](img/vase1.png)
![Vase2](img/vase2.png)
![Vase3](img/vase3.png)
![Vase4](img/vase4.png)
![Vase5](img/vase5.png)

Lampshade
![Lampshade](img/lampshade.png)

Plate
![Plate](img/plate.png)
