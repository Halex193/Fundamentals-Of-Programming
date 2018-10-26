"""
Defines the operations on the apartment_expense_dict model
"""


def create_apartment_expense_dict(apartment, type, amount):
    """
    Creates an apartment_expense_dict instance from given parameters
    :param apartment: int/string - The apartment number
    :param type: string - The type of the expense
    :param amount: int/string - The amount of the expense
    :return: The created apartment_expense_dict with the given values
    """
    apartment = parse_apartment(apartment)
    type = parse_type(type)
    amount = parse_amount(amount)

    apartment_expense_dict = {'apartment': apartment,
                              'type': type,
                              'amount': amount
                              }
    return apartment_expense_dict


def get_apartment(apartment_expense_dict):
    return apartment_expense_dict['apartment']


def valid_apartment(apartment):
    """
    Checks if the given apartment number is valid
    :param apartment: int/string - The apartment number
    :return: True if the apartment number is valid, False otherwise
    """
    try:
        apartment = int(apartment)
    except ValueError:
        return False

    if apartment > 0:
        return True


def parse_apartment(apartment):
    """
    Tries to convert the given apartment number to integer. On success, returns the integer, otherwise raises
    ValueError('apartment')
    :param apartment: int/string - The apartment number
    :return: int - The apartment number
    :raises ValueError: ValueError('apartment') if the apartment is not valid
    """
    if not valid_apartment(apartment):
        raise ValueError('apartment')
    return int(apartment)


def get_amount(apartment_expense_dict):
    return apartment_expense_dict['amount']


def valid_amount(amount):
    """
    Checks if the given amount is valid
    :param amount: int/string - The amount of the expense
    :return: True if the amount is valid, False otherwise
    """
    try:
        amount = int(amount)
    except ValueError:
        return False

    if amount > 0:
        return True


def parse_amount(amount):
    """
    Tries to convert the given amount to integer. On success, returns the integer, otherwise raises
    ValueError('amount')
    :param amount: int/string - The amount of the expense
    :return: int - The amount of the expense
    :raises ValueError: ValueError('amount') if the amount is not valid
    """
    if not valid_amount(amount):
        raise ValueError('amount')
    return int(amount)


def get_type_list():
    """
    Get a list of the accepted expense types
    :return: list - A lit of accepted expense types as strings
    """
    return ['water', 'heating', 'electricity', 'gas', 'other']


def get_type(apartment_expense_dict):
    return apartment_expense_dict['type']


def valid_type(type):
    """
    Checks if the given expense type is valid
    :param type: string - The expense type
    :return: True if the expense type is valid, False otherwise
    """
    return type in get_type_list()


def parse_type(type):
    """
    Checks if the given value is an accept expense type. If it is, returns the string, otherwise raises
    ValueError('type')
    :param type: string - The expense type
    :return: string - The expense type
    :raises ValueError: ValueError('type') if the type is not valid
    """
    if not valid_type(type):
        raise ValueError('type')
    return type


def valid_integer(integer):
    """
    Checks if the given string is an integer
    :param integer: int/string - The input string to check
    :return: True if the string is a valid integer, False otherwise
    """
    try:
        int(integer)
        return True
    except ValueError:
        return False


def parse_int(integer):
    """
    Checks if the given string is a valid integer. If it is, returns the integer, otherwise raises
    ValueError('int')
    :param integer: int/string - The input string to parse
    :return: int - The converted integer
    :raises ValueError: ValueError('int') if the string is not a valid integer
    """
    if not valid_integer(integer):
        raise ValueError('int')
    return int(integer)


def valid_relation(relation):
    """
    Checks if the given string is a valid relation
    :param relation: string - The input relation to check
    :return: True if the string is a valid relation, False otherwise
    """
    relations = ["<", "=", ">"]
    return relation in relations


def parse_relation(relation):
    """
    Checks if the given string is a valid relation. If it is, returns the string, otherwise raises
    ValueError('relation')
    :param relation: string - The input string to parse
    :return: string - The relation
    :raises ValueError: ValueError('relation') if the string is not a valid relation
    """
    if not valid_relation(relation):
        raise ValueError('relation')
    return relation
