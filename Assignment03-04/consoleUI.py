# Assignment 03-04
# Udrea Horațiu 917
"""
This is the console UI module
"""
from logic import *


def run():
    data = initialize_data()
    apartment_expense_data = data[0]
    changes_stack = data[1]

    print("Type 'help' to get the valid commands")
    while True:
        command = input("> ")
        if command == "exit":
            return
        execute_command(apartment_expense_data, command, changes_stack)


def get_command_name(command):
    return command.split(' ')[0]


def get_command_arguments(command):
    return command.split(' ')[1:]


def execute_command(apartment_expense_data, command, changes_stack):
    commands = {'add': ui_add,
                'remove': ui_remove,
                'replace': ui_replace,
                'list': ui_list,
                'sum': ui_sum,
                'max': ui_max,
                'sort': ui_sort,
                'filter': ui_filter,
                'undo': ui_undo,
                'help': ui_help,
                'credits': ui_credits
                }
    command_name = get_command_name(command)

    if command_name in commands.keys():
        command_arguments = get_command_arguments(command)
        commands[command_name](apartment_expense_data, command_arguments, changes_stack)
    else:
        print("Command not recognized")


def ui_add(apartment_expense_data, arguments, changes_stack):
    try:
        added = command_add(apartment_expense_data, arguments, changes_stack)
        if added:
            print("Expense added")
        else:
            print("Expense already exists. Use 'replace' command instead")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_remove(apartment_expense_data, arguments, changes_stack):
    try:
        number = command_remove(apartment_expense_data, arguments, changes_stack)
        print(str(number) + " expense" + ("s" if number != 1 else "") + " removed")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_replace(apartment_expense_data, arguments, changes_stack):
    try:
        replaced = command_replace(apartment_expense_data, arguments, changes_stack)
        if replaced:
            print("Amount replaced")
        else:
            print("Expense does not exist. Use 'add' command instead")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_list(apartment_expense_data, arguments, changes_stack):
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
    string_list = []
    for apartment_expense in apartment_expenses:
        string_list.append(apartment_expense_dict_to_string(apartment_expense) + "\n")
    return ''.join(string_list)


def generate_apartment_list(apartment_list):
    string_list = []
    for apartment in apartment_list:
        string_list.append(str(apartment) + ", ")
    return ''.join(string_list)


def ui_sum(apartment_expense_data, arguments, changes_stack):
    try:
        sum = command_sum(apartment_expense_data, arguments)
        if sum != 0:
            print("The " + arguments[0] + " expense sum is " + str(sum) + " RON")
        else:
            print("There are no " + arguments[0] + " expenses")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_max(apartment_expense_data, arguments, changes_stack):
    try:
        max = command_max(apartment_expense_data, arguments)
        print_max(max)
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def print_max(max):
    if len(max) == 0:
        print("There are no registered expenses")
    else:
        for type in max.keys():
            print("Apartment " + str(max[type][0]) + " has the maximum expense for '" + type + "', which is " + str(
                max[type][1]))


def ui_sort(apartment_expense_data, arguments, changes_stack):
    try:
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
    for pair in expense_list:
        print("The total '" + pair[0] + "' expenses are " + str(pair[1]) + " RON")


def ui_filter(apartment_expense_data, arguments, changes_stack):
    try:
        removed = command_filter(apartment_expense_data, arguments, changes_stack)
        if removed == 0:
            print("Nothing to remove")
        else:
            print(str(removed) + " expenses removed")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_undo(apartment_expense_data, arguments, changes_stack):
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


def ui_help(apartment_expense_data, arguments, changes_stack):
    commands = {
        'add': '''
add <apartment> <type> <amount>

e.g. 
add 25 gas 100 – add to apartment 25 an expense for gas in amount of 100 RON.
''',

        'remove': '''
remove <apartment>
remove <start apartment> to <end apartment>
remove <type>

e.g.  
remove 15 – remove all the expenses of apartment 15.
remove 5 to 10 – remove all the expenses from apartments between 5 and 10.
remove gas – remove all the expenses for gas from all apartments.
''',

        'replace': '''
replace <apartment> <type> with <amount>

e.g.
replace 12 gas with 200 – replace the amount of the expense with type gas for apartment 12 with 200 RON.
''',
        'list': '''
list
list <apartment>
list [ < | = | > ] <amount>

e.g. 
list – write the entire list of expenses.
list 15 – write all expenses for apartment 15.
list > 100 - write all the apartments having total expenses > 100 RON.
list = 17 - write all the apartments having total expenses = 17 RON.
''',
        'sum': '''
sum <type>

e.g. 
sum gas – write the total amount for the expenses having type “gas”. 
''',
        'max': '''
max <apartment> 

e.g. 
max 25 – write the maximum amount of the expenses for apartment 25. 
''',
        'sort': '''
sort apartment
sort type 

e.g. 
sort apartment – write the list of apartments sorted ascending by total amount of expenses. 
sort type – write the total amount of expenses for each type, sorted ascending by amount of money. 
        ''',
        'filter': '''
filter <type>
filter <value>      

e.g.
filter gas – keep only expenses for “gas”. 
filter 300 – keep only expenses having an amount of money smaller than 300 RON. 
''',
        'undo': '''
undo

undo – the last operation that has modified program data will be reversed. 
You can undo all operations performed since program start by repeatedly calling this function. 

''',
        'help': "Choose another command",
        'credits': "Shows the credits of the program"
    }
    if len(arguments) == 0:
        print("Valid commands:")
        for command in commands.keys():
            print(command)
        print("Type 'help <command>' to get the command's possible arguments")
    elif len(arguments) == 1:
        command = arguments[0]
        if command in commands.keys():
            print(commands[command])
        else:
            print("Unknown command")
    else:
        print("Unknown arguments")


def ui_credits(apartment_expense_data=None, command_arguments=None, changes_stack=None):
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


def ui_handle_value_error(ve):
    error_messages = {
        'apartment': "The apartment number must be a positive integer value",
        'amount': "The amount must be a positive integer value",
        'type': "The type must be one of these values: " + str(get_type_list()),
        'arguments': "Invalid arguments",
        'relation': "Provide a valid relation [ < | = | > ]",
        'int': "Provide a valid integer",
        'increasing': "The first apartment number must be lower than the second one"
    }
    if str(ve) in error_messages.keys():
        print(error_messages[str(ve)])
    else:
        raise NotImplementedError('ValueError - ' + str(ve))
