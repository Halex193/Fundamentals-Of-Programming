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
        commands[command_name](apartment_expense_data, command_arguments)
    else:
        print("Command not recognized")











# endregion
run_tests()
run()
