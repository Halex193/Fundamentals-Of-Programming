# Assignment 03-04
# Udrea Horațiu 917


def run():
    apartment_expense_data = create_apartment_expense_data()
    populate_apartment_expense_data(apartment_expense_data)
    changes_stack = create_changes_stack()

    while True:
        command = input("> ")
        if command == "exit":
            return
        execute_command(apartment_expense_data, command, changes_stack)


# region commands
def get_command_name(command):
    return command.split(' ')[0]


def get_command_args(command):
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
        command_args = get_command_args(command)
        commands[command_name](apartment_expense_data, command_args)
    else:
        print("Command not recognized")


def create_changes_stack():
    return []


def push_command_stack(command_stack, command):
    command_stack.append(command)


def pop_command_stack(command_stack):
    if len(command_stack) == 0:
        return ""
    return command_stack.pop()


def ui_add(apartment_expense_data, args):
    try:
        added = command_add(apartment_expense_data, args)
        if added:
            print("Expense added")
        else:
            print("Expense already exists. Use 'replace' command instead")
        return True
    except ValueError as ve:
        ui_handle_value_error(ve)
        return False


def command_add(apartment_expense_data, args):
    if len(args) != 3:
        raise ValueError('args')
    apartment = int(args[0])
    if not valid_apartment(apartment):
        raise ValueError('apartment')
    type = args[1]
    if not valid_type(type):
        raise ValueError('type')
    amount = int(args[2])
    if not valid_amount(amount):
        raise ValueError('amount')
    return add_apartment_expense(apartment_expense_data, apartment, type, amount)


def ui_remove(apartment_expense_data, args):
    try:
        number = command_remove(apartment_expense_data, args)
        print(str(number) + " expense" + ("s" if number != 1 else "") + " removed")
        return True
    except ValueError as ve:
        ui_handle_value_error(ve)
        return False


def command_remove(apartment_expense_data, args):
    if len(args) not in range(1, 4 + 1):
        raise ValueError('args')
    if valid_apartment(args[0]):
        if len(args) == 1:
            return remove_apartment_expenses_from_apartment_number(apartment_expense_data, int(args[0]))
        elif len(args) == 3 and args[1] == "to" and valid_apartment(args[2]):
            return remove_apartment_expenses_from_apartment_range(apartment_expense_data, int(args[0]), int(args[2]))
        else:
            raise ValueError("args")
    elif valid_type(args[0]):
        return remove_apartment_expenses_from_type(apartment_expense_data, args[0])
    else:
        raise ValueError('args')


def ui_replace(apartment_expense_data, args):
    try:
        replaced = command_replace(apartment_expense_data, args)
        if replaced:
            print("Amount replaced")
        else:
            print("Expense does not exist. Use 'add' command instead")
        return True
    except ValueError as ve:
        ui_handle_value_error(ve)
        return False


def command_replace(apartment_expense_data, args):
    if len(args) != 4:
        raise ValueError('args')
    if not valid_apartment(args[0]):
        raise ValueError('apartment')
    apartment = int(args[0])
    if not valid_type(args[1]):
        raise ValueError('type')
    type = args[1]
    if args[2] != "with":
        raise ValueError('args')
    if not valid_amount(args[3]):
        raise ValueError('amount')
    amount = int(args[3])
    if apartment in get_apartments(apartment_expense_data) and \
            type in get_types_for_apartment(apartment_expense_data, apartment):
        set_apartment_expense(apartment_expense_data, apartment, type, amount)
        return True
    return False


def ui_list(apartment_expense_data, args):
    try:
        output = command_list(apartment_expense_data, args)
        if output == '':
            print("Nothing to show")
        else:
            print(output)
        return True
    except ValueError as ve:
        ui_handle_value_error(ve)
        return False


def command_list(apartment_expense_data, args):
    if len(args) > 2:
        raise ValueError('args')
    if len(args) == 0:
        return generate_list(list_all_expenses(apartment_expense_data))
    elif len(args) == 1:
        if not valid_apartment(args[0]):
            raise ValueError('apartment')
        apartment = int(args[0])
        return generate_list(list_expenses_for_apartment(apartment_expense_data, apartment))
    elif len(args) == 2:
        if not valid_relation(args[0]):
            raise ValueError('relation')
        relation = args[0]
        try:
            amount = int(args[1])
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


def ui_sum(apartment_expense_data, args):
    pass


def ui_max(apartment_expense_data, args):
    pass


def ui_sort(apartment_expense_data, args):
    pass


def ui_filter(apartment_expense_data, args):
    pass


def ui_undo(apartment_expense_data, args):
    pass


def ui_help(apartment_expense_data, args):
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
    if len(args) == 0:
        print("Valid commands:")
        for command in commands.keys():
            print(command)
        print("Type 'help <command>' to get the command's possible arguments")
    elif len(args) == 1:
        command = args[0]
        if command in commands.keys():
            print(commands[command])
        else:
            print("Unknown command")
    else:
        print("Unknown arguments")


def ui_credits(apartment_expense_data, command_args):
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
        'args': "Invalid arguments",
        'relation': "Provide a valid relation [ < | = | > ]",
        'int': "Provide a valid integer"
    }
    if str(ve) in error_messages.keys():
        print(error_messages[str(ve)])
    else:
        raise NotImplementedError('ValueError - ' + str(ve))


# endregion

# region apartment_expense_data
def create_apartment_expense_data():
    return {}


def add_apartment_expense(apartment_expense_data, apartment, type, amount):
    if get_apartment_expense(apartment_expense_data, apartment, type) is None:
        set_apartment_expense(apartment_expense_data, apartment, type, amount)
        return True
    return False


def set_apartment_expense(apartment_expense_data, apartment, type, amount):
    if not valid_apartment(apartment):
        raise ValueError('apartment')
    apartment = int(apartment)
    if not valid_type(type):
        raise ValueError('type')
    if not valid_amount(amount):
        raise ValueError('amount')
    amount = int(amount)

    if apartment in apartment_expense_data.keys():
        apartment_expense_data[apartment][type] = amount
    else:
        apartment_expense_data[apartment] = {type: amount}


def get_apartment_expense(apartment_expense_data, apartment, type):
    if not valid_apartment(apartment):
        raise ValueError('apartment')
    apartment = int(apartment)
    if not valid_type(type):
        raise ValueError('type')
    if apartment not in apartment_expense_data.keys():
        return None
    if type not in apartment_expense_data[apartment].keys():
        return None
    return apartment_expense_data[apartment][type]


def get_apartments(apartment_expense_data):
    return list(apartment_expense_data.keys())


def get_types_for_apartment(apartment_expense_data, apartment):
    if apartment_expense_data == 0:
        return []
    return list(apartment_expense_data[apartment].keys())


def remove_apartment_expenses_from_apartment_number(apartment_expense_data, apartment):
    removed = 0
    if apartment in get_apartments(apartment_expense_data):
        removed = len(get_types_for_apartment(apartment_expense_data, apartment))
        del apartment_expense_data[apartment]
    return removed


def remove_apartment_expenses_from_apartment_range(apartment_expense_data, apartment_start, apartment_end):
    removed = 0
    for apartment in range(apartment_start, apartment_end + 1):
        removed += remove_apartment_expenses_from_apartment_number(apartment_expense_data, apartment)
    return removed


def remove_apartment_expenses_from_type(apartment_expense_data, type):
    removed = 0
    for expense_set in apartment_expense_data.values():
        if type in expense_set.keys():
            del expense_set[type]
            removed += 1
    return removed


def populate_apartment_expense_data(apartment_expense_data):
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


# endregion


# region apartment_expense
def create_apartment_expense_dict(apartment, type, amount):
    if not valid_apartment(apartment):
        raise ValueError('apartment')
    apartment = int(apartment)
    if not valid_type(type):
        raise ValueError('type')
    if not valid_amount(amount):
        raise ValueError('amount')
    amount = int(amount)

    apartment_expense_dict = {'apartment': apartment,
                              'type': type,
                              'amount': amount
                              }
    return apartment_expense_dict


def get_apartment(apartment_expense_dict):
    return apartment_expense_dict['apartment']


def valid_apartment(apartment):
    try:
        apartment = int(apartment)
    except ValueError:
        return False

    if apartment > 0:
        return True


def get_amount(apartment_expense_dict):
    return apartment_expense_dict['amount']


def valid_amount(amount):
    try:
        amount = int(amount)
    except ValueError:
        return False

    if amount > 0:
        return True


def get_type_list():
    return ['water', 'heating', 'electricity', 'gas', 'other']


def get_type(apartment_expense_dict):
    return apartment_expense_dict['type']


def valid_type(type):
    return type in get_type_list()


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


def valid_relation(relation):
    relations = ["<", "=", ">"]
    return relation in relations


# endregion


def test_apartment_expense_dict():
    apartment_expense_dict = create_apartment_expense_dict(12, 'water', 45)
    assert get_apartment(apartment_expense_dict) == 12
    assert get_type(apartment_expense_dict) == 'water'
    assert get_amount(apartment_expense_dict) == 45

    try:
        create_apartment_expense_dict(12, 'sample', 240)
        assert False
    except ValueError as ve:
        assert str(ve) == 'type'

    try:
        create_apartment_expense_dict(-12, 'water', '240')
        assert False
    except ValueError as ve:
        assert str(ve) == 'apartment'

    try:
        create_apartment_expense_dict('12', 'other', -43)
        assert False
    except ValueError as ve:
        assert str(ve) == 'amount'


def test_apartment_expense_data():
    apartment_expense_data = create_apartment_expense_data()
    assert len(get_apartments(apartment_expense_data)) == 0

    add_apartment_expense(apartment_expense_data, 12, 'gas', 240)
    assert len(get_apartments(apartment_expense_data)) == 1
    assert get_apartment_expense(apartment_expense_data, 12, 'gas') == 240

    remove_apartment_expenses_from_apartment_number(apartment_expense_data, 12)
    assert len(get_apartments(apartment_expense_data)) == 0


def test_command_add():
    apartment_expense_data = create_apartment_expense_data()

    command_add(apartment_expense_data, [12, 'gas', 240])
    assert len(get_apartments(apartment_expense_data)) == 1
    assert get_apartment_expense(apartment_expense_data, 12, 'gas') == 240

    command_add(apartment_expense_data, ['14', 'water', 244])
    assert len(get_apartments(apartment_expense_data)) == 2
    assert get_apartment_expense(apartment_expense_data, '14', 'water') == 244


def test_command_remove():
    apartment_expense_data = create_apartment_expense_data()
    command_add(apartment_expense_data, [12, 'gas', 240])
    command_remove(apartment_expense_data, [12])
    assert len(get_apartments(apartment_expense_data)) == 0


def run_tests():
    test_apartment_expense_dict()
    test_apartment_expense_data()
    test_command_add()
    test_command_remove()


run_tests()
run()
