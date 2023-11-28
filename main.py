bracket_dict = {
    '(': ')',
    '[': ']',
    '{': '}'
}

balanced_list = [
    '(((([{}]))))',
    '[([])((([[[]]])))]{()}',
    '{{[()]}}'
]

unbalanced_list = [
    '}{}',
    '{{[(])]}}',
    '[[{())}]'
]

class Stack(list):
    def is_empty(self):
        return len(self) == 0

    def push(self, item):
        self.append(item)

    def pop(self):
        if not self.is_empty():
            item = self[-1]
            self.__delitem__(-1)
        return item

    def peek(self):
        if not self.is_empty():
            return self[-1]

    def size(self):
        return len(self)

def checking_balance(check):
    stack = Stack()
    for item in check:
        if item in bracket_dict:
            stack.push(item)
        elif item == bracket_dict.get(stack.peek()):
            stack.pop()
        else:
            return False
    return stack.is_empty()


if __name__ == "__main__":
    for c in balanced_list + unbalanced_list:
        print(f'{c:<30}{checking_balance(c)}')