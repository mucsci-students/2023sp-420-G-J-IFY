###############################################################################
# ObjectPool.py
#
# Authors: Gaige Zakroski
#
# Date Modified: 4-7-23
#
# Creates an object pool of object pools to store our objects
#
###############################################################################

###############################################################################
# class Thead:
#   Helper Class:
#       Creats a single thread of the object pool.
#
# <public> Attributes:
#   field: threadName: str
#   field: obj: object
#
# <public> Functions:
#   __init__(threadName : str) -> None:
#       Creates a thread
#
#   setThreadName(newName : str) -> None:
#       sets the thread name to a new name
#
#   getThreadName(self) -> str:
#       gets the name of a thread and returns it
###############################################################################
class Thread:

    ###########################################################################
    # __init__(self, threadName: str, object: object) -> None:
    #
    # DESCRIPTION:
    #   Initializes a thread object
    # PARAMS:
    #   threadName: str
    #       Name of the thread
    #
    #   obj: object
    #       Object of the thread
    #
    # RETURNS:
    #   None
    ###########################################################################

    def __init__(self, threadName: str, obj: object) -> None:
        self.threadName = threadName
        self.obj = obj

    ###########################################################################
    # setThreadName(self, newName: str) -> None:
    #
    # DESCRIPTION:
    #   Sets the threadName to a given name
    #
    # PARAMS:
    #   newName: str
    #       new name of the Thread
    #
    # RETURNS:
    #   None
    ###########################################################################

    def setThreadName(self, newName: str) -> None:
        self.threadName = newName

    ###########################################################################
    # getThreadName(self) -> str:
    #
    # DESCRIPTION:
    #   gets the threadName and returns it
    #
    # PARAMS:
    #   None
    #
    # RETURNS:
    #   returns threadName: str
    ###########################################################################

    def getThreadName(self) -> str:
        return self.threadName

    ###########################################################################
    # setObject(self, object: object) -> None:
    #
    # DESCRIPTION:
    #   sets the object that represents the Thread
    #
    # PARAMS:
    #   obj: object
    #       The object that represents the Thread
    # RETURNS:
    #   None
    ###########################################################################

    def setObject(self, obj: object) -> None:
        self.obj = obj

    ###########################################################################
    # getObject(self) -> object:
    #
    # DESCRIPTION:
    #   returns the object that represents the Thread
    #
    # PARAMS:
    #  None
    #
    # RETURNS:
    #   obj: object
    #       object that represents the thread
    ###########################################################################
    def getObject(self) -> object:
        return self.obj

###############################################################################
# class Thead:
#   Helper Class:
#       creates the Object pool of threads
#
# <public> Attributes:
#   field: availableThreadList: list[Thread]
#   field: usedThreadList: list[Thread]
#   field: size: int
#   field: maxSize: int
#
# <public> Functions:
#   __init__(threadName : str) -> None:
#       Creates an object pool
#
#   setAvailableThreadList(threadList: list[Thread]) -> None:
#       sets the availableThreadList
#
#   addThread(self, thread: Thread) -> None:
#       add thread to the ThreadPool
#
#   getThread(self, threadName) -> Thread:
#       returns the thread to user
#
#   returnThread(self, thread: Thread) -> None:
#       returns the Thread back to the pool to use
#
#   getSize(self) -> int:
#       returns the size of the object pool
#
#   getAvailableThreadList(self) -> list[str]:
#       returns the list of names that are in the availableThreadList
#
#   getUsedThreadList(self) -> list[str]:
#       returns the list of names that are in the usedThreadList
#
###############################################################################


class ThreadPool:

    ###########################################################################
    # __init__(self, availableThreadList: list[Thread], usedThreadList= [],
    #             size= 0) -> None:
    #
    # DESCRIPTION:
    #   Initializes the ThreadPool object
    #
    # PARAMS:
    #   availableThreadList: list[Thread]
    #       list of the avalible Threads
    #
    #   usedThreadList: list[Thread]
    #       list of the threads currently in use
    #
    #   size: int
    #       the number of Threads that are in the pool
    #
    #   maxSize: int
    #       The maximum size of the pool which is 3
    #
    # RETURNS:
    #   None
    ###########################################################################

    def __init__(self, availableThreadList: list[Thread]) -> None:
        self.availableThreadList = availableThreadList
        self.usedThreadList = []
        self.size = len(availableThreadList)
        self.maxSize = 3

    ###########################################################################
    # setAvailableThreadList(threadList: list[Thread]) -> None:
    #
    # DESCRIPTION:
    #   sets the availbleThreadList to a list of Threads
    #
    # PARAMS:
    #   threadList: list[Thread]
    #
    # RETURNS:
    #   None
    ###########################################################################

    def setAvailableThreadList(self, threadList: list[Thread]) -> None:
        self.availableThreadList = threadList
        self.size = len(threadList)
        self.usedThreadList = []

    ###########################################################################
    # addThread(self, thread: Thread) -> None:
    #
    # DESCRIPTION:
    #   adds a thread to the ThreadPool
    #
    # PARAMS:
    #   thread: Thread
    #       The Thread to be added to the pool
    #
    # RETURNS:
    #   None
    ###########################################################################

    def addThread(self, thread: Thread) -> None:
        if self.size < 3:
            self.availableThreadList.append(thread)
            self.size += 1
        else:
            raise Exception('Pool is full')

    ###########################################################################
    # getThread(self, threadName) -> Thread:
    #
    # DESCRIPTION:
    #   gets a Thread and returns it. Then moves that thread to the
    # usedThreadList
    #
    # PARAMS:
    #   threadName: str
    #       name of the thread
    # RETURNS:
    #   thread: Thread
    #       the thread the user requested
    ###########################################################################

    def getThread(self, threadName) -> Thread:
        if (self.checkAvailableList(threadName) and not
           self.checkUsedList(threadName)):
            for i in self.availableThreadList:
                if i.getThreadName() == threadName:
                    self.availableThreadList.remove(i)
                    self.usedThreadList.append(i)
                    return i
        elif (not self.checkAvailableList(threadName) and
              self.checkUsedList(threadName)):
            raise AttributeError
        else:
            raise AttributeError

    ###########################################################################
    # checkUsedThreadList(self, name) -> bool:
    #
    # DESCRIPTION:
    #   checks if a thread is in the usedThreadList
    #
    # PARAMS:
    #   name: str
    #       name of the thread
    # RETURNS:
    #   bool
    #       true if the thread is in the list false otherwise
    ###########################################################################

    def checkUsedList(self, name) -> bool:
        for i in self.usedThreadList:
            if i.threadName == name:
                return True
        return False

    ###########################################################################
    # checkAvailableList(self, name) -> bool:
    #
    # DESCRIPTION:
    #   checks if a thread is in the availableThreadList
    #
    # PARAMS:
    #   thread: Thread
    #       Thread being returned
    #
    # RETURNS:
    #   bool
    #       true if the thread is in the list false otherwise
    ###########################################################################

    def checkAvailableList(self, name) -> bool:
        for i in self.availableThreadList:
            if i.threadName == name:
                return True
        return False

    ###########################################################################
    # returnThread(self, thread: Thread) -> None:
    #
    # DESCRIPTION:
    #   returns the thread back to the pool to be used again. The thread is
    # then returned back to the availableThreadList
    #
    # PARAMS:
    #   thread: Thread
    #       Thread that is being returned to the Thread Pool
    ###########################################################################

    def returnThread(self, thread: Thread) -> None:
        if thread in self.usedThreadList:
            self.usedThreadList.remove(thread)
            self.availableThreadList.append(thread)
        else:
            raise AttributeError

    ###########################################################################
    # getSize(self) -> int:
    #
    # DESCRIPTION:
    #   gets the size of the pool and returns it
    #
    # PARAMS:
    #   None
    #
    # RETURNS:
    #   size: int
    #       the size of the pool
    #
    ###########################################################################

    def getSize(self) -> int:
        return self.size

    ###########################################################################
    # getAvailableThreadList(self) -> list[str]:
    #
    # DESCRIPTION:
    #   gets the availableThreadList
    #
    # PARAMS:
    #   None
    #
    # RETURNS:
    #   lst: list[str]
    #       list of all the available threads names
    ###########################################################################

    def getAvailableThreadList(self) -> list[str]:
        lst = []
        for i in self.availableThreadList:
            lst.append(i.getThreadName())
        return lst

    ###########################################################################
    # getUsedThreadList(self) -> list[str]:
    #
    # DESCRIPTION:
    #   gets the List of used threads
    #
    # PARAMS:
    #   None
    #
    # RETURNS:
    #   usedThreadList: list[str]
    #       list of all the Threads currently in use
    ###########################################################################

    def getUsedThreadList(self) -> list[str]:
        lst = []
        for i in self.usedThreadList:
            lst.append(i.getThreadName())
        return lst
