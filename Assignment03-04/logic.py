# Assignment 03-04
# Udrea Horațiu 917
"""
This is the business logic module
"""
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


def command_undo(apartment_expense_data, arguments, changes_stack):
    """
    Undoes the last command that altered the application data
    :param arguments: list of strings - Command arguments
    :param apartment_expense_data: The application data instance
    :param changes_stack: The changes_stack instance
    :return: True if the operation succeeded, False otherwise (the changes stack is empty)
    """
    if len(arguments) != 0:
        raise_argument_error()
    if len(changes_stack) == 0:
        return False
    operation_stack = changes_stack.pop()

    while len(operation_stack) != 0:
        operation = operation_stack.pop()
        reverse_operation(apartment_expense_data, operation)
    return True


def reverse_operation(apartment_expense_data, operation):
    """
    Reverses the given operation
    :param apartment_expense_data: The apartment expense data
    :param operation: The operation tuple registered on the operation_stack
    :return:
    """
    apartment_expense_dict = operation[1]
    if operation[0] == 'add':
        remove_expense(apartment_expense_data, get_apartment(apartment_expense_dict), get_type(apartment_expense_dict))
    elif operation[0] == 'remove':
        add_apartment_expense(apartment_expense_data, get_apartment(apartment_expense_dict),
                              get_type(apartment_expense_dict), get_amount(apartment_expense_dict))


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


def command_add(apartment_expense_data, arguments, changes_stack):
    """
    Adds an apartment expense
    :param apartment_expense_data: The data instance
    :param arguments: list of strings - The arguments of the command
    :param changes_stack: The changes stack
    :return: True if the apartment expense was added, False otherwise (apartment expense already exists)
    """
    if len(arguments) != 3:
        raise_argument_error()

    apartment = parse_apartment(arguments[0])
    type = parse_type(arguments[1])
    amount = parse_amount(arguments[2])

    apartment_expense_dict = add_apartment_expense(apartment_expense_data, apartment, type, amount)
    if apartment_expense_dict is not None:
        operation_stack = create_operation_stack()
        operation_stack_add_expense(operation_stack, apartment_expense_dict)
        push_changes_stack(changes_stack, operation_stack)
        return True
    return False


def command_remove(apartment_expense_data, arguments, changes_stack):
    """
    Removes apartment expenses
    :param apartment_expense_data: The data instance
    :param arguments: list of strings - The arguments of the command
    :param changes_stack: The changes stack
    :return: int - number of expenses removed
    """
    if len(arguments) not in range(1, 4 + 1):
        raise_argument_error()
    if valid_integer(arguments[0]):
        apartment = parse_apartment(arguments[0])
        if len(arguments) == 1:
            return register_removals(changes_stack, remove_apartment_expenses(apartment_expense_data, apartment))
        elif len(arguments) == 3 and arguments[1] == "to":
            apartment_start = apartment
            apartment_end = parse_apartment(arguments[2])

            return register_removals(changes_stack,
                                     remove_apartment_expenses_from_range(apartment_expense_data, apartment_start,
                                                                          apartment_end))
        else:
            raise_argument_error()
    elif len(arguments) == 1:
        type = parse_type(arguments[0])
        return register_removals(changes_stack, remove_apartment_expenses_from_type(apartment_expense_data, type))
    else:
        raise_argument_error()


def register_removals(changes_stack, removal_list):
    operation_stack = create_operation_stack()
    for removal in removal_list:
        operation_stack_remove_expense(operation_stack, removal)
    push_changes_stack(changes_stack, operation_stack)
    return len(removal_list)


def command_replace(apartment_expense_data, arguments, changes_stack):
    """
    Replaces an apartment expense amount with a given one
    :param apartment_expense_data: The data instance
    :param arguments: list of strings - The arguments of the command
    :param changes_stack: The changes stack
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
        old_amount = get_apartment_expense(apartment_expense_data, apartment, type)
        set_apartment_expense(apartment_expense_data, apartment, type, amount)

        operation_stack = create_operation_stack()
        operation_stack_remove_expense(operation_stack, create_apartment_expense_dict(apartment, type, old_amount))
        operation_stack_add_expense(operation_stack, create_apartment_expense_dict(apartment, type, amount))
        push_changes_stack(changes_stack, operation_stack)
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


def list_expenses_for_amount(apartment_expense_data, relation, amount):
    """
    Gets the apartments that have the total expenses in the specified relation with the given amount
    :param apartment_expense_data: The data instance
    :param relation: The relation to compare the values
    :param amount: The amount with which to compare the total expenses of the apartments
    :return: list of int - The list of apartments which have the total
             expenses in the specified relation with the given amount
             sorted in ascending order
    """
    relation = parse_relation(relation)
    amount = parse_int(amount)

    apartments = []
    for apartment in get_apartments(apartment_expense_data):
        amount_sum = expense_sum(apartment_expense_data, apartment)
        if relation == "<" and amount_sum < amount:
            apartments.append(apartment)
        elif relation == "=" and amount_sum == amount:
            apartments.append(apartment)
        elif relation == ">" and amount_sum > amount:
            apartments.append(apartment)
    return sorted(apartments)


def expense_sum(apartment_expense_data, apartment):
    """
    Calculates the total expenses of an apartment
    :param apartment_expense_data: The data instance
    :param apartment: int - The apartment number
    :return: The sum of the expenses of the apartment
    """
    amount_sum = 0
    for type in get_types_for_apartment(apartment_expense_data, apartment):
        amount_sum += get_apartment_expense(apartment_expense_data, apartment, type)
    return amount_sum


def command_sum(apartment_expense_data, arguments):
    """
    Calculates the sum of expenses of the specified type
    :param apartment_expense_data: The data instance
    :param arguments: list of strings - The arguments of the command, the only one being the type of the expense
    :return: The sum of expenses of the given type
    """
    if len(arguments) != 1:
        raise_argument_error()
    type = parse_type(arguments[0])
    sum = 0
    for apartment in get_apartments(apartment_expense_data):
        amount = get_apartment_expense(apartment_expense_data, apartment, type)
        if amount is not None:
            sum += amount
    return sum


def command_max(apartment_expense_data, arguments):
    """
    Determines the maximum amount for each apartment expense type
    :param apartment_expense_data: The data instance
    :param arguments: The command arguments
    :return: dictionary - A dictionary having the expense types as keys and the
             (apartment number-maximum amount) tuples as values
    """
    if len(arguments) != 0:
        raise_argument_error()
    max = {}
    for apartment in get_apartments(apartment_expense_data):
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            amount = get_apartment_expense(apartment_expense_data, apartment, type)
            if type not in max.keys() or amount > max[type][1]:
                max[type] = (apartment, amount)
    return max


def command_sort(apartment_expense_data, arguments, generate_apartment_list, generate_type_list):
    """
    Sorts the apartment data
    :param apartment_expense_data:  The data instance
    :param arguments: The command arguments
    :param generate_apartment_list: A function that converts an apartment list to the desired output
    :param generate_type_list: A function that converts a list of type-amount tuples to the desired output
    :return:
    """
    if len(arguments) != 1:
        raise_argument_error()
    if arguments[0] == 'apartment':
        return generate_apartment_list(sort_apartments(apartment_expense_data))
    elif arguments[0] == 'type':
        return generate_type_list(sort_types(apartment_expense_data))
    else:
        raise_argument_error()


def sort_apartments(apartment_expense_data):
    """
    Sorts the apartments in ascending order by the sum of expenses
    :param apartment_expense_data: The data instance
    :return: list of ints - The list of apartments
    """
    expense_list = []
    for apartment in get_apartments(apartment_expense_data):
        amount_sum = expense_sum(apartment_expense_data, apartment)
        expense_list.append((apartment, amount_sum))
    expense_list = sorted(expense_list, key=lambda expense: expense[1])
    apartment_list = [pair[0] for pair in expense_list]
    return apartment_list


def sort_types(apartment_expense_data):
    """
    Sorts the types in ascending order by the sum of expenses
    :param apartment_expense_data: The data instance
    :return: The sorted list of type-amount tuples
    """
    expense_dict = {}
    for apartment in get_apartments(apartment_expense_data):
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            amount = get_apartment_expense(apartment_expense_data, apartment, type)
            if type in expense_dict.keys():
                expense_dict[type] += amount
            else:
                expense_dict[type] = amount
    for type in get_type_list():
        if type not in expense_dict.keys():
            expense_dict[type] = 0
    expense_list = [(k, v) for k, v in expense_dict.items()]
    expense_list = sorted(expense_list, key=lambda expense: expense[1])
    return expense_list


def command_filter(apartment_expense_data, arguments, changes_stack):
    """
    FIlters the data according to the given criteria
    :param apartment_expense_data: The data instance
    :param arguments: The command arguments
    :param changes_stack: The changes stack
    :return: int - The number of expenses removed
    :raises: ValueError if parsing fails or invalid arguments are given
    """
    if len(arguments) != 1:
        raise_argument_error()
    if valid_type(arguments[0]):
        type = parse_type(arguments[0])
        return register_removals(changes_stack, filter_type(apartment_expense_data, type))
    elif valid_amount(arguments[0]):
        amount = parse_amount(arguments[0])
        return register_removals(changes_stack, filter_amount(apartment_expense_data, amount))
    else:
        raise_argument_error()


def filter_type(apartment_expense_data, type):
    """
    Filters the data to preserve only expenses of the given type
    :param apartment_expense_data: The data instance
    :param type: string - The type to be preserved
    :return: list of apartment_expense_dict - The removed expenses
    """
    removed = []
    for expense_type in get_type_list():
        if expense_type != type:
            removed.extend(remove_apartment_expenses_from_type(apartment_expense_data, expense_type))
    return removed


def filter_amount(apartment_expense_data, amount):
    """
    Filters the data to preserve only expenses with the amount lower than the given value
    :param apartment_expense_data: The data instance
    :param amount: int - The amount threshold
    :return: list of apartment_expense_dict - The removed expenses
    """
    removed = []
    for apartment in get_apartments(apartment_expense_data):
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            expense_amount = get_apartment_expense(apartment_expense_data, apartment, type)
            if expense_amount >= amount:
                removed.extend(remove_expense(apartment_expense_data, apartment, type))
    return removed


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
