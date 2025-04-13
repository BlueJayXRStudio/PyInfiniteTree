from enum import Enum
from .Stack import Stack

class Status(Enum):
    RUNNING = 1
    SUCCESS = 2
    FAILURE = 3

class TaskStackMachine:
    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.memory = Stack()
        self.message = Status.RUNNING
        
    def drive(self) -> Status:
        if self.memory.count() == 0:
            return Status.RUNNING

        SubTask = self.memory.pop()

        if self.message == Status.RUNNING:
            self.message = SubTask.Step(self.memory, self.blackboard, self.message)
            return self.message
        
        if self.memory.count() > 0:
            self.message = self.memory.pop().Step(self.memory, self.blackboard, self.message)
            return self.message

        self.message = Status.RUNNING
        return Status.RUNNING
    
    def addBehavior(self, behavior):
        self.memory.push(behavior)
        self.message = Status.RUNNING
    