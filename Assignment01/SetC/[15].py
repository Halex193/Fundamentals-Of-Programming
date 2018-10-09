# Generate the smallest perfect number larger than a given natural number n. If such a number does not exist,
# a message should be displayed. A number is perfect if it is equal to the sum of its divisors, except itself. E.g. 6
#  is a perfect number (6=1+2+3).


def is_prime(x):
    prime = True
    for i in range(2, x // 2):
        if x % i == 0:
            prime = False
    return prime


n = int(input("Give n: "))
found = False
num = 4
while not found:
    if is_prime(num - 1):
        perfect = num / 2 * (num - 1)
        if perfect > n:
            found = True
    num *= 2

print(int(perfect))
