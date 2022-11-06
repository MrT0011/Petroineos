# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 01:08:50 2022

@author: Jeffrey
"""

instructions = ['BEGIN', 'LEFT 3', 'UP 5', 'RIGHT 4', 'DOWN 7', 'STOP']

def function (instruction):
    x = 0
    y = 0
    for i in instruction:
        if 'LEFT' in i:
            x -= int(i[-1])
        elif 'RIGHT' in i:
            x += int(i[-1])
        elif 'UP' in i:
            y += int(i[-1])
        elif 'DOWN' in i:
            y -= int(i[-1])
        elif i == 'STOP':
            distance = (x ** 2 + y ** 2)  ** (1/2)
            print('The distance of Robot from the original position (0,0): ', round(distance,2))
            break
    
    
if __name__ == '__main__':
    function(instructions)
    
