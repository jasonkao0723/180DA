import keyboard
import sys

def printStuff(a=1, b=2):
    while True:
        print('Running')
        if keyboard.is_pressed('space'):
            print(a,b)

if __name__ == '__main__':
    printStuff(*sys.argv[1:])
