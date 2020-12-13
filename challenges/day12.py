"""
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
"""

f = open("challenges\data\day12data.txt", "r")

def processData(file):
  data = []

  for x in f:
    x=x.strip().replace('\n', '')
    data.append((x[0], int(x[1:])))

  return data



class Ship:

    def __init__(self, facing, instructions):
        self.facing = facing.upper()
        self.instructions = instructions
        self.directions = {
            "N": self.moveNorth,
            "S": self.moveSouth,
            "E": self.moveEast,
            "W": self.moveWest
        }
        self.rotateDirections = {
            "R": self.rotateClockwise,
            "L": self.rotateCounterClockwise
        }
        self.coords = {
            # north positive; south negative
            "north_south": 0,
            # east positive; west negative
            "east_west": 0
        }

    def moveNorth(self, value):
        self.coords["north_south"] += value
    def moveSouth(self, value):
        self.coords["north_south"] -= value
    def moveEast(self, value):
        self.coords["east_west"] += value
    def moveWest(self, value):
        self.coords["east_west"] -= value
    
    def rotate(self, rotations):
        compass = ["N", "E", "S", "W"]
        curr = compass.index(self.facing)
        self.facing = compass[(curr + rotations) % 4]

    def rotateClockwise(self, value):
        rotations = 0
        while(value > 0):
            rotations += 1
            value -= 90
        self.rotate(rotations)
    def rotateCounterClockwise(self, value):
        rotations = 0
        while(value > 0):
            rotations -= 1
            value -= 90
        self.rotate(rotations)

    def navigate(self):
        for instruction in self.instructions:
            
            if instruction[0] == "F":
                self.directions[self.facing](instruction[1])
            elif instruction[0] in self.directions.keys():
                self.directions[instruction[0]](instruction[1])
            elif instruction[0] in self.rotateDirections.keys():
                self.rotateDirections[instruction[0]](instruction[1])
            else: 
                raise ValueError("Unreadable instruction")
    
    def findManhattanDistance(self):
        return abs(self.coords["north_south"]) + abs(self.coords["east_west"])



ship = Ship("e", processData(f))
ship.navigate()
print("Part 1:", ship.findManhattanDistance())
