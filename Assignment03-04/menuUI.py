from logic import *


def ui_add(apartment_expense_data, arguments):
    try:
        added = command_add(apartment_expense_data, arguments)
        if added:
            print("Expense added")
        else:
            print("Expense already exists. Use 'replace' command instead")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_remove(apartment_expense_data, arguments):
    try:
        number = command_remove(apartment_expense_data, arguments)
        print(str(number) + " expense" + ("s" if number != 1 else "") + " removed")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_replace(apartment_expense_data, arguments):
    try:
        replaced = command_replace(apartment_expense_data, arguments)
        if replaced:
            print("Amount replaced")
        else:
            print("Expense does not exist. Use 'add' command instead")
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_list(apartment_expense_data, arguments):
    try:
        output = command_list(apartment_expense_data, arguments)
        if output == '':
            print("Nothing to show")
        else:
            print(output)
        return True
    except ValueError as value_error:
        ui_handle_value_error(value_error)
        return False


def ui_sum(apartment_expense_data, arguments):
    pass


def ui_max(apartment_expense_data, arguments):
    pass


def ui_sort(apartment_expense_data, arguments):
    pass


def ui_filter(apartment_expense_data, arguments):
    pass


def ui_undo(apartment_expense_data, arguments):
    pass


def ui_help(apartment_expense_data, arguments):
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
max 25 – write the maximum amount per each expense type for apartment 25. 
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


def ui_credits(apartment_expense_data, command_arguments):
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
        'incr': "The first apartment number must be lower than the second one"
    }
    if str(ve) in error_messages.keys():
        print(error_messages[str(ve)])
    else:
        raise NotImplementedError('ValueError - ' + str(ve))