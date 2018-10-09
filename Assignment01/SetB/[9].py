# Find the smallest number m from the Fibonacci sequence, defined by f[0]=f[1]=1, f[n]=f[n-1]+f[n-2], for n>2,
# larger than the given natural number n. So, find k and m such that f[k]=m, m>n and f[k-1] <=n.

n = int(input("Give n: "))
a = 0
b = 1
c = 1
k = 1
found = False
while not found:
    if c > n:
        found = True
    else:
        a = b
        b = c
        c = a + b
        k += 1
print("f[" + str(k) + "] = " + str(c))