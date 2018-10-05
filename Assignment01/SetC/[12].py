# The numbers n1 and n2 have the property P if their writings in basis 10 have the same digits (e.g. 2113 and
# 323121). Determine whether two given natural numbers have the property P.

n1 = int(input("Give number 1: "))
n2 = int(input("Give number 2: "))
digits = [0] * 10
P = True

while n1 != 0:
    digits[n1 % 10] = 1
    n1 //= 10

while n2 != 0:
    if digits[n2 % 10] == 0:
        P = False
        break
    digits[n2 % 10] = 2
    n2 //= 10
if not P:
    print("The numbers do not have property P")
for i in range(10):
    if digits[i] == 1:
        P = False
if not P:
    print("The numbers do not have property P")
else:
    print("The numbers have property P")
