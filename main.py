from gpiozero import LED
from time import sleep

PI_INPUT_A = LED(20)
PI_INPUT_B = LED(21)  # ab = 緑
PI_INPUT_C = LED(12)
PI_INPUT_D = LED(5)  # cd = 青
PI_INPUT_S = LED(4)  # +なら0、-なら1


# PI_OUTPUT_X = LED()
# PI_OUTPUT_Y = LED()
# PI_OUTPUT_Z = LED()

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


while True:
    n = input('2ケタ±2ケタの計算式を入れてくれ')
    if n[2] == '-':
        S = 1
    else:
        S = 0
    pi_input(int(n[0]), int(n[1]), S, int(n[3]), int(n[4]))
