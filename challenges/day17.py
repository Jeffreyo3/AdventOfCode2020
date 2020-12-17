""" 
--- Day 17: Conway Cubes ---
As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact you. They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket dimension! When you hear it's having problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small flat region of cubes (your puzzle input); the cubes in this region start in the specified active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the following rules:

If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and determine what the configuration of cubes should be at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###
Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......
After the full six-cycle boot process completes, 112 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?
"""

import re
f = open("challenges\data\day17data.txt", "r")

def processData(file):
  data = []
  for x in f:
    x=x.strip().replace('\n', '')
    data.append(x)
    
  return data

def createCube(data):
    zMin = int(-len(data)/2)
    zMax = int(len(data)/2)+1
    
    cube = {
        "key": ["x", "y", "z"],
        "xy_range": (0, len(data)),
        "z_range": (zMin, zMax)
    }

    for x in range(len(data)):
        for y in range(len(data[x])):
            for z in range(zMin, zMax):
                key = str(x) + " " + str(y) + " " + str(z)
                if(z == 0):
                    cube[key] = data[x][y]
                else:
                    cube[key] = "."
    return cube

def evalNeighbors(coords, cube):
    living = 0
    for x in range(coords["x"]-1, coords["x"]+2):
        for y in range(coords["y"]-1, coords["y"]+2):
            for z in range(coords["z"]-1, coords["z"]+2):
                if(x == coords["x"] and y == coords["y"] and z == coords["z"]):
                    # print("same", x, y, z)
                    continue
                key = str(x) + " " + str(y) + " " + str(z)
                # print(x,y,z)
                if(key in cube.keys()):
                    if(cube[key] == "#"):
                        living += 1
    # print("living:", living, "co", coords)
    return living
    
def simulate(cube, cycles):

    while(cycles > 0):
        cycles -= 1
        nextCube = {}
        nextCube["key"] = cube["key"]
        nextCube["z_range"] = (cube["z_range"][0]-1, cube["z_range"][1]+1)
        nextCube["xy_range"] = (cube["xy_range"][0]-1, cube["xy_range"][1]+1)

        for x in range(nextCube["xy_range"][0], nextCube["xy_range"][1]):
            for y in range(nextCube["xy_range"][0], nextCube["xy_range"][1]):
                for z in range(nextCube["z_range"][0], nextCube["z_range"][1]):
                    key = str(x) + " " + str(y) + " " + str(z)
                    if(not(key in cube.keys())):
                        cube[key] = "."
                    living = evalNeighbors({"x": x, "y": y, "z": z}, cube)
                    # if(living > 0):
                        # print(living, "---", key)

                    if(cube[key] == "#"):
                        if(living == 2 or living == 3):
                            nextCube[key] = cube[key]
                        else:
                            nextCube[key] = "."
                    else:
                        if(living == 3):
                            nextCube[key] = "#"
                        else:
                            nextCube[key] = cube[key]
        cube = nextCube

    return cube

def printCube(cube):
    for z in range(cube["z_range"][0], cube["z_range"][1]):
        print("z = ", z)
        for x in range(cube["xy_range"][0], cube["xy_range"][1]):
            row = ""
            for y in range(cube["xy_range"][0], cube["xy_range"][1]):
                key = str(x) + " " + str(y) + " " + str(z)
                row += cube[key]
            print(row)
             

def countLivingCells(cube):
    living = 0
    for z in range(cube["z_range"][0], cube["z_range"][1]):
        for x in range(cube["xy_range"][0], cube["xy_range"][1]):
            row = ""
            for y in range(cube["xy_range"][0], cube["xy_range"][1]):
                key = str(x) + " " + str(y) + " " + str(z)
                row += cube[key]
                if(cube[key] == "#"):
                    living += 1
    return living

data = processData(f)
cube = createCube(data)

cube = simulate(cube, 6)
living = countLivingCells(cube)
# printCube(cube)
print("Part 1:",living)
