"""
Challenge 1:
Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
"""
# "\\r?\\n"
import re
f = open("challenges\data\day1data.txt", "r")

def processData(file):
  data = []
  for x in f:
    x=x.strip().replace('\n', '')
    data.append(int(x))

  return data

data = processData(f)

def findProductOfTwoNumsSummingToTarget(arr, target):
  dictionary = {}
  for num in arr:
    difference = target - num
    if difference in dictionary.keys():
      return difference * num
    
    dictionary[num] = difference
    
  return None

result = findProductOfTwoNumsSummingToTarget(data, 2020)
print(result)

"""
Challenge 2:
The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?

"""

def findProductOfThreeNumsSummingToTarget(arr, target):
  arr.sort()
  
  for i in range(0, len(arr) - 2):
    first = i + 1
    last = len(arr) - 1
    while(first < last):
      if ( arr[i] + arr[first] + arr[last] == target):
        return arr[i] * arr[first] * arr[last]
      elif( arr[i] + arr[first] + arr[last] < target):
        first += 1
      else:
        last -= 1
  return None

result = findProductOfThreeNumsSummingToTarget(data, 2020)
print(result)