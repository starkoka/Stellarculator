from gpiozero import Button
from time import sleep


def fulladder(a, b, x):  # 作成用関数
    if a + b + x == 0:
        return 0, 0
    elif a + b + x == 1:
        return 0, 1
    elif a + b + x == 2:
        return 1, 0
    else:
        return 1, 1


def twoadder(a, b, x, c, d):
    if x == 1:
        b = (b - 1) * (-1)
        d = (d - 1) * (-1)
    n = fulladder(b, d, x)
    m = fulladder(a, c, n[0])

    return m[0], m[1], n[1]


def allcheck():
    for x in range(2):
        if x == 0:
            X = '+'
        else:
            X = '-'
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    for d in range(2):
                        print(str(a) + str(b) + X + str(c) + str(d) + ' = ', end="")
                        r = twoadder(a, b, x, c, d)
                        print(str(r[0]) + str(r[1]) + str(r[2]))


while True:
    q = input("何かを入力したら実行")
    allcheck()
