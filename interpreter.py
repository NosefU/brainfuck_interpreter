from datatypes import MemoryRepository, InputRepository
from interpreter_states import command_translations


class Interpreter:
    """
    Интерпретатор языка Brainfuck.
    На вход принимает объекты входных данных и памяти.
    Выполняет программу, находящуюся в input_data
    """
    def __init__(self, input_data: InputRepository, memory: MemoryRepository) -> None:
        self.memory = memory
        self.input = input_data

    def execute_program(self) -> None:
        """
        Выполняет программу, поданную на вход
        """
        next_command = self.input.get_command(self.memory.runtime_pointer)
        while next_command != '0':
            state = command_translations.get(next_command, None)
            if state:  # проверка на наличие команды. Если такая есть, то выполняем
                state.handle_command(input_data=self.input, memory=self.memory)
            else:  # Если такой нет, то переходим на следующую
                self.memory.runtime_pointer += 1
            next_command = self.input.get_command(self.memory.runtime_pointer)
        print('\nProgram finished')


if __name__ == "__main__":
    program = """,.,.,.,.[-]++++++++[>++++[>++>+++>+++>+<<<<-]>+>->+>>+[<]<-]>>.>>---.+++++++..+++.>.<<-.>.+++.------.--------.>+.>++."""
    input_data = InputRepository(program=program, input_str='123 ')
    memory = MemoryRepository()
    interpreter = Interpreter(input_data, memory)
    interpreter.execute_program()
