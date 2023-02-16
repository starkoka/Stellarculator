from gpiozero import LED
from gpiozero import Button
from time import sleep

bitclock = 0.05
CHANGE_EI= 0 #0なら内蔵、1なら外付け

if CHANGE_EI == 1:
    PI_INPUT_A = LED(15)
    PI_INPUT_B = LED(7)  # ab = 緑
    PI_INPUT_C = LED(20)
    PI_INPUT_D = LED(21)  # cd = 青
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
    sleep(bitclock)
    if PI_OUTPUT_X.is_pressed:
        x = 1
    if PI_OUTPUT_Y.is_pressed:
        y = 1
    if PI_OUTPUT_Z.is_pressed:
        z = 1
    return str(x), str(y), str(z)

def clock():
    mode = input("自分でクロック数を決定するには1を、標準クロックを使うにはそれ以外の入力をしてください")
    if mode == '1':
        c = float(input("クロック数を入力"))
    else:
        c = 0.05
    return c

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
                            sleep(bitclock)
                            print(str(r[0]) + str(r[1]) + str(r[2]), end="  |  ")
                            o = pi_output()
                            print(str(o[0]) + str(o[1]) + str(o[2]))
    else:
        print("内蔵モードになっています！")

def add(add1,add2):
    add1 = str(add1)
    add2 = str(add2)
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
    return int(add_result,2)


def multi(multi1,multi2):
    multi_result = multi1
    loop = len(str(bin(int(multi2,2)))[2:])-1 #multi2に含まれる最大の2の乗数を求める
    if loop != 0:
        for i in range(int(loop)):
            multi_result = int(format(add(multi_result, multi_result), 'b'))
        remaining = int(format(multi(multi1, str(format(int(multi2, 2) - 2 ** loop, 'b'))), 'b'))
        multi_result = int(format(add(multi_result, remaining), 'b'))
        return int(str(multi_result),2)
    else:
        multi_result = '0'
        for i in range(int(multi2, 2)):
            multi_result = int(format(add(multi_result, multi1), 'b'))
        return int(str(multi_result),2)

def subtract(sub1,sub2):
    if len(sub1) < len(sub2):
        for i in range(len(sub2) - len(sub1)):
            sub1 = '0' + sub1
    else:
        for i in range(len(sub1) - len(sub2)):
            sub2 = '0' + sub2
    complement = 0
    if len(sub1) % 2 == 1:
        sub1 = '0' + sub1
        sub2 = '0' + sub2
        complement = 1

    output = []
    maegari = '1'
    for i in range(len(sub1) // 2):
        if maegari == '1':
            sub3 = [sub1[len(sub1) - (i * 2) - 2],sub1[len(sub1) - (i * 2) - 1]]
            next_maegari = 1
        else:
            sub = adderfunc(sub1[len(sub1) - (i * 2) - 2],sub1[len(sub1) - (i * 2) - 1],'1','0','1')
            sub3 = [sub[1],sub[2]]
            next_maegari = int(sub[0])
        subtraction = adderfunc(sub3[0],sub3[1],'1',sub2[len(sub2) - (i * 2) - 2],sub2[len(sub2) - (i * 2) - 1])

        output.insert(0, subtraction[2])
        output.insert(0, subtraction[1])
        maegari = str(min(int(subtraction[0]), next_maegari))
    sub_result = ""

    if maegari == '0':
        for i in range(len(output) - complement):
            if output[i + complement] == '0':
                sub_result = sub_result + '1'
            else:
                sub_result = sub_result + '0'
        sub_result = int(format(add(sub_result, '1'), 'b'),2)
        sub_result = 0-sub_result
    else:
        for i in range(len(output)):
            sub_result = sub_result + output[i]
        sub_result = int(sub_result, 2)
    return sub_result

bitclock = clock()
while True:
    a = input("演算モードは1,確認モードは2、クロック決定モードは3を入れてください")
    if a == '2':
        allcheck()
    elif a == '3':
        bitclock = clock()
    else:
        while True:
            text = input("式を入力")
            nm = 0
            n = ''
            m = ''
            mark = ''

            for i in range(len(text)):
                if text[i] == '+' or text[i] == '-' or text[i] == '*':
                    nm = 1
                    mark = text[i]
                elif nm == 1:
                    m = m + text[i]
                else:
                    n = n + text[i]

            n = str(format(int(n), 'b'))
            m = str(format(int(m), 'b'))
            if mark == '*':
                print(multi(n, m))
            elif mark == '+':
                print(add(n, m))
            elif mark == '-':
                print(subtract(n, m))

