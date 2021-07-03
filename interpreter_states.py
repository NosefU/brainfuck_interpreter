from abc import ABC, abstractmethod

from datatypes import MemoryRepository, InputRepository
from exceptions import UnmatchedClosingBracketException, UnmatchedOpeningBracketException, BadInputException


class AbstractInterpreterState(ABC):

    @staticmethod
    @abstractmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        pass


class IncrementDataPointer(AbstractInterpreterState):
    """
    >
    Переместить указатель на текущую ячейку на шаг вправо
    """
    @staticmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        memory.data_pointer += 1
        memory.runtime_pointer += 1


class DecrementDataPointer(AbstractInterpreterState):
    """
    <
    Переместить указатель на текущую ячейку на шаг влево
    """
    @staticmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        memory.data_pointer -= 1
        memory.runtime_pointer += 1


class IncrementCurrentByte(AbstractInterpreterState):
    """
    +
    Увеличить значение текущей ячейки на 1
    """
    @staticmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        memory.current_byte += 1
        memory.runtime_pointer += 1


class DecrementCurrentByte(AbstractInterpreterState):
    """
    -
    Уменьшить значение текущей ячейки на 1
    """
    @staticmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        memory.current_byte -= 1
        memory.runtime_pointer += 1


class OutputCurrentByte(AbstractInterpreterState):
    """
    .
    Вывести символ, соответствующий значению ячейки в 8-bit ASCII
    """
    @staticmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        print(chr(memory.current_byte), end='')
        memory.runtime_pointer += 1


class StoreInputByte(AbstractInterpreterState):
    """
    ,
    Записать в текущую ячейку памяти ASCII-код введённого символа
    """
    @staticmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        char = input_data.input_char
        if char:
            char_code = ord(char)
            if not 0 <= char_code < 256:
                raise BadInputException(f'Bad input character. '
                                        f'Character ascii code must be between 0 and 255 inclusive. '
                                        f'Character: {char}, code: {char_code}')
            memory.current_byte = ord(char)
        memory.runtime_pointer += 1


class LoopStart(AbstractInterpreterState):
    """
    [
    Начало цикла.
    Если значение текущей ячейки равно нулю, то переводит указатель на текущий шаг
    вперёд по тексту программы на ячейку, следующую за соответствующей ] (с учётом вложенности)
    """
    @staticmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        if memory.current_byte != 0:
            memory.runtime_pointer += 1
            return
        brackets = 0
        for temp_pointer in range(memory.runtime_pointer + 1, input_data.program_length):
            command = input_data.get_command(temp_pointer)
            if command == '[':
                brackets += 1
            elif command == ']':
                if brackets == 0:
                    memory.runtime_pointer = temp_pointer + 1
                    return
                else:
                    brackets -= 1
        raise UnmatchedClosingBracketException(f'Syntax error: No closing bracket. '
                                               f'Last command number: {input_data.get_command(memory.runtime_pointer)}')


class LoopEnd(AbstractInterpreterState):
    """
    ]
    Конец цикла.
    Возвращает указатель на текущий шаг
    назад по тексту программы на ячейку с командой [ (с учётом вложенности)
    """
    @staticmethod
    def handle_command(input_data: InputRepository, memory: MemoryRepository) -> None:
        brackets = 0
        for temp_pointer in range(memory.runtime_pointer - 1, -1, -1):
            command = input_data.get_command(temp_pointer)
            if command == ']':
                brackets += 1
            elif command == '[':
                if brackets == 0:
                    memory.runtime_pointer = temp_pointer
                    return
                else:
                    brackets -= 1
        raise UnmatchedOpeningBracketException(f'Syntax error: No opening bracket. '
                                               f'Last command number: {input_data.get_command(memory.runtime_pointer)}')


# список соответствия команды и обработчика
command_translations = {
    '>': IncrementDataPointer,
    '<': DecrementDataPointer,
    '+': IncrementCurrentByte,
    '-': DecrementCurrentByte,
    '.': OutputCurrentByte,
    ',': StoreInputByte,
    '[': LoopStart,
    ']': LoopEnd
}
