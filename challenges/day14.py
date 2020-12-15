"""
--- Day 14: Docking Data ---
As your ferry approaches the sea port, the captain asks for your help again. The computer system that runs this port isn't compatible with the docking program on the ferry, so the docking parameters aren't being correctly initialized in the docking program's memory.

After a brief inspection, you discover that the sea port's computer system uses a strange bitmask system in its initialization program. Although you don't have the correct decoder chip handy, you can emulate it in software!

The initialization program (your puzzle input) can either update the bitmask or write a value to memory. Values and memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.

The bitmask is always given as a string of 36 bits, written with the most significant bit (representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right. The current bitmask is applied to values immediately before they are written to memory: a 0 or 1 overwrites the corresponding bit in the value, while an X leaves the bit in the value unchanged.

For example, consider the following program:

mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite two bits in every written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten with 1.

The program then attempts to write the value 11 to memory address 8. By expanding everything out to individual bits, the mask is applied as follows:

value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)
So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program tries to write 101 to address 7:

value:  000000000000000000000000000001100101  (decimal 101)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001100101  (decimal 101)
This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to set. Finally, the program tries to write 0 to address 8:

value:  000000000000000000000000000000000000  (decimal 0)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001000000  (decimal 64)
64 is written to address 8 instead, overwriting the value that was there previously.

To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.) In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.

Execute the initialization program. What is the sum of all values left in memory after it completes?
"""

f = open("challenges\data\day14data.txt", "r")

def processData(file):
    data = []

    for x in f:
        x=x.strip().replace('\n', '').split(" = ")
        data.append((x[0], x[1]))

    return data

# Function to convert Decimal number  
# to Binary number  
def decimalToBinary(n):  
    return bin(n).replace("0b", "")

def leadingZeros(length, bin_num):
    leadingZeros = length - len(bin_num)
    return "0"*leadingZeros + bin_num

def initialize(commands):
    memory = {}
    mask = "X"*36
    for c in commands:
        if c[0] == "mask":
            mask = c[1]
        else:
            address = c[0][c[0].index("[")+1:len(c[0])-1]
            binaryValue = decimalToBinary(int(c[1]))
            
            binary36 = leadingZeros(36, binaryValue)
            
            memory[address] = ""
            for i in range(len(mask)):
                if mask[i] == "X":
                    memory[address] += binary36[i]
                else:
                    memory[address] += mask[i]
    sum = 0
    for val in memory.values():
        sum += int("".join(val), 2)

    return sum


"""
--- Part Two ---
For some reason, the sea port's computer system still can't communicate with your ferry's docking program. It must be using version 2 of the decoder chip!

A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts as a memory address decoder. Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address in the following way:

If the bitmask bit is 0, the corresponding memory address bit is unchanged.
If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
If the bitmask bit is X, the corresponding memory address bit is floating.
A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, this means the floating bits will take on all possible values, potentially causing many memory addresses to be written all at once!

For example, consider the following program:

mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
When this program goes to write to memory address 42, it first applies the bitmask:

address: 000000000000000000000000000000101010  (decimal 42)
mask:    000000000000000000000000000000X1001X
result:  000000000000000000000000000000X1101X
After applying the mask, four bits are overwritten, three of which are different, and two of which are floating. Floating bits take on every possible combination of values; with two floating bits, four actual memory addresses are written:

000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
000000000000000000000000000000111010  (decimal 58)
000000000000000000000000000000111011  (decimal 59)
Next, the program is about to write to memory address 26 with a different bitmask:

address: 000000000000000000000000000000011010  (decimal 26)
mask:    00000000000000000000000000000000X0XX
result:  00000000000000000000000000000001X0XX
This results in an address with three floating bits, causing writes to eight memory addresses:

000000000000000000000000000000010000  (decimal 16)
000000000000000000000000000000010001  (decimal 17)
000000000000000000000000000000010010  (decimal 18)
000000000000000000000000000000010011  (decimal 19)
000000000000000000000000000000011000  (decimal 24)
000000000000000000000000000000011001  (decimal 25)
000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
The entire 36-bit address space still begins initialized to the value 0 at every address, and you still need the sum of all values left in memory at the end of the program. In this example, the sum is 208.

Execute the initialization program using an emulator for a version 2 decoder chip. What is the sum of all values left in memory after it completes?
"""

def calculateCombinations(bin_address):
    combinations = []
    
    # xCount = 0
    xPositions = []

    for i in range(len(bin_address)):
        # find each X and add its idx to a list
        if bin_address[i] == "X":
            xPositions.append(i)
            # xCount += 1

    if len(xPositions) > 0:
        for i in range(2**(len(xPositions))):
            # need to generate all possible combos of 0s & 1s
            # w/ leading 0s
            possible = decimalToBinary(i)

            while len(possible) < len(xPositions):
                possible = "0"+possible
            
            combinations.append(possible)
        

    addresses = []

    for c in combinations:
        # need to insert combination[i] into binary number
        # current combo associated idx is in xPositions[i]
        newAddress = ""
        currPos = 0
        for i in range(len(bin_address)):
            if currPos < len(xPositions) and i == xPositions[currPos]:
                newAddress += c[currPos]
                currPos += 1
            else:
                newAddress += bin_address[i]
            
        
        addresses.append(newAddress)

    return addresses


def initialize_v2(commands):
    memory = {}
    mask = "X"*36
    for c in commands:
        if c[0] == "mask":
            mask = c[1]
        else:
            address = c[0][c[0].index("[")+1:len(c[0])-1]
            binaryAddress = decimalToBinary(int(address))
            binary36 = leadingZeros(36, binaryAddress)

            newVal = ""
            for i in range(len(mask)):
                if mask[i] != "0":
                    newVal += mask[i]
                else:
                    newVal += binary36[i]
                    
            addresses = calculateCombinations(newVal)
            
            for a in addresses:
                memory[a] = int(c[1])
    
    sum = 0
    for val in memory.values():
        sum += val
    # print(memory)
    return sum


data = processData(f)
# [print(d) for d in data]
sumAllValues = initialize(data)
print("Part 1:", sumAllValues)

sumAllValuesV2 = initialize_v2(data)
print("Part 2:", sumAllValuesV2)

# binary = decimalToBinary(33323)
# binary = leadingZeros(36, binary)
# print(binary)
# combos = initialize_v2([("mask", "100X100X101011111X100000100X11010011"),
# ("mem[33323]", "349380")])
# print(combos)