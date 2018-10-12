# Determine a calendar data (as year, month, day) starting from two integer numbers representing the year and the day
#  number inside that year.


def month_days(month_number):
    months = {
        1: ('January', 31),
        2: ('February', 28),
        3: ('March', 31),
        4: ('April', 30),
        5: ('May', 31),
        6: ('June', 30),
        7: ('July', 31),
        8: ('August', 31),
        9: ('September', 30),
        10: ('October', 31),
        11: ('November', 30),
        12: ('December', 31)
    }
    if month_number == 2 and leapYear:
        return 29
    return months.get(month_number)[1]


year = int(input("Year: "))
days = int(input("Number of the day: "))
leapYear = (year % 4 == 0)
month = 1

while days - month_days(month) > 0:
    days -= month_days(month)
    month += 1

print('The date is ' + str(days) + '.' + str(month) + '.' + str(year))
