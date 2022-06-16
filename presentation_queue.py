class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.previous = None


class DoubleLinkedList:
    """
    Create instanced DLL, to be used for presentation data encapsulation.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def __repr__(self):
        string = ''

        if self.head is None:
            string += 'Empty'
            return string

        string += f'Double Linked List:\n{self.head.data}'
        start = self.head.next
        while start is not None:
            string += f' <--> {start.data}'
            start = start.next
        return string

    def append(self, data):
        if self.head is None:
            self.head = Node(data)
            self.tail = self.head
            self.count += 1
            return

        self.tail.next = Node(data)
        self.tail.next.previous = self.tail
        self.tail = self.tail.next
        self.count += 1

    def insert(self, data, index):
        if index > self.count or index < 0:
            raise ValueError('Out of Ranged')

        if index == self.count:
            self.append(data)

        if index == 0:
            self.head.previous = Node(data)
            self.head.previous.next = self.head
            self.head = self.head.previous
            self.count += 1
            return

        start = self.head

        for _ in range(index):
            start = start.next

        start.previous.next = Node(data)
        start.previous.next.previous = start.previous.next
        start.previous.next.next = start
        start.previous = start.previous.next
        self.count += 1
        return

    def get(self, index):
        if index > self.count or index < 0:
            raise ValueError('Out of Range')

        start = self.head

        if index == 0:
            return start

        for _ in range(index):
            start = start.next

        return start

    def remove(self, index):
        if index > self.count or index < 0:
            raise ValueError('Out of Ranged')

        if index == 0:
            self.head = self.head.next
            self.head.previous = None
            self.count -= 1
            return

        if index == self.count - 1:
            self.tail = self.tail.previous
            self.tail.next = None
            self.count -= 1
            return

        start = self.head

        for _ in range(index):
            start = start.next

        start.previous.next = start.next
        start.next.previous = start.previous
        self.count -= 1

    def index(self, data):
        start = self.head
        for i in range(self.count):
            if start.data == data:
                return i
            start = start.next
        return None

    def size(self):
        return self.count

    def display(self):
        print(self)
