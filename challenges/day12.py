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


instructions = processData(f)
ship = Ship("e", instructions)
ship.navigate()
print("Part 1:", ship.findManhattanDistance())


"""
--- Part Two ---
Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.
The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.

For example, using the same instructions as above:

F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?
"""

class Boat:
    
    def __init__(self, facing, instructions, waypoint_ns, waypoint_ew):
        self.facing = facing.upper()
        self.instructions = instructions
        self.waypoint = {
            # north positive; south negative
            "north_south": waypoint_ns,
            # east positive; west negative
            "east_west": waypoint_ew
        }
        self.coords = {
            "north_south": 0,
            "east_west": 0
        }
        self.directions = {
            "N": self.moveWaypointNorth,
            "S": self.moveWaypointSouth,
            "E": self.moveWaypointEast,
            "W": self.moveWaypointWest,
            "F": self.moveToWaypoint
        }
        self.rotateDirections = {
            "R": self.rotateWaypointClockwise,
            "L": self.rotateWaypointCounterClockwise
        }


    def moveWaypointNorth(self, value):
        self.waypoint["north_south"] += value
    def moveWaypointSouth(self, value):
        self.waypoint["north_south"] -= value
    def moveWaypointEast(self, value):
        self.waypoint["east_west"] += value
    def moveWaypointWest(self, value):
        self.waypoint["east_west"] -= value


    def rotateWaypoint(self, rotations):
        turns = rotations % 4
        
        if rotations < 0 and rotations % 2 != 0:
            mod = (-rotations) % 4
            turns = -mod
        
        temp_ns = self.waypoint["north_south"]
        temp_ew = self.waypoint["east_west"]
        if turns == 1 or turns == -3:
            self.waypoint["north_south"] = -temp_ew
            self.waypoint["east_west"] = temp_ns
        elif turns == 3 or turns == -1:
            self.waypoint["north_south"] = temp_ew
            self.waypoint["east_west"] = -temp_ns
        elif turns == 2:
            self.waypoint["north_south"] = -temp_ns
            self.waypoint["east_west"] = -temp_ew
        else:
            pass
        
    def rotateWaypointClockwise(self, value):
        rotations = 0
        while(value > 0):
            rotations += 1
            value -= 90
        self.rotateWaypoint(rotations)
        
    def rotateWaypointCounterClockwise(self, value):
        rotations = 0
        while(value > 0):
            rotations -= 1
            value -= 90
        self.rotateWaypoint(rotations)
        


    def moveToWaypoint(self, value):
        
        self.coords["north_south"] += (self.waypoint["north_south"] * value)
        self.coords["east_west"] += (self.waypoint["east_west"] * value)

    def navigate(self):
        for instruction in self.instructions:
            if instruction[0] in self.directions.keys():
                self.directions[instruction[0]](instruction[1])
            elif instruction[0] in self.rotateDirections.keys():
                self.rotateDirections[instruction[0]](instruction[1])
            else: 
                raise ValueError("Unreadable instruction")

    
    def findManhattanDistance(self):
        return abs(self.coords["north_south"]) + abs(self.coords["east_west"])

boat = Boat("e", instructions, 1, 10)
boat.navigate()
print("Part 2:", boat.findManhattanDistance())