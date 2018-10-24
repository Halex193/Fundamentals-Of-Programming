# Assignment 03-04
# Udrea Horațiu 917

from data import *


def initialize_data():
    apartment_expense_data = create_apartment_expense_data()
    populate_apartment_expense_data(apartment_expense_data)
    changes_stack = create_changes_stack()
    return (apartment_expense_data, changes_stack)


def command_add(apartment_expense_data, arguments):
    if len(arguments) != 3:
        raise ValueError('arguments')

    if not valid_apartment(arguments[0]):
        raise ValueError('apartment')
    apartment = int(arguments[0])

    if not valid_type(arguments[1]):
        raise ValueError('type')
    type = arguments[1]

    if not valid_amount(arguments[2]):
        raise ValueError('amount')
    amount = int(arguments[2])

    return add_apartment_expense(apartment_expense_data, apartment, type, amount)


def command_remove(apartment_expense_data, arguments):
    if len(arguments) not in range(1, 4 + 1):
        raise ValueError('arguments')
    if valid_integer(arguments[0]):
        if not valid_apartment(arguments[0]):
            raise ValueError('apartment')
        if len(arguments) == 1:
            return remove_apartment_expenses_from_apartment_number(apartment_expense_data, int(arguments[0]))
        elif len(arguments) == 3 and arguments[1] == "to":
            if not valid_apartment(arguments[2]):
                raise ValueError('apartment')

            apartment_start = int(arguments[0])
            apartment_end = int(arguments[2])
            if apartment_start >= apartment_end:
                raise ValueError('increasing')
            return remove_apartment_expenses_from_apartment_range(apartment_expense_data, apartment_start,
                                                                  apartment_end)
        else:
            raise ValueError("arguments")
    elif len(arguments) == 1:
        if not valid_type(arguments[0]):
            raise ValueError('type')
        return remove_apartment_expenses_from_type(apartment_expense_data, arguments[0])
    else:
        raise ValueError('arguments')


def command_replace(apartment_expense_data, arguments):
    if len(arguments) != 4:
        raise ValueError('arguments')
    if not valid_apartment(arguments[0]):
        raise ValueError('apartment')
    apartment = int(arguments[0])
    if not valid_type(arguments[1]):
        raise ValueError('type')
    type = arguments[1]
    if arguments[2] != "with":
        raise ValueError('arguments')
    if not valid_amount(arguments[3]):
        raise ValueError('amount')
    amount = int(arguments[3])
    if apartment in get_apartments(apartment_expense_data) and \
            type in get_types_for_apartment(apartment_expense_data, apartment):
        set_apartment_expense(apartment_expense_data, apartment, type, amount)
        return True
    return False


def command_list(apartment_expense_data, arguments):
    if len(arguments) > 2:
        raise ValueError('arguments')
    if len(arguments) == 0:
        return generate_list(list_all_expenses(apartment_expense_data))
    elif len(arguments) == 1:
        if not valid_apartment(arguments[0]):
            raise ValueError('apartment')
        apartment = int(arguments[0])
        return generate_list(list_expenses_for_apartment(apartment_expense_data, apartment))
    elif len(arguments) == 2:
        if not valid_relation(arguments[0]):
            raise ValueError('relation')
        relation = arguments[0]
        try:
            amount = int(arguments[1])
        except ValueError:
            raise ValueError("int")
        return list_expenses_for_amount(apartment_expense_data, relation, amount)


def generate_list(apartment_expenses):
    string_list = []
    for apartment_expense in apartment_expenses:
        string_list.append(apartment_expense_dict_to_string(apartment_expense) + "\n")
    return ''.join(string_list)


def list_all_expenses(apartment_expense_data):
    apartment_expenses = []
    for apartment in get_apartments(apartment_expense_data):
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            amount = apartment_expense_data[apartment][type]
            apartment_expenses.append(create_apartment_expense_dict(apartment, type, amount))
    return apartment_expenses


def list_expenses_for_apartment(apartment_expense_data, apartment):
    apartment_expenses = []
    if apartment in get_apartments(apartment_expense_data):
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            amount = apartment_expense_data[apartment][type]
            apartment_expenses.append(create_apartment_expense_dict(apartment, type, amount))
    return apartment_expenses


def list_expenses_for_amount(apartment_expense_data, relation, amount):
    apartments = []
    for apartment in get_apartments(apartment_expense_data):
        amount_sum = 0
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            amount_sum += get_apartment_expense(apartment_expense_data, apartment, type)
        if relation == "<" and amount_sum < amount:
            apartments.append(str(apartment))
            apartments.append(", ")
        elif relation == "=" and amount_sum == amount:
            apartments.append(str(apartment))
            apartments.append(", ")
        elif relation == ">" and amount_sum > amount:
            apartments.append(str(apartment))
            apartments.append(", ")
    return ''.join(apartments[:-1])
