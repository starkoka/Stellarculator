from gpiozero import Button

def fulladder(a,b,x): #作成用関数
    if a+b+x == 0:
        return 0,0
    elif a+b+x == 1:
        return 0,1
    elif a+b+x == 2:
        return 1,0
    else:
        return 1,1
