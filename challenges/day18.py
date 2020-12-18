""" 
--- Day 18: Operation Order ---
As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71
Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51
Here are a few more examples:

2 * 3 + (4 * 5) becomes 26.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?
"""

import re
f = open("challenges\data\day18data.txt", "r")

def processData(file):
    data = []
    for x in f:
        x=x.strip().replace('\n', '')
        data.append(x)
    
    return data

def evalEquationString(equation):
    operations = []
    stack = []
    def apply_top_op():
        if operations[-1] == '+':
            stack[-2:] = [stack[-2] + stack[-1]]
        elif operations[-1] == '*':
            stack[-2:] = [stack[-2] * stack[-1]]
        else:
            raise Exception(f"Bad state; opstack {operations} stack {stack}")
        operations.pop()

    for m in re.finditer(r'([()])|(\d+)|([+*])', equation):
        if m.group(1) == '(':
            operations.append('(')
        elif m.group(1) == ')':
            while operations[-1] != '(':
                apply_top_op()
            operations.pop()
        elif m.group(2):
            stack.append(int(m.group(2)))
        else:
            while operations and operations[-1] != '(':
                apply_top_op()
            operations.append(m.group(3))
    while operations:
        apply_top_op()
    assert len(stack) == 1, f"operations {operations} stack {stack}"
    return stack[0]

def sumResultingValues(arr):
    count = 0
    for equationString in arr:
        count += evalEquationString(equationString)
    return count


data = processData(f)
print(sumResultingValues(data))