"""
--- Day 8: Handheld Halting ---
Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to you.

Their handheld game console won't turn on! They ask if you can take a look.

You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should be able to fix it, but first you need to be able to run the code in isolation.

The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
For example, consider the following program:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
These instructions are visited in this order:

nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |
First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.

This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to run any instruction a second time, you know it will never terminate.

Immediately before the program would run an instruction a second time, the value in the accumulator is 5.

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?
"""
import re
f = open("challenges\data\day8data.txt", "r")

def processData(file):
  data = []

  for x in f:
    x=x.strip().replace('\n', '').split()
    data.append(x)

  return data

class Handheld:

    def __init__(self, commandList):
        self.commandList = commandList
        self.accumulator = 0
    
    def printList(self):
        [print(item) for item in self.commandList]
    
    def noOp(self):
        print("No OPeration. Continuing to next command.")

    def accumulate(self, value):
        if value > 0:
            print("Increasing accumulator to:", (self.accumulator + value))
        elif value < 0:
            print("Decreasing accumulator to:", (self.accumulator + value))
        else:
            print("Accumulator is not changing. Value:", self.accumulator)

    def jump(self, idx, jmpInterval):
        print("Jumping from command:", idx, "to command:", (idx + jmpInterval))

    def executeCommands(self):
        self.accumulator = 0
        visited = set()
        idx = 0

        while idx < len(self.commandList):
            if idx in visited:
                # print("Error: Endless loop detected")
                return False
            visited.add(idx)
            if self.commandList[idx][0] == "acc":
                # self.accumulate(int(self.commandList[idx][1]))
                self.accumulator += int(self.commandList[idx][1])
                idx += 1
            elif self.commandList[idx][0] == "nop":
                # self.noOp()
                idx += 1
            elif self.commandList[idx][0] == "jmp":
                # self.jump(idx, int(self.commandList[idx][1]))
                idx += int(self.commandList[idx][1])

        return True
    
    def boot(self):
        if not self.executeCommands():
            print("Error: Endless loop detected")
        return self.accumulator

    def swapCommand(self, command):
        if command == "jmp":
            return "nop"
        elif command == "nop":
            return "jmp"
        else:
            return command

    def fixEndlessLoop(self):
        # hold our original
        copyCommands = self.commandList

        for command in copyCommands:
            if command[0] != "nop" and command[0] != "jmp":
                continue

            # swap a command
            command[0] = self.swapCommand(command[0])
            
            # update list
            self.commandList = copyCommands
            if (self.executeCommands()):
                print("New list successfully terminates")
                return self.accumulator
            else:
                # if unsuccessful, swap back for next iteration
                command[0] = self.swapCommand(command[0])
        
        return None


commandList = processData(f)
h = Handheld(commandList)

print("Part 1:", h.boot())
print("Part 2:", h.fixEndlessLoop())
