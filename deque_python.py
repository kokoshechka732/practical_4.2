class Node:
    def __init__(self, number, text):
        self.number = number
        self.text = text
        self.next = None


class DequePython:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def push_front(self, number, text):
        if len(text) > 9:
            text = text[:9]
        
        n = Node(number, text)
        n.next = self.head
        self.head = n
        
        if self.tail is None:
            self.tail = n
        
        self.size += 1
    
    def push_back(self, number, text):
        if len(text) > 9:
            text = text[:9]
        
        n = Node(number, text)
        n.next = None
        
        if self.tail:
            self.tail.next = n
            self.tail = n
        else:
            self.head = self.tail = n
        
        self.size += 1
    
    def pop_front(self):
        if self.head is None:
            return False
        
        temp = self.head
        self.head = self.head.next
        del temp
        
        if self.head is None:
            self.tail = None
        
        self.size -= 1
        return True
    
    def pop_back(self):
        if self.head is None:
            return False
        
        if self.head == self.tail:
            del self.head
            self.head = self.tail = None
            self.size -= 1
            return True
        
        current = self.head
        while current.next != self.tail:
            current = current.next
        
        del self.tail
        self.tail = current
        self.tail.next = None
        self.size -= 1
        return True
    
    def get_size(self):
        return self.size
    
    def is_empty(self):
        return self.head is None
    
    def to_string(self):
        result = ""
        current = self.head
        index = 0
        
        while current:
            result += f"[{index}] ({current.number}, '{current.text}')\n"
            current = current.next
            index += 1
        
        return result
    
    def clear(self):
        while self.head:
            self.pop_front()