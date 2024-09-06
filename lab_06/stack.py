class Stack():
    """Класс для реализации стека."""
    list_stack = list()
    number_stack_elements = 0

    def push(self, element: tuple):
        """Добавляет элемент в стек."""
        self.number_stack_elements += 1
        self.list_stack.append(element)

    def pop(self) -> tuple:
        """Извлекает элемент из стека."""
        element = tuple()

        if self.number_stack_elements != 0:
            element = self.list_stack.pop()

            self.number_stack_elements -= 1

        return element

    def clear(self):
        """Очищает стек."""
        while self.number_stack_elements != 0:
            element = self.pop()