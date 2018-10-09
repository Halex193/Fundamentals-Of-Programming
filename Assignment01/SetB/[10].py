# Consider a given natural number n. Determine the product p of all the proper factors of n.

n = int(input("Give n: "))
p = 1
for i in range(2, n // 2):
    if n % i == 0:
        p *= n
print(p) if p != 1 else print("No proper factors found")
