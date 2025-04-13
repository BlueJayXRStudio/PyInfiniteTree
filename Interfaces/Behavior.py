from abc import ABC, abstractmethod
from ..Core.TaskStackMachine import Status
from ..Core.Stack import Stack

class Behavior:
    def __init__(self, blackboard):
        # redundant, but there may be cases where we need to internally
        # store blackboard reference
        self.blackboard = blackboard 
        
    @abstractmethod
    def Step(self, memory, blackboard, message) -> Status:
        pass

    @abstractmethod
    def CheckRequirement(self) -> Status:
        pass

    def TraverseRequirements(self, memory) -> Status:
        tempStack = Stack()
        result = Status.RUNNING

        while memory.count() > 0:
            task = memory.pop()
            tempStack.push(task)
            result = task.CheckRequirement()
            if result != Status.RUNNING:
                break

        while tempStack.count() > 0:
            memory.push(tempStack.Pop())

        return result