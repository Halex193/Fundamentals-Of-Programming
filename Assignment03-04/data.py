def create_changes_stack():
    return []


def push_command_stack(command_stack, command):
    command_stack.append(command)


def pop_command_stack(command_stack):
    if len(command_stack) == 0:
        return ""
    return command_stack.pop()


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
    max_apartment_number = max(get_apartments(apartment_expense_data))
    if apartment_end > max_apartment_number:
        apartment_end = max_apartment_number

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


# region apartment_expense_dict
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


def valid_integer(integer):
    try:
        int(integer)
        return True
    except ValueError:
        return False


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
