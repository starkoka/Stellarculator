from gpiozero import LED
from gpiozero import Button
from time import sleep
import csv

PI_INPUT_A = LED(20)
PI_INPUT_B = LED(21)  # ab = 緑
PI_INPUT_C = LED(15)
PI_INPUT_D = LED(7)  # cd = 青
PI_INPUT_S = LED(4)  # +なら0、-なら1

clock = 0

PI_OUTPUT_X = Button(26)
PI_OUTPUT_Y = Button(22)
PI_OUTPUT_Z = Button(5)

def pi_input(a, b, s, c, d):
    if a == '1':
        PI_INPUT_A.on()
    else:
        PI_INPUT_A.off()

    if b == '1':
        PI_INPUT_B.on()
    else:
        PI_INPUT_B.off()

    if s == '1':
        PI_INPUT_S.on()
    else:
        PI_INPUT_S.off()

    if c == '1':
        PI_INPUT_C.on()
    else:
        PI_INPUT_C.off()

    if d == '1':
        PI_INPUT_D.on()
    else:
        PI_INPUT_D.off()

    return


def pi_output():
    x = 0
    y = 0
    z = 0
    sleep(0)
    if PI_OUTPUT_X.is_pressed:
        x = 1
    if PI_OUTPUT_Y.is_pressed:
        y = 1
    if PI_OUTPUT_Z.is_pressed:
        z = 1
    return x, y, z


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
        c = (c - 1) * (-1)
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
                        pi_input(a,b,x,c,d)
                        print(str(r[0]) + str(r[1]) + str(r[2]), end="  |  ")
                        o = pi_output()
                        print(str(o[0]) + str(o[1]) + str(o[2]))

                        with open('output.csv', 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow([str(a) + str(b) + X + str(c) + str(d) , str(r[0]) + str(r[1]) + str(r[2])],str(o[0]) + str(o[1]) + str(o[2]))

a = input("演算モードは1,確認モードは2を入れてください")
if a == '2':
    while True:
        q = input("何かを入力したら実行")
        with open('output.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([])
        allcheck()
else:
    while True:
        n = input('2ケタ±2ケタの計算式を入れてくれ')
        if n[2] == '-':
            S = '1'
        else:
            S = '0'
        pi_input(n[0], n[1], S, n[3], n[4])
        print(pi_output())