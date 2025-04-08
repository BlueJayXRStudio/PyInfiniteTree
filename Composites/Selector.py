from Interfaces.Behavior import Behavior
from queue import Queue
from Core.TaskStackMachine import Status

class Selector(Behavior):
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

        if message == Status.SUCCESS:
            self.finished = True
            return Status.SUCCESS
        
        if self.actions.qsize() == 0:
            self.finished = True
            return Status.FAILURE
        
        nextAction = self.actions.get()
        self.prevActions.append(nextAction)
        memory.push(nextAction)
        return Status.RUNNING
    
    def CheckRequirement(self):
        for i in range(len(self.prevActions)-int(not self.finished)):
            result = self.prevActions[i].CheckRequirement()
            if result != Status.FAILURE:
                return Status.SUCCESS
            
        if not self.finished:
            return Status.RUNNING
        return Status.FAILURE
    