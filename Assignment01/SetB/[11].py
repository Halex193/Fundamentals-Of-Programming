# The palindrome of a number is the number obtained by reversing the order of digits. E.g. palindrome (237) = (732).
# For a given natural number n, determine its palindrome.

n = int(input("Give the number: "))
result = 0
while n != 0:
    result = result * 10 + n % 10
    n //= 10
print(result)
