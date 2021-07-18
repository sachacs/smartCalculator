# write your code here
import re
from collections import deque


def signal(s):
    if "-" in s and len(s) % 2 != 0:
        return "-"
    elif "+" in s:
        return "+"
    elif (len(s) > 2 and "*" in s) or (len(s) > 1 and "/" in s):
        raise Exception("Invalid expression")
    elif s == "^":
        return "**"
    else:
        return s


def iscommand(cmd):
    keep = True
    if cmd =="/help":
        print("I'm using eval function")
    elif cmd=="/exit":
        print("Bye!")
        keep = False
    else:
        print("Unknown command")
    return keep


def isvariable(variable):
    if re.match("[a-zA-Z]+$", variable) is None:
        raise Exception("Invalid identifier")
    return variable


def isvalue(variable,dict):
    if variable.isnumeric():
        return variable
    elif isvariable(variable) and variable not in dict:
        raise Exception("Unknown variable")
    elif isvariable(variable) and variable in dict:
        return dict[variable]
    else:
         raise Exception("Invalid assignment")
    return variable


def prepareEquation(string, dict):
    equation = string
    for key, value in dict.items():
        equation = equation.replace(key, value)
    return equation



def bracketsCheck(equation):
    brackets = sum([1 for x in equation if x =="("])
    brackets+= sum([-1 for x in equation if x ==")"])
    if brackets!=0:
        raise Exception("Invalid expression")


def checkequation(equation, variables):
    eq = []
    for e in equation:
        if e.isalnum():
            eq.append(isvalue(e, variables))
        else:
            eq.append(signal(e))

    return eq

def checkInvalidExpression(equation):
    pattern = r"[\*]{3,}"
    if re.search(pattern, equation) is not None:
        raise Exception("Invalid expression")

    pattern = r"[\/]{2,}"
    if re.search(pattern, equation) is not None:
        raise Exception("Invalid expression")

    bracketsCheck(equation)


def arrangeEquation(equation):

    delimiters = '^', '**', '/', '*', '-', '+','(',')',' '
    equation = "".join(x for x in equation if not x.isspace())
    regexPattern =  '|'.join('(?={})'.format(re.escape(delim)) for delim in delimiters)
    equation = re.sub('([A-Za-z0-9]+(\.[A-Za-z0-9]+)?)', r' \1 ', equation)#'(\d+(\.\d+)?)'
    #equation = re.sub('([\(\)]*([\(\)]*)?)', r' \1 ', equation)#'(\(*\)*(\.\(*\)*)?)'

    equation = re.split(regexPattern, equation)
    return list(x.strip() for x in equation if len(x) >= 1 and not x.isspace())


def postfix(equation):
    priority_operators = {'^': 3, '**': 3, '/': 2, '*': 2, '-': 1, '+': 1}
    operators = deque()
    postfix = deque()
    for e in equation:
        if e.isalnum():
            postfix.append(e)
        elif len(operators) <= 0 or operators[-1] == "(":
            operators.append(e)
        elif e == "(":
            operators.append(e)
        elif e == ")":
            a = e
            while a != "(":
                a = operators.pop()
                if a not in "(,)":
                    postfix.append(a)
        elif priority_operators.get(e) > priority_operators.get(operators[-1]):
            operators.append(e)
        elif priority_operators.get(e) <= priority_operators.get(operators[-1]):
            a = operators[-1]
            while a != "(" and priority_operators.get(e) <= priority_operators.get(a):
                a = operators[-1]
                if a not in "(,)":
                    postfix.append(operators.pop())
                if len(operators)<= 0:
                    break

            operators.append(e)
    for _ in range(len(operators)):
        postfix.append(operators.pop())

    return postfix

def calc(postfix, variables):
    result = 0
    temp = []
    for term in postfix:
        if term.isalnum():
            temp.append(prepareEquation(term, variables))
        else:
            a = str(temp.pop())
            b = str(temp.pop())
            temp.append(eval(b + term + a))

    result = temp[-1]

    return int(result)

if __name__ == "__main__":
    keep = True
    variables = {}

    while keep:
        i = input()
        if i.startswith("/"):
           keep = iscommand(i)
           continue
        elif len(i)<=0 or i.isspace():
            continue
        else:
            try:
                if "=" in i:
                  vlist = list(map(str, i.split("=")))
                  key = isvariable(vlist[0].strip())
                  value = isvalue(vlist[1].strip(), variables)
                  variables[key] = value

                else:
                        checkInvalidExpression(i)
                        i = arrangeEquation(i)
                        equation = checkequation(i, variables)
                        print(calc(postfix(equation), variables))

            except Exception as err:
                print(err.__str__())

