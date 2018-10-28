# Assignment 03-04
# Udrea Horațiu 917
"""
The test module of the application
"""
from logic import *


def test_apartment_expense_dict():
    # test creation and getters
    apartment_expense_dict = create_apartment_expense_dict(12, 'water', 45)
    assert get_apartment(apartment_expense_dict) == 12
    assert get_type(apartment_expense_dict) == 'water'
    assert get_amount(apartment_expense_dict) == 45

    # test errors
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
    # test creation
    assert len(get_apartments(apartment_expense_data)) == 0

    # test addition of elements
    add_apartment_expense(apartment_expense_data, 12, 'gas', 240)
    assert len(get_apartments(apartment_expense_data)) == 1
    assert get_apartment_expense(apartment_expense_data, 12, 'gas') == 240
    add_apartment_expense(apartment_expense_data, 1, 'water', 50)
    assert len(get_apartments(apartment_expense_data)) == 2
    assert get_apartment_expense(apartment_expense_data, 1, 'water') == 50

    # test getters
    assert 1 in get_apartments(apartment_expense_data)
    assert 12 in get_apartments(apartment_expense_data)
    assert 'gas' in get_types_for_apartment(apartment_expense_data, 12)

    # test updating of elements
    set_apartment_expense(apartment_expense_data, 1, 'water', 500)
    assert get_apartment_expense(apartment_expense_data, 1, 'water') == 500
    set_apartment_expense(apartment_expense_data, 12, 'gas', 250)
    assert get_apartment_expense(apartment_expense_data, 12, 'gas') == 250

    # test removal of elements
    remove_apartment_expenses(apartment_expense_data, 12)
    assert len(get_apartments(apartment_expense_data)) == 1
    add_apartment_expense(apartment_expense_data, 2, 'gas', 500)
    remove_apartment_expenses_from_range(apartment_expense_data, 1, 3)
    assert len(get_apartments(apartment_expense_data)) == 0
    add_apartment_expense(apartment_expense_data, 3, 'water', 240)
    add_apartment_expense(apartment_expense_data, 4, 'water', 3000)
    remove_apartment_expenses_from_type(apartment_expense_data, 'water')
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
    # remove from apartment number
    command_add(apartment_expense_data, [12, 'gas', 240])
    command_add(apartment_expense_data, [12, 'water', 50])
    command_remove(apartment_expense_data, [12])
    assert len(get_apartments(apartment_expense_data)) == 0
    # remove range of apartments
    command_add(apartment_expense_data, [1, 'gas', 240])
    command_add(apartment_expense_data, [2, 'water', 240])
    command_add(apartment_expense_data, [3, 'gas', 560])
    command_add(apartment_expense_data, [4, 'gas', 240])
    command_remove(apartment_expense_data, [1, "to", 3])
    assert len(get_apartments(apartment_expense_data)) == 1
    # remove expense type
    command_add(apartment_expense_data, [1, 'gas', 9])
    command_add(apartment_expense_data, [2, 'water', 98])
    command_add(apartment_expense_data, [6, 'electricity', 87])
    command_add(apartment_expense_data, [7, 'water', 76])
    command_remove(apartment_expense_data, ["water"])
    assert len(get_apartments(apartment_expense_data)) == 3


def run_tests():
    test_apartment_expense_dict()
    test_apartment_expense_data()
    test_command_add()
    test_command_remove()
