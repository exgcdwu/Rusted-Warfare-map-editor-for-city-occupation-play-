from asteval import Interpreter

aeval = Interpreter()

#alz = [[str([[0, 2, 4], [6, 8], [1, 3, 5, 7, 9], [-3, -2, -1]][ti][tj]),str(ti)] for ti in range(4) for tj in range([3, 2, 5, 3][ti])]

#print(alz)
#print(aeval("[[str([[0, 2, 4], [6, 8], [1, 3, 5, 7, 9], [-3, -2, -1]][ti][tj]),str(ti)] for ti in range(4) for tj in range([3, 2, 5, 3][ti])]"))

al = dict(sum([[[str([[0, 2, 4], [6, 8], [1, 3, 5, 7, 9], [-3, -2, -1]][ti][tj]),str(ti)] for tj in range([3, 2, 5, 3][ti])] for ti in range(4)], []))

print(al)

for i, j in [2, 4, 3], [3, 5, 4]:
    print(f"i:{i}")
    print(f"j:{j}")

