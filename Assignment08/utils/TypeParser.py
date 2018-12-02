from datetime import date

class TypeParser:
    @staticmethod
    def parseInt(string: str, errorType: type) -> int:
        """
        Parses a number to an integer. If the conversion fails, raises the specified exception
        """
        try:
            return int(string)
        except ValueError:
            raise errorType()

    @staticmethod
    def parseDate(string: str, errorType: type) -> date:
        """
        Parses a string to a date. Valid format: day.month.year .
        If the conversion fails, raises the specified exception
        """
        try:
            symbols = string.split('.')
            if len(symbols) != 3:
                raise errorType()
            day = int(symbols[0])
            month = int(symbols[1])
            year = int(symbols[2])
            return date(year, month, day)
        except ValueError:
            raise errorType()
