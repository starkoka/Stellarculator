from gpiozero import LED
from gpiozero import Button
from time import sleep

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


def output():
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
    return x, y, z


while True:
    n = input('2ケタ±2ケタの計算式を入れてくれ')
    if n[2] == '-':
        S = '1'
    else:
        S = '0'
    pi_input(n[0], n[1], S, n[3], n[4])
    print(output())