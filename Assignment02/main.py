# Assignment 02
# Udrea Horațiu 917

# region Functional part
def run():
    number_dictionary = get_default_numbers()
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
            options.get(choice)(number_dictionary)


def slice_dictionary(number_dictionary, start_index, end_index):
    '''
    Slices a dictionary
    :param number_dictionary: THe dictionary to be sliced
    :param start_index: The minimi=um key value
    :param end_index: The maximum key value (exclusive)
    :return: The sliced dictionary
    '''
    return {index - start_index: number_dictionary[index] for index in range(start_index, end_index) if
            index in number_dictionary}


def get_default_numbers():
    '''
    Creates a dictionary with the default number set
    '''
    return {0: (1, 0),
            1: (5, 5),
            2: (4, 5),
            3: (9, 7),
            4: (1, 4),
            5: (2, 6),
            6: (3, 5),
            7: (4, 9),
            8: (1, 8),
            9: (2, 2)}


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


def number_dictionary_add(number_dictionary, complex_tuple):
    number_dictionary[len(number_dictionary)] = complex_tuple


def find_sequence_10(number_dictionary):
    '''
    The method finds the longest sequence of complex numbers with the sum 10 + 10i from the given dictionary
    :param number_dictionary: The complex number tuple dictionary in which to search for the sequence
    :return: A dictionary containing tuples, representing the longest sequence of complex numbers with the sum 10 + 10i.
    An empty dictionary is returned if no sequence is found.
    :postconditions: The initial number dictionary will remain unmodified.
    '''

    start_index = 0
    length = len(number_dictionary)
    max_start_index = 0
    max_length = 0

    found = False
    while not found:
        complex_sum = sum(slice_dictionary(number_dictionary, start_index, start_index + length))
        if get_real_part(complex_sum) == 10 and get_imaginary_part(complex_sum) == 10:
            if length > max_length:
                max_length = length
                max_start_index = start_index

        if start_index + length == len(number_dictionary):
            length -= 1
            start_index = 0
            if length <= 0:
                found = True
        else:
            start_index += 1
    return slice_dictionary(number_dictionary, max_start_index, max_start_index + max_length)


def sum(number_dictionary):
    '''
    Calculates the sum of the complex numbers in the given dictionary.
    :param number_dictionary: The dictionary of numbers to be added together
    :return: The sum of the complex numbers in the form of a complex tuple
    '''

    real_sum = 0
    imaginary_sum = 0
    for complex_tuple in number_dictionary.values():
        real_sum += get_real_part(complex_tuple)
        imaginary_sum += get_imaginary_part(complex_tuple)
    return (real_sum, imaginary_sum)


def find_sequence_11(number_dictionary):
    '''
    The method finds the longest sequence of complex numbers with the mountain layout from the given dictionary.
    A sequence of complex numbers has a mountain layout when the real parts of the numbers first increase, then decrease.
    (e.g. 1-i, 2+6i, 4-67i, 90+3i, 80-7i, 76+i, 43-12i, 3)
    :param number_dictionary: The complex number tuple dictionary in which to search for the sequence
    :return: A dictionary containing tuples, representing the longest sequence of complex numbers having the mountain layout.
    An empty dictionary is returned if no sequence is found.
    :postconditions: The initial number dictionary will remain unmodified.
    '''

    stage = 2  # 1 -> ascending, 2 -> descending
    max_start_index = -1
    max_length = 0
    start_index = 0
    length = 0

    for i in range(len(number_dictionary) - 1):
        if get_real_part(number_dictionary[i + 1]) >= get_real_part(number_dictionary[i]):
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
        if get_real_part(number_dictionary[i + 1]) < get_real_part(number_dictionary[i]):
            length += 1
            if stage == 1:
                stage = 2

    if stage == 2:
        if length > max_length:
            max_start_index = start_index
            max_length = length

    return slice_dictionary(number_dictionary, max_start_index, max_start_index + max_length)


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


def ui_read_number(number_dictionary):
    print("Inserting new number in dictionary")
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
    number_dictionary_add(number_dictionary, complex_number)


def ui_display_numbers(number_dictionary):
    number_strings_list = []
    for i in range(len(number_dictionary)):
        complex_tuple = number_dictionary[i]
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
        number_strings_list.append(
            str(real_part) + imaginary_string + (", " if i != len(number_dictionary) - 1 else ""))
    print(''.join(number_strings_list))


def ui_display_all_numbers(number_dictionary):
    print("Displaying all numbers in the dictionary:")
    ui_display_numbers(number_dictionary)


def ui_display_sequence_10(number_dictionary):
    sequence_10 = find_sequence_10(number_dictionary)
    if len(sequence_10) == 0:
        print("Sequence not found")
    else:
        print("The longest sequence with the sum of its elements 10 + 10i:")
        ui_display_numbers(sequence_10)


def ui_display_sequence_11(number_dictionary):
    sequence_11 = find_sequence_11(number_dictionary)
    if len(sequence_11) == 0:
        print("No mountain sequence found")
    else:
        print("The largest mountain sequence is:")
        ui_display_numbers(sequence_11)


# endregion

# region Test Part
def run_tests():
    test_number_dictionary_add()
    # test_find_sequence_10()
    # test_find_sequence_11()


def test_number_dictionary_add():
    number_dictionary = []
    number_dictionary_add(number_dictionary, (0, 1))
    assert number_dictionary == {0: (0, 1)}

    number_dictionary_add(number_dictionary, (12.654, 123.876))
    assert number_dictionary == {0: (0, 1), 1: (12.654, 123.876)}

    number_dictionary_add(number_dictionary, (-543, 11.876))
    assert number_dictionary == {0: (0, 1), 1: (12.654, 123.876), 2: (-543, 11.876)}


def test_find_sequence_10():
    number_dictionary = []
    assert find_sequence_10(number_dictionary) == {}
    assert number_dictionary == []

    number_dictionary = [(10, 10)]
    assert find_sequence_10(number_dictionary) == [(10, 10)]
    assert number_dictionary == [(10, 10)]

    number_dictionary = [(4, 6), (6, 4)]
    assert find_sequence_10(number_dictionary) == [(4, 6), (6, 4)]
    assert number_dictionary == [(4, 6), (6, 4)]

    number_dictionary = [(4, 6), (6, 4), (0, 7), (10, 2), (0, 1)]
    assert find_sequence_10(number_dictionary) == [(0, 7), (10, 2), (0, 1)]
    assert number_dictionary == [(4, 6), (6, 4), (0, 7), (10, 2), (0, 1)]


def test_find_sequence_11():
    number_dictionary = []
    assert find_sequence_11(number_dictionary) == []
    assert number_dictionary == []

    number_dictionary = {0:(10, 10)}
    assert find_sequence_11(number_dictionary) == []
    assert number_dictionary == {0:(10, 10)}

    number_dictionary = {0:(3, 6), 1: (6, 6)}
    assert find_sequence_11(number_dictionary) == []
    assert number_dictionary == {0:(3, 6), 1: (6, 6)}

    number_dictionary = {0:(4, 6), 1: (6, 4), 2: (0, 7), 3: (10, 2)}
    assert find_sequence_11(number_dictionary) == {0:(4, 6), 1: (6, 4), 2: (0, 7)}
    assert number_dictionary == {0:(4, 6), 1: (6, 4), 2: (0, 7), 3: (10, 2)}

    number_dictionary = {0:(4, 6), 1: (6, 4), 2:(0, 7), 3:(10, 2), 4:(5, 8)}
    assert find_sequence_11(number_dictionary) == {0:(4, 6), 1: (6, 4), 2:(0, 7)}
    assert number_dictionary == {0:(4, 6), 1: (6, 4), 2:(0, 7), 3:(10, 2), 4:(5, 8)}

    number_dictionary = {0:(4, 6), 1: (6, 4), 2: (0, 7), 3: (10, 2), 4: (11, 8), 5: (12, 54), 6: (13, 87.987)}
    assert find_sequence_11(number_dictionary) == {0:(4, 6), 1: (6, 4), 2: (0, 7)}
    assert number_dictionary == {0:(4, 6), 1: (6, 4), 2: (0, 7), 3: (10, 2), 4: (11, 8), 5: (12, 54), 6: (13, 87.987)}

    number_dictionary = {0:(4, 6), 1: (6, 4), 2: (0, 7), 3: (10, 2), 4: (11, 8), 5: (12, 54), 6: (13, 87.987), 7: (2.5, 87)}
    assert find_sequence_11(number_dictionary) == {0: (0, 7), 1: (10, 2), 2: (11, 8), 3: (12, 54), 4: (13, 87.987), 5: (2.5, 87)}
    assert number_dictionary == {0:(4, 6), 1: (6, 4), 2: (0, 7), 3: (10, 2), 4: (11, 8), 5: (12, 54), 6: (13, 87.987), 7: (2.5, 87)}

    number_dictionary = {0:(4, 6), 1: (6, 4), 2: (0, 7), 3: (10, 2), 4: (11, 8), 5: (12, 54), 6: (13, 87.987), 7: (2.5, 87), 8: (3.8, 9)}
    assert find_sequence_11(number_dictionary) == {1: (0, 7), 2: (10, 2), 3: (11, 8), 4: (12, 54), 5: (13, 87.987), 6: (2.5, 87), 7: (3.8, 9)}
    assert number_dictionary == {0:(4, 6), 1: (6, 4), 2: (0, 7), 3: (10, 2), 4: (11, 8), 5: (12, 54), 6: (13, 87.987), 7: (2.5, 87), 8: (3.8, 9)}


# endregion

# run_tests()
run()
