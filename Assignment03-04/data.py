# Assignment 03-04
# Udrea Horațiu 917
"""
This module provides the functionality for CRUD operations on the application data instance
apartment_expense_data
"""
from model import *


def create_apartment_expense_data():
    """
    Creates a new apartment expense data instance that holds all the application data
    :return: An empty apartment expense data instance
    """
    return {}


def get_apartment_expense(apartment_expense_data, apartment, type):
    """
    Gets the apartment expense amount for the given apartment and expense type
    :param apartment_expense_data: The data instance
    :param apartment: int/string - The apartment number
    :param type: string - The expense type
    :return: int - The amount of the expense for the given apartment and type.
             Returns None if the expense does not exist
    :raises ValueError: If the data parsing fails
    """
    apartment = parse_apartment(apartment)
    if apartment not in apartment_expense_data.keys():
        return None
    type = parse_type(type)
    if type not in apartment_expense_data[apartment].keys():
        return None
    return apartment_expense_data[apartment][type]


def set_apartment_expense(apartment_expense_data, apartment, type, amount):
    """
    Sets the apartment expense amount for the given apartment and type
    :param apartment_expense_data: The data instance
    :param apartment: int/string - The apartment number
    :param type: string - The expense type
    :param amount: int/string - The amount of the expense
    :raises ValueError: If the data parsing fails
    """
    apartment = parse_apartment(apartment)
    type = parse_type(type)
    amount = parse_amount(amount)

    if apartment in apartment_expense_data.keys():
        apartment_expense_data[apartment][type] = amount
    else:
        apartment_expense_data[apartment] = {type: amount}


def add_apartment_expense(apartment_expense_data, apartment, type, amount):
    """
    Adds an apartment expense to the data instance
    :param apartment_expense_data: The data instance
    :param apartment: int/string - The apartment number
    :param type: string - The expense type
    :param amount: int/string - The amount of the expense
    :returns: If the addition occurred, the apartment_expense_dict that has been added. Otherwise, returns None
    :raises ValueError: If the data parsing fails
    """
    if get_apartment_expense(apartment_expense_data, apartment, type) is None:
        set_apartment_expense(apartment_expense_data, apartment, type, amount)
        return create_apartment_expense_dict(apartment, type, amount)
    return None


def get_apartments(apartment_expense_data):
    """
    Returns a list of the apartments with expenses
    :param apartment_expense_data: The data instance
    :return: list - The apartment number list of integers
    """
    return list(apartment_expense_data.keys())


def get_types_for_apartment(apartment_expense_data, apartment):
    """
    Returns the list of expense types for the expenses of the apartment
    :param apartment_expense_data: The data instance
    :param apartment: int/string - THe apartment number
    :return: list - The expense type list of strings
    :raises ValueError: If the data parsing fails
    """
    apartment = parse_apartment(apartment)
    if apartment not in get_apartments(apartment_expense_data):
        return []
    return list(apartment_expense_data[apartment].keys())


def remove_expense(apartment_expense_data, apartment, type):
    """
    Removes an expense
    :param apartment_expense_data: The data instance
    :param apartment: int/string - The apartment number
    :param type: string - The expense type
    :return: The removed expense as a list if the removal occurred
             or an empty list otherwise (the expense does not exist)
    :raises ValueError: If the data parsing fails
    """
    apartment = parse_apartment(apartment)
    type = parse_type(type)
    if apartment in get_apartments(apartment_expense_data):
        if type in get_types_for_apartment(apartment_expense_data, apartment):
            amount = get_apartment_expense(apartment_expense_data, apartment, type)
            del apartment_expense_data[apartment][type]
            if len(apartment_expense_data[apartment]) == 0:
                remove_apartment_expenses(apartment_expense_data, apartment)
            return [create_apartment_expense_dict(apartment, type, amount)]
    return []


def remove_apartment_expenses(apartment_expense_data, apartment):
    """
    Removes the expenses of the apartment
    :param apartment_expense_data: The data instance
    :param apartment: int/string - The apartment number
    :returns: THe list of removed elements
    :raises ValueError: If the data parsing fails
    """
    apartment = parse_apartment(apartment)
    removed = []
    if apartment in get_apartments(apartment_expense_data):
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            amount = get_apartment_expense(apartment_expense_data, apartment, type)
            removed.append(create_apartment_expense_dict(apartment, type, amount))
        del apartment_expense_data[apartment]
    return removed


def remove_apartment_expenses_from_range(apartment_expense_data, start_apartment, end_apartment):
    """
    Removes a range of apartment expenses from a range of apartment numbers
    :param apartment_expense_data: The data instance
    :param start_apartment: The first apartment number to be removed
    :param end_apartment: The last apartment number to be removed
    :return: The removed expenses
    :raises ValueError: ValueError('increasing') if the end value is equal or higher than the start value
                        ValueError if the data parsing fails
    """
    start_apartment = parse_apartment(start_apartment)
    end_apartment = parse_apartment(end_apartment)
    if start_apartment >= end_apartment:
        raise ValueError('increasing')

    max_apartment_number = max(get_apartments(apartment_expense_data))
    if end_apartment > max_apartment_number:
        end_apartment = max_apartment_number

    removed = []
    for apartment in range(start_apartment, end_apartment + 1):
        removed.extend(remove_apartment_expenses(apartment_expense_data, apartment))
    return removed


def remove_apartment_expenses_from_type(apartment_expense_data, type):
    """
    Removes all the expenses of the given type
    :param apartment_expense_data: The data instance
    :param type: string - The expense type
    :return: The removed expenses
    :raises ValueError: If the data parsing fails
    """
    type = parse_type(type)
    apartments_to_delete = []
    for apartment in get_apartments(apartment_expense_data):
        if type in get_types_for_apartment(apartment_expense_data, apartment):
            apartments_to_delete.append(apartment)
    removed = []
    for apartment in apartments_to_delete:
        removed.extend(remove_expense(apartment_expense_data, apartment, type))
    return removed


def list_all_expenses(apartment_expense_data):
    """
    Gets all apartment expenses
    :param apartment_expense_data: The data instance
    :return: list of apartment_expense_dict - The list of all apartment expenses
    """
    apartment_expenses = []
    for apartment in get_apartments(apartment_expense_data):
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            amount = get_apartment_expense(apartment_expense_data, apartment, type)
            apartment_expenses.append(create_apartment_expense_dict(apartment, type, amount))
    return sorted(apartment_expenses, key=lambda apartment_expense_dict: get_apartment(apartment_expense_dict))


def list_expenses_for_apartment(apartment_expense_data, apartment):
    """
    Gets all apartment expenses for the given apartment number
    :param apartment_expense_data: The data instance
    :param apartment: int/string - The apartment number
    :return: list of apartment_expense_dict - The list of all apartment expenses of the given apartment
    """
    apartment = parse_apartment(apartment)
    apartment_expenses = []
    if apartment in get_apartments(apartment_expense_data):
        for type in get_types_for_apartment(apartment_expense_data, apartment):
            amount = get_apartment_expense(apartment_expense_data, apartment, type)
            apartment_expenses.append(create_apartment_expense_dict(apartment, type, amount))
    return apartment_expenses
