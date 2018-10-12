# 10. Sum of its elements is 10+10i
# 11. Real part is in the form of a mountain (first the values increase, then they decrease).
# (e.g. 1-i, 2+6i, 4-67i, 90+3i, 80-7i, 76+i, 43-12i, 3)
def show_menu():
    print("1. Read a complex number")
    print("2. Display all complex numbers")
    print("3. Display the longest sequence with the sum of its elements 10 + 10i")
    print("4. Display the lasrgest mountain sequence")
    print("0. Exit")

    return int(input("Your choice: "))


numbers = [(1, 0), (5, 5), (4, 5), (9, 7), (1, 4), (2, 6), (3, 5), (4, 9), (1, 8), (2, 2)]


def get_real_part(complex_tuple):
    return complex_tuple[0]


def get_imaginary_part(complex_tuple):
    return complex_tuple[1]


def read_number():
    a = float(input("Enter real part:"))
    b = float(input("Enter imaginary part: "))
    numbers.append((a, b))


def display_numbers(start_index, end_index):
    for complex_tuple in numbers[start_index:end_index]:
        real_part = get_real_part(complex_tuple)
        imaginary_part = get_imaginary_part(complex_tuple)

        if int(real_part) == real_part:
            real_part = int(real_part)

        if int(imaginary_part) == imaginary_part:
            imaginary_part = int(imaginary_part)

        if imaginary_part == 0:
            imaginary_string = ""
        elif imaginary_part < 0:
            imaginary_string = " - " + str(-imaginary_part) + "i"
        else:
            imaginary_string = " + " + str(imaginary_part) + "i"

        print(str(real_part) + imaginary_string)


# end_index is exclusive
def sum(start_index, end_index):
    real_sum = 0
    imaginary_sum = 0
    for index in range(start_index, end_index):
        real_sum += get_real_part(numbers[index])
        imaginary_sum += get_imaginary_part(numbers[index])
    return (real_sum, imaginary_sum)


def display_sequence_10():
    start_index = 0
    length = len(numbers)

    found = False
    while not found:
        complex_sum = sum(start_index, start_index + length)
        if get_real_part(complex_sum) == 10 and get_imaginary_part(complex_sum) == 10:
            found = True
        else:
            if start_index + length == len(numbers):
                length -= 1
                start_index = 0
                if length == 0:
                    found = True
            else:
                start_index += 1
    if length == 0:
        print("Sequence not found")
    else:
        display_numbers(start_index, start_index + length)


def display_sequence_11():
    stage = 2  # 1 -> ascending, 2 -> descending
    max_start = -1
    max_length = 0
    start = 0
    length = 0
    for i in range(len(numbers) - 1):
        if get_real_part(numbers[i + 1]) >= get_real_part(numbers[i]):
            if stage == 1:
                length += 1
            if stage == 2:  # new possible mountain
                # compare with last one
                if length > max_length:
                    max_start = start
                    max_length = length
                # reinitiate search
                stage = 1
                start = i
                length = 2
        if get_real_part(numbers[i + 1]) < get_real_part(numbers[i]):
            length += 1
            if stage == 1:
                stage = 2
    if stage == 2:
        if length > max_length:
            max_start = start
            max_length = length
    if max_length <= 0:
        print("No mountain sequences found")
    else:
        display_numbers(max_start, max_start + max_length)


display_menu = True
while display_menu:
    option = show_menu()
    if option == 1:
        read_number()
    elif option == 2:
        display_numbers(0, len(numbers))
    elif option == 3:
        display_sequence_10()
    elif option == 4:
        display_sequence_11()
    elif option == 0:
        display_menu = False

print("Goodbye! :)")
