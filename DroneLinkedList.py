# drone_linked_list.py

class DroneNode:
    def __init__(self, drone):
        self.drone = drone
        self.next = None
        self.prev = None

class DroneLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def append(self, drone):
        new_node = DroneNode(drone)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def delete(self, node):
        if node == self.head and node == self.tail:
            self.head = None
            self.tail = None
            self.current = None
        elif node == self.head:
            self.head = node.next
            self.head.prev = None
        elif node == self.tail:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        if self.current == node:
            self.current = self.current.next if self.current.next else self.head

        self.size -= 1

    def switch_to_next(self):
        if self.current and self.current.next:
            self.current = self.current.next
        elif self.current:
            self.current = self.head

    def switch_to_previous(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        elif self.current:
            self.current = self.tail

    def get_current_drone(self):
        return self.current.drone if self.current else None

    def __len__(self):
        return self.size

    def __iter__(self):
        self._iter_node = self.head
        return self

    def __next__(self):
        if self._iter_node:
            drone = self._iter_node.drone
            self._iter_node = self._iter_node.next
            return drone
        else:
            raise StopIteration
