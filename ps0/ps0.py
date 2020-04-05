#  Problem Set 0
import math

x = int(input("Enter a number: "))
y = int(input("Enter another number: "))

logx = round(math.log(x, 2), 2)

x_pow_y = x ** y
print()
print("{} raise to {} is equal to {}".format(x, y, x_pow_y))
print("Log of x is {}".format(logx))
