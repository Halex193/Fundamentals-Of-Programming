# Determine the twin prime numbers p1 and p2 immediately larger than the given non-null natural number n. Two prime
# numbers p and q are called twin if q-p = 2.


def is_prime(x):
    prime = True
    for i in range(2, x // 2):
        if x % i == 0:
            prime = False
    return prime


n = int(input("Give n: "))
found = False
p = 1
q = n
while not found:
    if q % 2 == 0:
        q += 1
    else:
        q += 2
    if is_prime(q):
        if q - p == 2:
            found = True
        else:
            p = q

print(str(p) + " and " + str(q))
