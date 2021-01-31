# manages and organzies all the threads assigned to processes by the assistant
# all threads of a particular type are stored in stacks so that the user
# can close the most recent instance of a process, I'm really over engineering
# this as I doubt users will have more than one of a particular task open
# at a time, but just incase :P
import threading
import time
from collections import deque

class PManager:
    def __init__(self):
        self.processes = {}

    # adds a process of a given type(name) to the top of the process stack
    # for its given type (explain better)
    def add(self, name, process, flags):
        if(self.processes.get(name)==None):
            self.processes[name] = deque()
        thread = thread_with_flag(process, flags)
        print('starting process')
        thread.start()
        self.processes[name].append(thread)
    
    # adds a process of a given type to the bottom of the process stack
    # for its given type
    def addBottom(self, name, process, flags):
        if(self.processes.get(name)==None):
            self.processes[name] = deque()
        thread = thread_with_flag(process, flags)
        thread.start()
        self.processes[name].appendleft(thread)

    # removes the top process in the stack for the give process name.
    # returns False if their are no processes of that name,
    # and True if the top process in the stack was properly removed.
    def remove(self, name):
        if self.processes.get(name)==None:
            return False
        toRemove = self.processes[name].pop()
        toRemove.kill()
        if(len(self.processes[name])==0):
            del self.processes[name]
        return True
    
    # removes the nth process in the given process stack
    # returns True if the process was removed
    # returns False if n was to large or name was not found
    def removeN(self, name, n):
        if self.processes.get(name)==None or len(self.processes[name]) < n:
            return False
        tempStack = deque()
        for i in range(n-1):
            tempStack.append(self.processes[name].pop())
        toRemove = self.processes[name].pop()
        toRemove.kill()
        for i in range(n-1):
            self.processes[name].append(tempStack.pop())
        return True

    # removes a process 
    def removeId(self, name, id):
        print('to do')

    def getProcess(self, name):
        if self.processes.get(name) != None and len(self.processes[name]) > 0:
            temp = self.processes.get(name).pop()
            self.processes.get(name).append(temp)
            return temp
        return False

# class to manage killing threads using a pass by reference flag that can
# be changed to end the function. For this to work there must be proper
# flag logic in the passed function itself.
class thread_with_flag:
    def __init__(self, func, flags = [False], id = -1):
        self.func = func
        self.flags = flags
        self.t1 = threading.Thread(target = self.func, args = (self.flags,))
        self.id = id

    # changes the flag to True to tell the function to end its execution
    # as quickly as possible.
    def kill(self):
        print('killing thread')
        self.flags[0] = True
        while(self.t1.is_alive()):
            continue
        self.t1.join()
    
    # starts the execution of the thread's function.
    def start(self):
        self.t1.start()

# example of properly incorporated flag function logic.
# essentially the function needs a parameter for the flag
# and an if statement that will break out of any loops
# in the function. This is because the thread will terminate
# once the function is done executing.
def main1():
    def run(stop):
        while True:
            print('thread running')
            time.sleep(1)
            print(stop[0])
            if stop[0]==True:
                break
        print('thread ending')

    #t1 = threading.Thread(target = run, args=(False,))
    #print('starting thread')
    #t1.start()
    #print('thread has started')

    thread = thread_with_flag(run, [False])
    print('starting thread')
    thread.start()
    print('thread has started')
    time.sleep(5)
    thread.kill()


def main():
    print('----processes manager main----')


if __name__ == '__main__':
    main()
