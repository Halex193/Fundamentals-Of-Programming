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
    changes_stack = create_changes_stack()

    command_add(apartment_expense_data, [12, 'gas', 240], changes_stack)
    assert len(get_apartments(apartment_expense_data)) == 1
    assert get_apartment_expense(apartment_expense_data, 12, 'gas') == 240

    command_add(apartment_expense_data, ['14', 'water', 244], changes_stack)
    assert len(get_apartments(apartment_expense_data)) == 2
    assert get_apartment_expense(apartment_expense_data, '14', 'water') == 244


def test_command_remove():
    apartment_expense_data = create_apartment_expense_data()
    changes_stack = create_changes_stack()

    # remove from apartment number
    command_add(apartment_expense_data, [12, 'gas', 240], changes_stack)
    command_add(apartment_expense_data, [12, 'water', 50], changes_stack)
    command_remove(apartment_expense_data, [12], changes_stack)
    assert len(get_apartments(apartment_expense_data)) == 0
    # remove range of apartments
    command_add(apartment_expense_data, [1, 'gas', 240], changes_stack)
    command_add(apartment_expense_data, [2, 'water', 240], changes_stack)
    command_add(apartment_expense_data, [3, 'gas', 560], changes_stack)
    command_add(apartment_expense_data, [4, 'gas', 240], changes_stack)
    command_remove(apartment_expense_data, [1, "to", 3], changes_stack)
    assert len(get_apartments(apartment_expense_data)) == 1
    # remove expense type
    command_add(apartment_expense_data, [1, 'gas', 9], changes_stack)
    command_add(apartment_expense_data, [2, 'water', 98], changes_stack)
    command_add(apartment_expense_data, [6, 'electricity', 87], changes_stack)
    command_add(apartment_expense_data, [7, 'water', 76], changes_stack)
    command_remove(apartment_expense_data, ["water"], changes_stack)
    assert len(get_apartments(apartment_expense_data)) == 3


def test_command_replace():
    apartment_expense_data = create_apartment_expense_data()
    changes_stack = create_changes_stack()
    populate_apartment_expense_data(apartment_expense_data)

    assert command_replace(apartment_expense_data, [3, 'electricity', 'with', 400], changes_stack)
    assert get_apartment_expense(apartment_expense_data, 3, 'electricity') == 400
    assert len(get_apartments(apartment_expense_data)) == 6
    assert len(get_types_for_apartment(apartment_expense_data, 3)) == 1

    assert command_replace(apartment_expense_data, [3, 'gas', 'with', 500], changes_stack) is False
    assert get_apartment_expense(apartment_expense_data, 3, 'electricity') == 400
    assert len(get_apartments(apartment_expense_data)) == 6

    try:
        command_replace(apartment_expense_data, [3, 'gas', 'sample data', 500], changes_stack)
        assert False
    except ValueError as value_error:
        assert str(value_error) == 'arguments'


def test_command_list():
    apartment_expense_data = create_apartment_expense_data()
    changes_stack = create_changes_stack()
    command_add(apartment_expense_data, [3, 'gas', 100], changes_stack)

    apartment_expense_list = command_list(apartment_expense_data, [], lambda value: value, lambda value: value)
    apartment_expense = apartment_expense_list[0]
    assert get_apartment(apartment_expense) == 3
    assert get_type(apartment_expense) == 'gas'
    assert get_amount(apartment_expense) == 100

    command_remove(apartment_expense_data, [3], changes_stack)
    populate_apartment_expense_data(apartment_expense_data)
    apartment_expense_list = command_list(apartment_expense_data, ["3"], lambda value: value, lambda value: value)
    apartment_expense = apartment_expense_list[0]
    assert get_apartment(apartment_expense) == 3
    assert get_type(apartment_expense) == 'electricity'
    assert get_amount(apartment_expense) == 300

    apartment_list = command_list(apartment_expense_data, ["<", "210"], lambda value: value, lambda value: value)
    assert apartment_list[0] == 1

    apartment_list = command_list(apartment_expense_data, [">", "560"], lambda value: value, lambda value: value)
    assert apartment_list[0] == 4

    apartment_list = command_list(apartment_expense_data, ["=", "550"], lambda value: value, lambda value: value)
    assert apartment_list[0] == 6

    apartment_list = command_list(apartment_expense_data, [">", "300"], lambda value: value, lambda value: value)
    assert apartment_list == [4, 5, 6]


def test_command_sum():
    apartment_expense_data = create_apartment_expense_data()
    changes_stack = create_changes_stack()
    command_add(apartment_expense_data, [3, 'gas', 100], changes_stack)

    assert command_sum(apartment_expense_data, ['water']) == 0
    assert command_sum(apartment_expense_data, ['gas']) == 100

    populate_apartment_expense_data(apartment_expense_data)
    assert command_sum(apartment_expense_data, ['water']) == 400
    assert command_sum(apartment_expense_data, ['gas']) == 600
    assert command_sum(apartment_expense_data, ['electricity']) == 300
    assert command_sum(apartment_expense_data, ['other']) == 600
    assert command_sum(apartment_expense_data, ['heating']) == 650


def test_command_max():
    apartment_expense_data = create_apartment_expense_data()
    changes_stack = create_changes_stack()
    command_add(apartment_expense_data, [3, 'gas', 100], changes_stack)

    assert command_max(apartment_expense_data, [])['gas'][0] == 3
    assert command_max(apartment_expense_data, [])['gas'][1] == 100

    populate_apartment_expense_data(apartment_expense_data)
    assert command_max(apartment_expense_data, [])['gas'][0] == 4
    assert command_max(apartment_expense_data, [])['gas'][1] == 400
    assert command_max(apartment_expense_data, [])['water'][0] == 4
    assert command_max(apartment_expense_data, [])['water'][1] == 200
    assert command_max(apartment_expense_data, [])['electricity'][0] == 3
    assert command_max(apartment_expense_data, [])['electricity'][1] == 300
    assert command_max(apartment_expense_data, [])['other'][0] == 5
    assert command_max(apartment_expense_data, [])['other'][1] == 500
    assert command_max(apartment_expense_data, [])['heating'][0] == 6
    assert command_max(apartment_expense_data, [])['heating'][1] == 450


def test_command_sort():
    apartment_expense_data = create_apartment_expense_data()
    changes_stack = create_changes_stack()
    command_add(apartment_expense_data, [3, 'gas', 100], changes_stack)
    assert command_sort(apartment_expense_data, ['apartment'], lambda value: value, lambda value: value) == [3]
    assert command_sort(apartment_expense_data, ['type'], lambda value: value, lambda value: value)[-1] == ('gas', 100)
    command_remove(apartment_expense_data, ["3"], changes_stack)

    populate_apartment_expense_data(apartment_expense_data)
    apartment_list = command_sort(apartment_expense_data, ['apartment'], lambda value: value, lambda value: value)
    assert apartment_list == [1, 2, 3, 5, 6, 4]
    type_list = command_sort(apartment_expense_data, ['type'], lambda value: value, lambda value: value)
    assert type_list == [('electricity', 300), ('water', 400), ('gas', 500), ('other', 600), ('heating', 650)]


def test_command_filter():
    apartment_expense_data = create_apartment_expense_data()
    changes_stack = create_changes_stack()
    command_add(apartment_expense_data, [3, 'gas', 100], changes_stack)

    assert command_filter(apartment_expense_data, ['gas'], changes_stack) == 0
    assert command_filter(apartment_expense_data, ['water'], changes_stack) == 1

    command_add(apartment_expense_data, [3, 'gas', 100], changes_stack)

    assert command_filter(apartment_expense_data, ['300'], changes_stack) == 0
    assert command_filter(apartment_expense_data, ['50'], changes_stack) == 1

    populate_apartment_expense_data(apartment_expense_data)
    assert command_filter(apartment_expense_data, ['other'], changes_stack) == 8
    assert command_filter(apartment_expense_data, ['300'], changes_stack) == 1
    assert get_apartment_expense(apartment_expense_data, 2, 'other') == 100
    assert get_apartment_expense(apartment_expense_data, 1, 'gas') is None
    assert get_apartment_expense(apartment_expense_data, 6, 'heating') is None
    assert get_apartment_expense(apartment_expense_data, 5, 'other') is None


def test_command_undo():
    apartment_expense_data = create_apartment_expense_data()
    changes_stack = create_changes_stack()
    command_add(apartment_expense_data, [3, 'gas', 100], changes_stack)

    command_undo(apartment_expense_data, [], changes_stack)
    assert get_apartment_expense(apartment_expense_data, 3, 'gas') is None

    command_add(apartment_expense_data, [3, 'gas', 100], changes_stack)
    command_add(apartment_expense_data, [6, 'water', 200], changes_stack)
    command_undo(apartment_expense_data, [], changes_stack)
    command_undo(apartment_expense_data, [], changes_stack)
    assert get_apartment_expense(apartment_expense_data, 3, 'gas') is None
    assert get_apartment_expense(apartment_expense_data, 6, 'water') is None

    populate_apartment_expense_data(apartment_expense_data)
    command_remove(apartment_expense_data, [1, 'to', 6], changes_stack)
    command_undo(apartment_expense_data, [], changes_stack)
    assert len(get_apartments(apartment_expense_data)) == 6
    assert get_apartment_expense(apartment_expense_data, 3, 'electricity') == 300
    command_remove(apartment_expense_data, [1], changes_stack)
    command_undo(apartment_expense_data, [], changes_stack)
    assert get_apartment_expense(apartment_expense_data, 1, 'water') == 100
    command_remove(apartment_expense_data, ['water'], changes_stack)
    command_undo(apartment_expense_data, [], changes_stack)
    assert get_apartment_expense(apartment_expense_data, 1, 'water') == 100


def populate_apartment_expense_data(apartment_expense_data):
    """
    Populates the list with sample data
    :param apartment_expense_data: The data instance
    """
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


def run_tests():
    test_apartment_expense_dict()
    test_apartment_expense_data()
    test_command_add()
    test_command_remove()
    test_command_replace()
    test_command_list()
    test_command_sum()
    test_command_max()
    test_command_sort()
    test_command_filter()
    test_command_undo()
