class BrainfuckInterpreterException(Exception):
    """ Общее исключение для всей программы """
    pass


# Syntax exceptions ========================================================
class SyntaxErrorException(BrainfuckInterpreterException):
    """ Общее исключение для синтаксической ошибки """
    pass


class UnmatchedOpeningBracketException(SyntaxErrorException):
    """ Не найдена ответная открывающая скобка """
    pass


class UnmatchedClosingBracketException(SyntaxErrorException):
    """ Не найдена ответная закрывающая скобка """
    pass


# Runtime exceptions =======================================================
class RuntimeException(BrainfuckInterpreterException):
    """ Общее исключение времени выполнения """
    pass


class BadMemoryPointerException(RuntimeException):
    """ Неверный указатель на ячейку памяти """
    pass


class BadCommandPointerException(RuntimeException):
    """ Неверный указатель на шаг программы """
    pass


class BadInputException(RuntimeException):
    """ Некорректный ввод """
    pass
