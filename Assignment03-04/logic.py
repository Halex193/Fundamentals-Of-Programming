# Assignment 03-04
# Udrea Horațiu 917

from data import *


def initialize_data():
    """
    Initializes the data instance and the changes stack
    :return: tuple - A tuple containing the apartment data instance wit the default valuesand the changes stack
    """
    apartment_expense_data = create_apartment_expense_data()
    populate_apartment_expense_data(apartment_expense_data)
    changes_stack = create_changes_stack()
    return apartment_expense_data, changes_stack


def create_changes_stack():
    """
    Creates an empty changes stack
    :return: The changes stack
    """
    return []


def push_changes_stack(changes_stack, operation_stack):
    """
    Pushes a changes_commit object to the changes_stack
    :param changes_stack: The changes stack
    :param operation_stack: The changes commit object
    """
    changes_stack.append(operation_stack)


def undo(apartment_expense_data, changes_stack, add, remove):
    """
    Undoes the last command that altered the application data
    :param apartment_expense_data: The application data instance
    :param changes_stack: The changes_stack instance
    :param add: The function that adds an apartment_expense_dict
    :param remove: The function that removes an apartment_expense_dict
    :return: True if the operation succeeded, False otherwise (the changes stack is empty)
    """
    if len(changes_stack) == 0:
        return False
    operation_stack = changes_stack.pop()

    while len(operation_stack) != 0:
        operation = operation_stack.pop()
        reverse_operation(apartment_expense_data, operation, add, remove)


def reverse_operation(apartment_expense_data, operation, add, remove):
    """
    Reverses the given operation
    :param apartment_expense_data: The apartment expense data
    :param operation: The operation tuple registered on the operation_stack
    :param add: The function that adds an apartment_expense_dict
    :param remove: The function that removes an apartment_expense_dict
    :return:
    """
    if operation[0] == 'add':
        remove(apartment_expense_data, operation[1])
    elif operation[0] == 'remove':
        add(apartment_expense_data, operation[1])


def create_operation_stack():
    """
    Creates an operation_stack object
    :return: The new operation_stack
    """
    return []


def operation_stack_add_expense(operation_stack, apartment_expense_dict):
    """
    Registers the addition of the apartment_expense_dict to the operation_stack
    :param operation_stack: The operation stack that registers the addition
    :param apartment_expense_dict: The apartment_expense_dict that has been added
    """
    operation_stack.append(('add', apartment_expense_dict))


def operation_stack_remove_expense(operation_stack, apartment_expense_dict):
    """
    Registers the removal of the apartment_expense_dict to the operation_stack
    :param operation_stack: The operation stack that registers the removal
    :param apartment_expense_dict: The apartment_expense_dict that has been removed
    """
    operation_stack.append(('remove', apartment_expense_dict))


def command_add(apartment_expense_data, arguments):
    """
    Adds an apartment expense
    :param apartment_expense_data: The data instance
    :param arguments: list of strings - The arguments of the command
    :return: True if the apartment expense was added, False otherwise (apartment expense already exists)
    """
    if len(arguments) != 3:
        raise_argument_error()

    apartment = parse_apartment(arguments[0])
    type = parse_type(arguments[1])
    amount = parse_amount(arguments[2])

    return add_apartment_expense(apartment_expense_data, apartment, type, amount)


def command_remove(apartment_expense_data, arguments):
    """
    Removes apartment expenses
    :param apartment_expense_data: The data instance
    :param arguments: list of strings - The arguments of the command
    :return: int - number of expenses removed
    """
    if len(arguments) not in range(1, 4 + 1):
        raise_argument_error()
    if valid_integer(arguments[0]):
        apartment = parse_apartment(arguments[0])
        if len(arguments) == 1:
            return remove_apartment_expenses(apartment_expense_data, apartment)
        elif len(arguments) == 3 and arguments[1] == "to":
            apartment_start = apartment
            apartment_end = parse_apartment(arguments[2])

            return remove_apartment_expenses_from_range(apartment_expense_data, apartment_start,
                                                        apartment_end)
        else:
            raise_argument_error()
    elif len(arguments) == 1:
        type = parse_type(arguments[0])
        return remove_apartment_expenses_from_type(apartment_expense_data, type)
    else:
        raise_argument_error()


def command_replace(apartment_expense_data, arguments):
    """
    Replaces an apartment expense amount with a given one
    :param apartment_expense_data: The data instance
    :param arguments: list of strings - The arguments of the command
    :return: True if the value is replace, False otherwise (the expense does not exist
    """
    if len(arguments) != 4:
        raise_argument_error()
    if arguments[2] != "with":
        raise_argument_error()
    apartment = parse_apartment(arguments[0])
    type = parse_type(arguments[1])

    amount = parse_amount(arguments[3])
    if apartment in get_apartments(apartment_expense_data) and \
            type in get_types_for_apartment(apartment_expense_data, apartment):
        set_apartment_expense(apartment_expense_data, apartment, type, amount)
        return True
    return False


def command_list(apartment_expense_data, arguments, generate_expense_list, generate_apartment_list):
    """
    Gets a list from the data instance
    :param apartment_expense_data: The data instance
    :param arguments: list of strings - The arguments of the command
    :param generate_expense_list: The function that generates the output desired from the given expense list
    :param generate_apartment_list: The function that generates the output desired from the given apartment list
    :return: The generated output
    """
    if len(arguments) > 2:
        raise_argument_error()
    if len(arguments) == 0:
        return generate_expense_list(list_all_expenses(apartment_expense_data))
    elif len(arguments) == 1:
        apartment = parse_apartment(arguments[0])
        return generate_expense_list(list_expenses_for_apartment(apartment_expense_data, apartment))
    elif len(arguments) == 2:
        relation = parse_relation(arguments[0])
        amount = parse_int(arguments[1])
        return generate_apartment_list(list_expenses_for_amount(apartment_expense_data, relation, amount))


def populate_apartment_expense_data(apartment_expense_data):
    """
    Populates the list with sample data
    :param apartment_expense_data: The data instance
    """
    add_apartment_expense(apartment_expense_data, 1, 'water', 100)
    add_apartment_expense(apartment_expense_data, 1, 'gas', 100)
    add_apartment_expense(apartment_expense_data, 2, 'heating', 200)
    add_apartment_expense(apartment_expense_data, 2, 'other', 100)
    add_apartment_expense(apartment_expense_data, 3, 'electricity', 300)
    add_apartment_expense(apartment_expense_data, 4, 'gas', 400)
    add_apartment_expense(apartment_expense_data, 4, 'water', 200)
    add_apartment_expense(apartment_expense_data, 5, 'other', 500)
    add_apartment_expense(apartment_expense_data, 6, 'heating', 450)
    add_apartment_expense(apartment_expense_data, 6, 'water', 100)
