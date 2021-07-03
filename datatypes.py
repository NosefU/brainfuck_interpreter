from typing import Union

from exceptions import BadCommandPointerException, BadMemoryPointerException


class Byte:
    """
    Беззнаковый байт.
    Увеличкение и уменьшение значения происходит по модулю 256
    """
    def __init__(self, value=0):
        self._value: int = int(value) % 256

    def __int__(self):
        return self._value

    def __repr__(self):
        return f"b'{self._value}'"

    def __str__(self):
        """ Возвращает символ, соответствующий номеру в 8-bit ASCII """
        return bytes([self._value, ]).decode('Latin-1')


class MemoryRepository:
    """
    Память интерпретатора.
    Хранит набор ячеек, указатель на текущую ячейку и указатель на текущий шаг программы
    """
    def __init__(self, memsize: int = 30000):
        """
        :param memsize: размер набора ячеек
        """
        self._data_pointer = 0
        self._data = [Byte() for _ in range(memsize)]
        self.runtime_pointer = 0

    @property
    def current_byte(self) -> int:
        """ Возвращает значение ячейки, на которую указывает указатель на текущую ячейку """
        return int(self._data[self._data_pointer])

    @current_byte.setter
    def current_byte(self, value: Union[int, Byte]):
        """ Задаёт значение текущей ячейки """
        self._data[self._data_pointer] = Byte(value)

    @property
    def size(self) -> int:
        """ Возвращает размер набора ячеек """
        return len(self._data)

    @property
    def data_pointer(self) -> int:
        """ Возвращает значение указателя на текущую ячейку """
        return self._data_pointer

    @data_pointer.setter
    def data_pointer(self, value: int):
        """ Задаёт значение указателя на текущую ячейку. Проверяет выход за границы набора ячеек """
        if not 0 <= value < len(self._data):
            raise BadMemoryPointerException(f'Bad memory pointer value: {value}')
        self._data_pointer = value

    def __repr__(self):
        return f'Memory (Runtime pointer: {self.runtime_pointer}, ' \
               f'Data pointer: {self._data_pointer}, ' \
               f'Data: {self._data})'


class InputRepository:
    """
    Входные дaнные для программы.
    Хранит текст программы и пользовательский ввод
    """
    def __init__(self, program: str, input_str: str = ''):
        self._program = program + '0'  # 0 является внутренней командой на корректное завершение программы
        self._input_str = list(input_str)
        self._current_step = 0

    def get_command(self, pointer: int) -> str:
        """
        Возвращает команду по номеру шага
        :param pointer: номер шага программы
        """
        if not 0 <= pointer < len(self._program):
            raise BadCommandPointerException(f'Bad command pointer value: {pointer}')
        return self._program[pointer]

    @property
    def program_length(self) -> int:
        """ Возвращает длину введённой программы """
        return len(self._program) - 1

    @property
    def input_char(self) -> str:
        """ Возвращает следующий символ ввода, удаляя его из исходной строки """
        if self._input_str:
            result = self._input_str.pop(0)
        else:
            result = ''
        return result

    def __repr__(self):
        current_input = ''.join(self._input_str)
        return f'Input (Program: {self._program}, Input: {current_input})'


