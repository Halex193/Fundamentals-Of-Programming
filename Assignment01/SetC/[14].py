# Determine the n-th element of the sequence 1,2,3,2,2,5,2,2,3,3,3,7,2,2,3,3,3,...
# obtained from the sequence of natural numbers by replacing composed numbers with their prime divisors,
# each divisor d being written d times, without memorizing the elements of the sequence.

index = int(input("Give n: "))
number_remainder = current_number = 1
divisor = 1
result = -1

while index > 0:
    divisor += 1
    is_divisor = False
    while number_remainder % divisor == 0:
        number_remainder //= divisor
        is_divisor = True

    if is_divisor and current_number != 2:
        index -= divisor
        result = divisor
        if number_remainder == 1:
            current_number += 1
            number_remainder = current_number
            divisor = 1
    elif divisor >= current_number // 2:
        index -= 1
        result = current_number
        current_number += 1
        number_remainder = current_number
        divisor = 1

print(result)
