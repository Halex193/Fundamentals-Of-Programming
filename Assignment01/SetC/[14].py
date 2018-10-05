# Determine the n-th element of the sequence 1,2,3,2,2,5,2,2,3,3,3,7,2,2,3,3,3,...
# obtained from the sequence of natural numbers by replacing composed numbers with their prime divisors,
# each divisor d being written d times, without memorizing the elements of the sequence.

n = int(input("Give n: "))
t = i = 1
d = 1
out = -1

while n > 0:
    d += 1
    divisor = False
    while t % d == 0:
        t //= d
        divisor = True

    if divisor and i != 2:
        n -= d
        out = d
        if t == 1:
            i += 1
            t = i
            d = 1
    elif d >= i // 2:
        n -= 1
        out = i
        i += 1
        t = i
        d = 1

print(out)
