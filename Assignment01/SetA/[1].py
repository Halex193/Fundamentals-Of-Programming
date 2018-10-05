# Generate the first prime number larger than a given natural number n
n = int(input("Give n: "))
n = n + 1
prime = False
while not prime:
    prime = True
    for i in range(2, n // 2):
        if n % i == 0:
            prime = False
            n = n + 1
print(n)
