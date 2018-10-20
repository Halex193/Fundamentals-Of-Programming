# Assignment 03-04
# Udrea Horațiu 917


def run():
    apartment_expense_list = create_apartment_expense_list()
    populate_apartment_expense_list(apartment_expense_list)
    changes_stack = create_changes_stack()

    while True:
        command = input("> ")
        if command == "exit":
            return
        execute_command(apartment_expense_list, command, changes_stack)


# region commands
def get_command_name(command):
    return command.split(' ')[0]


def get_command_args(command):
    return command.split(' ')[1:]


def execute_command(apartment_expense_list, command, changes_stack):
    commands = {'add': ui_add,
                'remove': ui_remove,
                'replace': ui_replace,
                'list': ui_list,
                'sum': ui_sum,
                'max': ui_max,
                'sort': ui_sort,
                'filter': ui_filter,
                'undo': ui_undo,
                'help': ui_help
                }
    command_name = get_command_name(command)

    if command_name in commands.keys():
        command_args = get_command_args(command)
        commands[command_name](apartment_expense_list, command_args)
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


def ui_add(apartment_expense_list, args):
    try:
        command_add(apartment_expense_list, args)
        print("Expense added")
        return True
    except ValueError as ve:
        ui_handle_value_error(ve)
        return False


def command_add(apartment_expense_list, args):
    if len(args) != 3:
        raise ValueError('args')
    apartment = args[0]
    if not valid_apartment(apartment):
        raise ValueError('apartment')
    type = args[1]
    if not valid_type(type):
        raise ValueError('type')
    amount = args[2]
    if not valid_amount(amount):
        raise ValueError('amount')
    add_apartment_expense(apartment_expense_list, create_apartment_expense(apartment, amount, type))


def ui_remove(apartment_expense_list, args):
    try:
        command_remove(apartment_expense_list, args)
        print("Expenses removed")
        return True
    except ValueError as ve:
        ui_handle_value_error(ve)
        return False


def command_remove(apartment_expense_list, args):
    if len(args) in range(1, 4 + 1):
        raise ValueError('args')
    if valid_apartment(args[0]):
        if len(args) == 1:
            remove_apartment_expenses_from_apartment_number(apartment_expense_list, int(args[0]))
        elif len(args) == 3 and args[1] == "to" and valid_apartment(args[2]):
            remove_apartment_expenses_from_apartment_range(apartment_expense_list, int(args[0]), int(args[2]))
        else:
            raise ValueError("args")
    elif valid_type(args[0]):
        remove_apartment_expenses_from_type(apartment_expense_list, args[0])
    else:
        raise ValueError('args')


def ui_replace(apartment_expense_list, args):
    pass


def ui_list(apartment_expense_list, args):
    output = command_list(apartment_expense_list, args)
    if output == '':
        print("Nothing to show")
    else:
        print(output)
    return True


def command_list(apartment_expense_list, args):
    if len(args) == 0:
        return generate_list(apartment_expense_list)
    # TODO finish


def generate_list(apartment_expense_list):
    string_list = []
    for i in range(0, get_apartment_expense_list_length(apartment_expense_list)):
        string_list.append(apartment_expense_to_string(get_apartment_expense(apartment_expense_list, i)))
        if i != get_apartment_expense_list_length(apartment_expense_list) - 1:
            string_list.append("\n")
    return ''.join(string_list)


def ui_sum(apartment_expense_list, args):
    pass


def ui_max(apartment_expense_list, args):
    pass


def ui_sort(apartment_expense_list, args):
    pass


def ui_filter(apartment_expense_list, args):
    pass


def ui_undo(apartment_expense_list, args):
    pass


def ui_help(apartment_expense_list, command_args):
    pass


def ui_handle_value_error(ve):
    error_messages = {
        'apartment': "The apartment number must be a positive integer value",
        'amount': "The amount must be a positive integer value",
        'type': "The type must be one of these values: " + str(get_type_list()),
        'args': "Invalid arguments"
    }
    if str(ve) in error_messages.keys():
        print(error_messages[str(ve)])
    else:
        raise NotImplementedError('ValueError - ' + str(ve))


# endregion

# region apartment_expense_list
def create_apartment_expense_list():
    return []


def get_apartment_expense_list_length(apartment_expense_list):
    return len(apartment_expense_list)


def get_apartment_expense(apartment_expense_list, index):
    return apartment_expense_list[index]


def add_apartment_expense(apartment_expense_list, new_apartment_expense):
    apartment_expense_list.append(new_apartment_expense)


def remove_apartment_expense(apartment_expense_list, index):
    del apartment_expense_list[index]


def remove_apartment_expenses_from_apartment_number(apartment_expense_list, apartment):
    i = 0
    while i < get_apartment_expense_list_length(apartment_expense_list):
        if get_apartment(get_apartment_expense(apartment_expense_list, i)) == apartment:
            remove_apartment_expense(apartment_expense_list, i)
        else:
            i += 1


def remove_apartment_expenses_from_apartment_range(apartment_expense_list, apartment_start, apartment_end):
    i = 0
    while i < get_apartment_expense_list_length(apartment_expense_list):
        if get_apartment(get_apartment_expense(apartment_expense_list, i)) in range(apartment_start, apartment_end + 1):
            remove_apartment_expense(apartment_expense_list, i)
        else:
            i += 1


def remove_apartment_expenses_from_type(apartment_expense_list, type):
    i = 0
    while i < get_apartment_expense_list_length(apartment_expense_list):
        if get_type(get_apartment_expense(apartment_expense_list, i)) == type:
            remove_apartment_expense(apartment_expense_list, i)
        else:
            i += 1


def populate_apartment_expense_list(apartment_expense_list):
    add_apartment_expense(apartment_expense_list, create_apartment_expense(1, 100, 'water'))
    add_apartment_expense(apartment_expense_list, create_apartment_expense(2, 200, 'heating'))
    add_apartment_expense(apartment_expense_list, create_apartment_expense(3, 300, 'electricity'))
    add_apartment_expense(apartment_expense_list, create_apartment_expense(4, 400, 'gas'))
    add_apartment_expense(apartment_expense_list, create_apartment_expense(5, 500, 'other'))


# endregion


# region apartment_expense
def create_apartment_expense(apartment, amount, type):
    apartment_expense = {}
    set_apartment(apartment_expense, apartment)
    set_amount(apartment_expense, amount)
    set_type(apartment_expense, type)
    return apartment_expense


def get_apartment(apartment_expense):
    return apartment_expense['apartment']


def valid_apartment(apartment):
    try:
        apartment = int(apartment)
    except ValueError:
        return False

    if apartment > 0:
        return True


def set_apartment(apartment_expense, apartment):
    if not valid_apartment(apartment):
        raise ValueError('apartment')
    apartment_expense['apartment'] = int(apartment)


def get_amount(apartment_expense):
    return apartment_expense['amount']


def valid_amount(amount):
    try:
        amount = int(amount)
    except ValueError:
        return False

    if amount > 0:
        return True


def set_amount(apartment_expense, amount):
    if not valid_amount(amount):
        raise ValueError('amount')
    apartment_expense['amount'] = int(amount)


def get_type_list():
    return ['water', 'heating', 'electricity', 'gas', 'other']


def get_type(apartment_expense):
    return apartment_expense['type']


def valid_type(type):
    return type in get_type_list()


def set_type(apartment_expense, type):
    if not valid_type(type):
        raise ValueError('type')
    apartment_expense['type'] = type


def apartment_expense_to_string(apartment_expense):
    apartment = get_apartment(apartment_expense)
    amount = get_amount(apartment_expense)
    type = get_type(apartment_expense)
    max_length = 0
    for i in get_type_list():
        if len(i) > max_length:
            max_length = len(i)

    return "{ Apartment " + str(apartment) + ", Expense type: " + type + \
           (max_length - len(type)) * " " + ", Amount: " + str(amount) + " RON }"


# endregion


def test_apartment_expense():
    apartment_expense = create_apartment_expense(12, 240, 'water')
    assert get_apartment(apartment_expense) == 12
    assert get_amount(apartment_expense) == 240
    assert get_type(apartment_expense) == 'water'

    try:
        create_apartment_expense(12, 240, 'sample')
    except ValueError as ve:
        assert str(ve) == 'type'

    try:
        create_apartment_expense(-12, '240', 'water')
    except ValueError as ve:
        assert str(ve) == 'apartment'

    try:
        create_apartment_expense('12', -43, 'other')
    except ValueError as ve:
        assert str(ve) == 'amount'


def test_apartment_expense_list():
    apartment_expense_list = create_apartment_expense_list()
    assert get_apartment_expense_list_length(apartment_expense_list) == 0

    apartment_expense1 = create_apartment_expense(12, 240, 'gas')
    add_apartment_expense(apartment_expense_list, apartment_expense1)
    assert get_apartment_expense_list_length(apartment_expense_list) == 1
    apartment_expense2 = get_apartment_expense(apartment_expense_list, 0)
    assert apartment_expense2 == apartment_expense1

    apartment_expense1 = create_apartment_expense(54, 7240, 'gas')
    add_apartment_expense(apartment_expense_list, apartment_expense1)
    assert get_apartment_expense_list_length(apartment_expense_list) == 2
    apartment_expense2 = get_apartment_expense(apartment_expense_list, 1)
    assert apartment_expense2 == apartment_expense1

    remove_apartment_expense(apartment_expense_list, 1)
    assert get_apartment_expense_list_length(apartment_expense_list) == 1


def test_command_add():
    apartment_expense_list = create_apartment_expense_list()

    command_add(apartment_expense_list, [12, 'gas', 240])
    assert get_apartment_expense_list_length(apartment_expense_list) == 1
    apartment_expense = get_apartment_expense(apartment_expense_list, 0)
    assert get_apartment(apartment_expense) == 12
    assert get_amount(apartment_expense) == 240
    assert get_type(apartment_expense) == 'gas'

    command_add(apartment_expense_list, ['14', 'water', 244])
    assert get_apartment_expense_list_length(apartment_expense_list) == 2
    apartment_expense = get_apartment_expense(apartment_expense_list, 1)
    assert get_apartment(apartment_expense) == 14
    assert get_amount(apartment_expense) == 244
    assert get_type(apartment_expense) == 'water'


def run_tests():
    test_apartment_expense()
    test_apartment_expense_list()
    test_command_add()


run_tests()
run()
