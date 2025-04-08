from Interfaces.Behavior import Behavior
from queue import Queue
from Core.TaskStackMachine import Status

class Sequence(Behavior):
    def __init__(self, toPopulate, blackboard):
        super.__init__(blackboard)

        if toPopulate == None:
            return
        
        self.finished = False
        self.actions = Queue() # Behavior/Task Queue
        self.prevActions = [] # Behavior/Task List
        
        for action in toPopulate:
            self.actions.put(action)

    def Step(self, memory, blackboard, message) -> Status:
        memory.push(self)

        if message == Status.FAILURE:
            self.finished = True
            return Status.FAILURE
        
        if self.actions.qsize() == 0:
            self.finished = True
            return Status.SUCCESS
        
        nextAction = self.actions.get()
        self.prevActions.append(nextAction)
        memory.push(nextAction)
        return Status.RUNNING
    
    def CheckRequirement(self):
        if self.finished:
            return Status.FAILURE
        
        for i in range(len(self.prevActions)-1):
            result = self.prevActions[i].CheckRequirement()
            if result != Status.SUCCESS:
                return Status.FAILURE
        
        return Status.RUNNING
    