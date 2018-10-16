# Assignment 02
# Udrea Horațiu 917

# region Functional part
def run():
    number_list = get_default_numbers()
    while True:
        choice = ui_show_menu()
        options = {
            1: ui_read_number,
            2: ui_display_all_numbers,
            3: ui_display_sequence_10,
            4: ui_display_sequence_11
            # 0: exit
        }
        if choice == 0:
            ui_exit()
            break
        else:
            options.get(choice)(number_list)


def get_default_numbers():
    '''
    Creates a list with the default number set
    '''
    return [(1, 0), (5, 5), (4, 5), (9, 7), (1, 4), (2, 6), (3, 5), (4, 9), (1, 8), (2, 2)]


def get_real_part(complex_tuple):
    '''
    Returns the real part of a complex tuple
    '''

    return complex_tuple[0]


def get_imaginary_part(complex_tuple):
    '''
        Returns the imaginary part of a complex tuple
        '''

    return complex_tuple[1]


def number_list_add(number_list, complex_tuple):
    number_list.append(complex_tuple)


def find_sequence_10(number_list):
    '''
    The method finds the longest sequence of complex numbers with the sum 10 + 10i from the given list
    :param number_list: The complex number tuple list in which to search for the sequence
    :return: A list containing tuples, representing the longest sequence of complex numbers with the sum 10 + 10i.
    An empty list is returned if no sequence is found.
    :postconditions: The initial number list will remain unmodified.
    '''

    start_index = 0
    length = len(number_list)
    max_start_index = 0
    max_length = 0

    found = False
    while not found:
        complex_sum = sum(number_list[start_index:start_index + length])
        if get_real_part(complex_sum) == 10 and get_imaginary_part(complex_sum) == 10:
            if length > max_length:
                max_length = length
                max_start_index = start_index

        if start_index + length == len(number_list):
            length -= 1
            start_index = 0
            if length <= 0:
                found = True
        else:
            start_index += 1
    return number_list[max_start_index : max_start_index + max_length]


def sum(number_list):
    '''
    Calculates the sum of the complex numbers in the given list.
    :param number_list: The list of numbers to be added together
    :return: The sum of the complex numbers in the form of a complex tuple
    '''

    real_sum = 0
    imaginary_sum = 0
    for complex_tuple in number_list:
        real_sum += get_real_part(complex_tuple)
        imaginary_sum += get_imaginary_part(complex_tuple)
    return (real_sum, imaginary_sum)


def find_sequence_11(number_list):
    '''
    The method finds the longest sequence of complex numbers with the mountain layout from the given list.
    A sequence of complex numbers has a mountain layout when the real parts of the numbers first increase, then decrease.
    (e.g. 1-i, 2+6i, 4-67i, 90+3i, 80-7i, 76+i, 43-12i, 3)
    :param number_list: The complex number tuple list in which to search for the sequence
    :return: A list containing tuples, representing the longest sequence of complex numbers having the mountain layout.
    An empty list is returned if no sequence is found.
    :postconditions: The initial number list will remain unmodified.
    '''

    stage = 2  # 1 -> ascending, 2 -> descending
    max_start_index = -1
    max_length = 0
    start_index = 0
    length = 0

    for i in range(len(number_list) - 1):
        if get_real_part(number_list[i + 1]) >= get_real_part(number_list[i]):
            if stage == 1:
                length += 1
            if stage == 2:  # new possible mountain
                # compare with last one
                if length > max_length:
                    max_start_index = start_index
                    max_length = length
                # reinitiate search
                stage = 1
                start_index = i
                length = 2
        if get_real_part(number_list[i + 1]) < get_real_part(number_list[i]):
            length += 1
            if stage == 1:
                stage = 2

    if stage == 2:
        if length > max_length:
            max_start_index = start_index
            max_length = length

    return number_list[max_start_index : max_start_index + max_length]


# endregion

# region UI Part
def ui_show_menu():
    print()
    print("1. Read a complex number")
    print("2. Display all complex numbers")
    print("3. Display the longest sequence with the sum of its elements 10 + 10i")
    print("4. Display the largest mountain sequence")
    print("0. Exit")

    while True:
        try:
            choice = int(input("Please input your choice number: "))
            if choice not in range(0, 4 + 1):
                print("The number is not a valid choice number")
            else:
                return choice
        except ValueError:
            print("Value is not a number")


def ui_exit():
    print("Goodbye! :)")


def ui_read_number(number_list):
    print("Inserting new number in list")
    value_found = False
    while not value_found:
        try:
            real_part = float(input("Input the real part of the new number:"))
            value_found = True
        except ValueError:
            print("Please input a valid number")
    value_found = False
    while not value_found:
        try:
            imaginary_part = float(input("Input the imaginary part of the new number:"))
            value_found = True
        except ValueError:
            print("Please input a valid number")
    complex_number = (real_part, imaginary_part)
    number_list_add(number_list, complex_number)


def ui_display_numbers(number_list):
    number_strings_list = []
    for i in range(len(number_list)):
        complex_tuple = number_list[i]
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
        number_strings_list.append(str(real_part) + imaginary_string + (", " if i != len(number_list) - 1 else ""))
    print(''.join(number_strings_list))


def ui_display_all_numbers(number_list):
    print("Displaying all numbers in the list:")
    ui_display_numbers(number_list)


def ui_display_sequence_10(number_list):
    sequence_10 = find_sequence_10(number_list)
    if len(sequence_10) == 0:
        print("Sequence not found")
    else:
        print("The longest sequence with the sum of its elements 10 + 10i:")
        ui_display_numbers(sequence_10)


def ui_display_sequence_11(number_list):
    sequence_11 = find_sequence_11(number_list)
    if len(sequence_11) == 0:
        print("No mountain sequence found")
    else:
        print("The largest mountain sequence is:")
        ui_display_numbers(sequence_11)


# endregion

# region Test Part
def run_tests():
    test_number_list_add()
    test_find_sequence_10()
    test_find_sequence_11()


def test_number_list_add():
    number_list = []
    number_list_add(number_list, (0, 1))
    assert number_list == [(0, 1)]

    number_list_add(number_list, (12.654, 123.876))
    assert number_list == [(0, 1), (12.654, 123.876)]

    number_list_add(number_list, (-543, 11.876))
    assert number_list == [(0, 1), (12.654, 123.876), (-543, 11.876)]


def test_find_sequence_10():
    number_list = []
    assert find_sequence_10(number_list) == []
    assert number_list == []

    number_list = [(10, 10)]
    assert find_sequence_10(number_list) == [(10, 10)]
    assert number_list == [(10, 10)]

    number_list = [(4, 6), (6, 4)]
    assert find_sequence_10(number_list) == [(4, 6), (6, 4)]
    assert number_list == [(4, 6), (6, 4)]

    number_list = [(4, 6), (6, 4), (0, 7), (10, 2), (0, 1)]
    assert find_sequence_10(number_list) == [(0, 7), (10, 2), (0, 1)]
    assert number_list == [(4, 6), (6, 4), (0, 7), (10, 2), (0, 1)]


def test_find_sequence_11():
    number_list = []
    assert find_sequence_11(number_list) == []
    assert number_list == []

    number_list = [(10, 10)]
    assert find_sequence_11(number_list) == []
    assert number_list == [(10, 10)]

    number_list = [(3, 6), (6, 6)]
    assert find_sequence_11(number_list) == []
    assert number_list == [(3, 6), (6, 6)]

    number_list = [(4, 6), (6, 4), (0, 7), (10, 2)]
    assert find_sequence_11(number_list) == [(4, 6), (6, 4), (0, 7)]
    assert number_list == [(4, 6), (6, 4), (0, 7), (10, 2)]

    number_list = [(4, 6), (6, 4), (0, 7), (10, 2), (5, 8)]
    assert find_sequence_11(number_list) == [(4, 6), (6, 4), (0, 7)]
    assert number_list == [(4, 6), (6, 4), (0, 7), (10, 2), (5, 8)]

    number_list = [(4, 6), (6, 4), (0, 7), (10, 2), (11, 8), (12, 54), (13, 87.987)]
    assert find_sequence_11(number_list) == [(4, 6), (6, 4), (0, 7)]
    assert number_list == [(4, 6), (6, 4), (0, 7), (10, 2), (11, 8), (12, 54), (13, 87.987)]

    number_list = [(4, 6), (6, 4), (0, 7), (10, 2), (11, 8), (12, 54), (13, 87.987), (2.5, 87)]
    assert find_sequence_11(number_list) == [(0, 7), (10, 2), (11, 8), (12, 54), (13, 87.987), (2.5, 87)]
    assert number_list == [(4, 6), (6, 4), (0, 7), (10, 2), (11, 8), (12, 54), (13, 87.987), (2.5, 87)]

    number_list = [(4, 6), (6, 4), (0, 7), (10, 2), (11, 8), (12, 54), (13, 87.987), (2.5, 87), (3.8, 9)]
    assert find_sequence_11(number_list) == [(0, 7), (10, 2), (11, 8), (12, 54), (13, 87.987), (2.5, 87)]
    assert number_list == [(4, 6), (6, 4), (0, 7), (10, 2), (11, 8), (12, 54), (13, 87.987), (2.5, 87), (3.8, 9)]


# endregion

run_tests()
run()
