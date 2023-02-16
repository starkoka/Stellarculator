from gpiozero import LED
from gpiozero import Button
from time import sleep
import numpy
import math

clock = 0.05
CHANGE_EI= 0 #0なら内蔵、1なら外付け

if CHANGE_EI == 1:
    PI_INPUT_A = LED(15)
    PI_INPUT_B = LED(7)  # ab = 緑 ※修正前は逆になる
    PI_INPUT_C = LED(20)
    PI_INPUT_D = LED(21)  # cd = 青　※修正前は逆になる
    PI_INPUT_S = LED(4)  # +なら0、-なら1

    PI_OUTPUT_X = Button(26)
    PI_OUTPUT_Y = Button(22)
    PI_OUTPUT_Z = Button(5)


def pi_input(a, b, s, c, d): #ラズパイ入力用関数
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


def pi_output(): #ラズパイ出力用関数
    x = 0
    y = 0
    z = 0
    sleep(clock)
    if PI_OUTPUT_X.is_pressed:
        x = 1
    if PI_OUTPUT_Y.is_pressed:
        y = 1
    if PI_OUTPUT_Z.is_pressed:
        z = 1
    return str(x), str(y), str(z)


def fulladder(a, b, x):  # 内蔵1bit加減算機
    if a + b + x == 0:
        return 0, 0
    elif a + b + x == 1:
        return 0, 1
    elif a + b + x == 2:
        return 1, 0
    else:
        return 1, 1


def twoadder(a, b, x, c, d): #内蔵2bit加減算機
    a = int(a)
    b = int(b)
    x = int(x)
    c = int(c)
    d = int(d)
    if x == 1:
        c = (c - 1) * (-1)
        d = (d - 1) * (-1)
    n = fulladder(b, d, x)
    m = fulladder(a, c, n[0])

    return str(m[0]), str(m[1]), str(n[1])

def adderfunc(a, b, x, c, d): #切り替え対応関数
    if CHANGE_EI == 0:
        return twoadder(a, b, x, c, d)
    else:
        pi_input(a, b, x, c, d)
        return pi_output()

def allcheck(): #外付け回路動作チェック関数
    if CHANGE_EI == 1:
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
                            pi_input(str(a), str(b), str(x), str(c), str(d))
                            sleep(clock)
                            print(str(r[0]) + str(r[1]) + str(r[2]), end="  |  ")
                            o = pi_output()
                            print(str(o[0]) + str(o[1]) + str(o[2]))
    else:
        print("内蔵モードになっています！")

def add(add1,add2):
    if len(add1) < len(add2):
        add1, add2 = add2, add1

    for i in range(len(add1) - len(add2)):
        add2 = '0' + add2
    if len(add1) % 2 == 1:
        add1 = '0' + add1
        add2 = '0' + add2

    output = []
    kuriagari = '0'
    for i in range(len(add1) // 2):
        if kuriagari == '0':
            add3 = [add1[len(add1) - (i * 2) - 2], add1[len(add1) - (i * 2) - 1]]
            next_kuriagari = '0'
        else:
            if i % 2 == 0:  # 片方だけが01を頻繁に入力することを避けるコード
                adder = adderfunc(add1[len(add1) - (i * 2) - 2], add1[len(add1) - (i * 2) - 1], '0', '0', '1')
            else:
                adder = adderfunc('0', '1', '0', add1[len(add1) - (i * 2) - 2], add1[len(add1) - (i * 2) - 1])
            add3 = [adder[1], adder[2]]
            next_kuriagari = adder[0]
        adder = adderfunc(add3[0], add3[1], '0', add2[len(add2) - (i * 2) - 2], add2[len(add2) - (i * 2) - 1])

        output.insert(0, adder[2])
        output.insert(0, adder[1])
        kuriagari = max(adder[0], next_kuriagari)
    output.insert(0, kuriagari)
    add_result = ""
    for i in range(len(output)):
        add_result = add_result + output[i]
    return add_result


def multi(multi1,multi2):
    multi_result = multi1
    loop = len(str(bin(int(multi2,2)))[2:])-1 #multi2に含まれる最大の2の乗数を求める
    if loop != 0:
        for i in range(int(loop)):
            multi_result = add(multi_result, multi_result)
        remaining = multi(multi1, str(format(int(multi2, 2) - 2 ** loop, 'b')))
        multi_result = add(multi_result, remaining)
        return multi_result
    else:
        multi_result = '0'
        for i in range(int(multi2, 2)):
            multi_result = add(multi_result, multi1)
        return multi_result


a = input("演算モードは1,確認モードは2を入れてください")
if a == '2':
    while True:
        q = input("何かを入力したら実行")
        allcheck()

else:
    while True:
        n = str(format(int(input("足す数を入力")), 'b'))
        m = str(format(int(input("足される数を入力")), 'b'))
        print(int(multi(n,m),2))
