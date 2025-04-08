from Interfaces.Behavior import Behavior
from Core.TaskStackMachine import *

class Parallel(Behavior):
    def __init__(self, ParallelActions, blackboard):
        super.__init__(blackboard)
        self.trees = []
        for action in ParallelActions:
            tree = TaskStackMachine(None)
            tree.addBehavior(action)
            self.trees.append(tree)

    def CheckRequirement(self):
        raise NotImplementedError()
    
    def Step(self, memory, blackboard, message):
        for tree in self.trees:
            tree.blackboard = blackboard
            result = tree.drive()
            if result != Status.RUNNING:
                memory.push(self)
                return result
    
        memory.push(self)
        return Status.RUNNING