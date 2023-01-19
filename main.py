from gpiozero import LED
from time import sleep

a = LED(20)
b = LED(21) #ab = 緑
c = LED(12)
d = LED(5) #cd = 青
s = LED(4)

while True:
        n = input('数字入れてくれ')
        if n[0] == '1':
            a.on()
        else:
            a.off()

        if n[1] == '1':
                b.on()
        else:
            b.off()

        if n[3] == '1':
            c.on()
        else:
            c.off()

        if n[4] == '1':
            d.on()
        else:
            d.off()

        if n[2] == '+':
            s.off()
        else:
            s.on()
