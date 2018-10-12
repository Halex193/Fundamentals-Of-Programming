# For a given natural number n find the largest natural number written with the same digits. E.g. n=3658, m=8653.

n = int(input("Give n: "))
fq = [0] * 10
while n != 0:
    fq[n % 10] += 1
    n //= 10

result = ""

for k in range(9, -1,-1):
    result += str(k) * fq[k]
a = int(result)
print(a)
