from gpiozero import LED
from time import sleep

INPUT_A = LED(20)
INPUT_B = LED(21)  # ab = 緑
INPUT_C = LED(12)
INPUT_D = LED(5)  # cd = 青
INPUT_S = LED(4)  # +なら0、-なら1


# OUTPUT_X = LED()
# OUTPUT_Y = LED()
# OUTPUT_Z = LED()

def pi_input(a, b, s, c, d):
    if a == '1':
        INPUT_A.on()
    else:
        INPUT_A.off()

    if b == '1':
        INPUT_B.on()
    else:
        INPUT_B.off()

    if s == '1':
        INPUT_S.on()
    else:
        INPUT_S.off()

    if c == '1':
        INPUT_C.on()
    else:
        INPUT_C.off()

    if d == '1':
        INPUT_D.on()
    else:
        INPUT_D.off()
    return


while True:
    n = input('2ケタ±2ケタの計算式を入れてくれ')
    if n[2] == '-':
        S = 1
    else:
        S = 0
    pi_input(int(n[0]), int(n[1]), S, int(n[3]), int(n[4]))
