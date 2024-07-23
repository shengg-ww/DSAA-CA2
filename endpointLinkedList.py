class Node:
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, name, endpoint):
        new_node = Node(name, endpoint)
        new_node.next = self.head
        self.head = new_node

    def delete(self, name):
        current = self.head
        prev = None

        while current:
            if current.name == name:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return current.endpoint
            prev = current
            current = current.next
        return None

    def find(self, name):
        current = self.head
        while current:
            if current.name == name:
                return current.endpoint
            current = current.next
        return None
