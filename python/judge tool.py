import math
import os
import random
import re
import sys

def judge_input(number):
    if number%2==1:
        print("Weird")
    elif number>=2 and number<5:
        print("NOT Weird")
    elif number>=6 and number<20:
        print("weird")
    else:
        print("not Weird")
    
  
if __name__ == '__main__':

    n = int(input("Enter a number:"))
    judge_input(n)