# AI task planning in Python

This is a project written in Python 3, which uses the numpy and pygame libraries. You can install them with:

```
pip install numpy
pip install pygame
```

The different task planning exercises are structured as follows:

## P21: Multi Agent Collision Avoidance

Multiple agents have to reach their destination without colliding between themselves in a map.

## P22: Vehicle Routing Problem

Multiple agents have to coordinate themselves to visit all the points in a map in the least possible time. This is a variant of the travelling salesperson problem.

## P23: UAV Search

A single agent has to travel around a map and scan its whole surface in the least possible time. For executing this exercise, it is necessary to comment the P22 part and uncomment the P23 part in main.py before launching.

## P25: Formation along trajectory

A leader agent executes a route and several agents have to coordinate to keep a formation while following it.

The project is always executed in the exercise respective folder with the command:

```
python main.py
```