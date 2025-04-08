class Stack:
    def __init__(self):
        self.collection = []
    
    def push(self, item):
        self.collection.append(item)

    def pop(self):
        if not self.collection:
            raise IndexError("Cannot pop from empty stack")
        return self.collection.pop()
    
    def count(self):
        return len(self.collection)