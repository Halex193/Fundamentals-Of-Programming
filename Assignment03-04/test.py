# Assignment 03-04
# Udrea Horațiu 917

from logic import *


def test_apartment_expense_dict():
    apartment_expense_dict = create_apartment_expense_dict(12, 'water', 45)
    assert get_apartment(apartment_expense_dict) == 12
    assert get_type(apartment_expense_dict) == 'water'
    assert get_amount(apartment_expense_dict) == 45

    try:
        create_apartment_expense_dict(12, 'sample', 240)
        assert False
    except ValueError as value_error:
        assert str(value_error) == 'type'

    try:
        create_apartment_expense_dict(-12, 'water', '240')
        assert False
    except ValueError as value_error:
        assert str(value_error) == 'apartment'

    try:
        create_apartment_expense_dict('12', 'other', -43)
        assert False
    except ValueError as value_error:
        assert str(value_error) == 'amount'


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
