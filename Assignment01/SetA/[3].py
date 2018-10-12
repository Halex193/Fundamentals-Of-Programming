# For a given natural number n find the minimal natural number m formed with the same digits. E.g. n=3658, m=3568.

number = int(input("Give n: "))
digit_index = [0] * 10

while number != 0:
    digit_index[number % 10] += 1
    number //= 10

i = 1
found = False
while not found:
    if digit_index[i] != 0:
        found = True
    else:
        i += 1

result = ""
result += str(i) * digit_index[i]
result += str(0) * digit_index[0]

for k in range(i + 1, 10):
    result += str(k) * digit_index[k]
a = int(result)
print(a)
