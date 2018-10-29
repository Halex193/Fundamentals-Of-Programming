# Assignment 03-04
# Udrea Horațiu 917
"""
This is the menu UI module
"""
from logic import *


def ui_show_menu():
    option_list = ["1. Add",
                   "2. Remove",
                   "3. Replace",
                   "4. List",
                   "5. Sum",
                   "6. Max",
                   "7. Sort",
                   "8. Filter",
                   "9. Undo",
                   "10. Credits",
                   "x. Exit"
                   ]
    print()
    return ui_show_options(option_list)


def run():
    data = initialize_data()
    apartment_expense_data = data[0]
    changes_stack = data[1]

    while True:
        choice = ui_show_menu()
        if choice == "x":
            return
        execute_command(apartment_expense_data, choice, changes_stack)


def execute_command(apartment_expense_data, choice, changes_stack):
    commands = {'1': ui_add,
                '2': ui_remove,
                '3': ui_replace,
                '4': ui_list,
                '5': ui_sum,
                '6': ui_max,
                '7': ui_sort,
                '8': ui_filter,
                '9': ui_undo,
                '10': ui_credits
                }

    if choice in commands.keys():
        commands[choice](apartment_expense_data, changes_stack)
    else:
        print("Choice not valid")


def ui_add(apartment_expense_data, changes_stack):
    try:
        apartment = parse_apartment(input("Choose an apartment number: "))
        type = parse_type(input("Choose a type of expense: "))
        amount = parse_amount(input("Choose an amount for the expense: "))

        arguments = [apartment, type, amount]
        added = command_add(apartment_expense_data, arguments, changes_stack)
        if added:
            print("Expense added")
        else:
            print("Expense already exists. Use 'replace' command instead")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_remove(apartment_expense_data, changes_stack):
    option_list = ["1. Remove expenses for an apartment",
                   "2. Remove expenses for a range of apartments",
                   "3. Remove expenses for a type"
                   ]
    try:
        choice = ui_show_options(option_list)
        arguments = []
        if choice == '1':
            apartment = parse_apartment(input("Choose an apartment number: "))
            arguments = [apartment]
        elif choice == '2':
            start_apartment = parse_apartment(input("Choose the first apartment number: "))
            end_apartment = parse_apartment(input("Choose the last apartment number: "))
            arguments = [start_apartment, 'to', end_apartment]
        elif choice == '3':
            type = parse_type(input("Choose a type of expense to remove: "))
            arguments = [type]
        else:
            raise_choice_error()

        number = command_remove(apartment_expense_data, arguments, changes_stack)
        print(str(number) + " expense" + ("s" if number != 1 else "") + " removed")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_replace(apartment_expense_data, changes_stack):
    try:
        apartment = parse_apartment(input("Choose an apartment number: "))
        type = parse_type(input("Choose an expense type: "))
        amount = parse_amount(input("Choose the new amount for the expense: "))
        arguments = [apartment, type, 'with', amount]
        replaced = command_replace(apartment_expense_data, arguments, changes_stack)
        if replaced:
            print("Amount replaced")
        else:
            print("Expense does not exist. Use 'add' command instead")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_list(apartment_expense_data, changes_stack):
    option_list = ["1. List all expenses",
                   "2. List all expenses for an apartment",
                   "3. List all expenses in a specified relation with an amount"]
    choice = ui_show_options(option_list)
    arguments = []
    if choice == '1':
        arguments = []
    elif choice == '2':
        apartment = parse_apartment(input("Choose an apartment number: "))
        arguments = [apartment]
    elif choice == '3':
        relation = parse_relation(input("Choose a relation: "))
        amount = parse_amount(input("Choose an expense amount: "))
        arguments = [relation, amount]
    else:
        raise_choice_error()
    try:
        output = command_list(apartment_expense_data, arguments, generate_list, generate_apartment_list)
        if output == '':
            print("Nothing to show")
        else:
            print(output)
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def apartment_expense_dict_to_string(apartment_expense_dict):
    apartment = get_apartment(apartment_expense_dict)
    amount = get_amount(apartment_expense_dict)
    type = get_type(apartment_expense_dict)

    max_length = 0
    for i in get_type_list():
        if len(i) > max_length:
            max_length = len(i)

    return "{ Apartment " + str(apartment) + ", Expense type: " + type + (
            max_length - len(type)) * " " + ", Amount: " + str(amount) + " RON }"


def generate_list(apartment_expenses):
    """
    Converts a list of apartment_expense_dict to string
    """
    string_list = []
    for apartment_expense in apartment_expenses:
        string_list.append(apartment_expense_dict_to_string(apartment_expense) + "\n")
    return ''.join(string_list)


def generate_apartment_list(apartment_list):
    """
    Converts a list of apartments to string
    """
    string_list = []
    for apartment in apartment_list:
        string_list.append(str(apartment) + ", ")
    return ''.join(string_list)


def ui_sum(apartment_expense_data, changes_stack):
    try:
        type = parse_type(input("Choose an expense type: "))
        arguments = [type]
        sum = command_sum(apartment_expense_data, arguments)
        if sum != 0:
            print("The " + arguments[0] + " expense sum is " + str(sum) + " RON")
        else:
            print("There are no " + arguments[0] + " expenses")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_max(apartment_expense_data, changes_stack):
    try:
        arguments = []
        max = command_max(apartment_expense_data, arguments)
        print_max(max)
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def print_max(max):
    """
    Converts the command_max output to string
    """
    if len(max) == 0:
        print("There are no registered expenses")
    else:
        for type in max.keys():
            print("Apartment " + str(max[type][0]) + " has the maximum expense for '" + type + "', which is " + str(
                max[type][1]))


def ui_sort(apartment_expense_data, changes_stack):
    option_list = ["1. Sort by apartment",
                   "2. Sort by type"
                   ]
    try:
        choice = ui_show_options(option_list)
        arguments = []
        if choice == '1':
            arguments = ['apartment']
        elif choice == '2':
            arguments = ['type']
        else:
            raise_choice_error()
        output = command_sort(apartment_expense_data, arguments, generate_apartment_list, generate_type_list)
        if output == '':
            print("Nothing to show")
        else:
            print(output)
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def generate_type_list(expense_list):
    """
    Converts a type-amount tuple list to string
    """
    type_list = []
    for pair in expense_list:
        type_list.append("The total '" + pair[0] + "' expenses are " + str(pair[1]) + " RON\n")
    return ''.join(type_list)


def ui_filter(apartment_expense_data, changes_stack):
    option_list = ["1. Filter by type",
                   "2. Filter by value"
                   ]
    try:
        choice = ui_show_options(option_list)
        arguments = []
        if choice == '1':
            type = parse_type(input("Choose an expense type: "))
            arguments = [type]
        elif choice == '2':
            amount = parse_amount(input("Choose an amount: "))
            arguments = [amount]
        else:
            raise_choice_error()
        removed = command_filter(apartment_expense_data, arguments, changes_stack)
        if removed == 0:
            print("Nothing to remove")
        else:
            print(str(removed) + " expenses removed")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_undo(apartment_expense_data, changes_stack):
    arguments = []
    try:
        undone = command_undo(apartment_expense_data, arguments, changes_stack)
        if undone:
            print("Command undone")
        else:
            print("No more commands to undo")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_credits(apartment_expense_data=None, changes_stack=None):
    print('''
    Udrea Horațiu 917 2018

        &@@@@@@@@@            @              
          @@@@@@  @         @@@              
            @@  @@@       @@@@@              
              %@@@@     @@@@@@@              
             @@@@@@      ,@@@@@              
             @@@@@@      ,@@@@@              
             @@@@@@      ,@@@@@              
             @@@@@@      ,@@@@@              
             @@@@@@@@@@@@@@@@@@              
          ,@@@@@@@@@@@@@@@@@@@@              
         @@@@@@@@@@@@@@@@@@@@@@              
             @@@@@@       @@@@@              
             @@@@@@       @@@@@              
             @@@@@@       @@@@@              
             @@@@@@       @@@@@              
             @@@@@@       @@@@@              
             @@@@@@       @@@@@              
             @@@@@@       @@@@@@@            
           @@@@@@@@       @@@@@@
    ''')


def ui_show_options(option_list):
    print("Valid choices:")
    for option in option_list:
        print(option)
    return input("Your choice: ")


def ui_handle_value_error(ve):
    error_messages = {
        'apartment': "The apartment number must be a positive integer value",
        'amount': "The amount must be a positive integer value",
        'type': "The type must be one of these values: " + str(get_type_list()),
        'arguments': "Invalid arguments",
        'relation': "Provide a valid relation [ < | = | > ]",
        'int': "Provide a valid integer",
        'increasing': "The first apartment number must be lower than the second one",
        'choice': "Invalid choice"
    }
    if str(ve) in error_messages.keys():
        print(error_messages[str(ve)])
    else:
        raise NotImplementedError('ValueError - ' + str(ve))


def raise_choice_error():
    raise ValueError('choice')
