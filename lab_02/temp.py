from random import randint as r


def mult(a):
    ans = 1
    for i in a:
        ans *= i

    return ans


for i in range(20):
    results = [r(1, 6), r(1, 6), r(1, 6)]
    for j in results:
        print(f"{j} ", end='')

    print(f" sum={sum(results)} damage={mult(results)}")
