#import threading
import heapq

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []
        #self.__atomicLock = threading.Lock()

    def push(self,item):
        "Push 'item' onto the stack"
        #self.__atomicLock.acquire()
        self.list.append(item)
        #self.__atomicLock.release()

    def pop(self):
        "Pop the most recently pushed item from the stack"
        #self.__atomicLock.acquire()
        return self.list.pop()
        #self.__atomicLock.release()

    def isEmpty(self):
        "Returns true if the stack is empty"
        #self.__atomicLock.acquire()
        return len(self.list) == 0
        #self.__atomicLock.release()

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []
        self.__atomicLock = threading.Lock()

    def push(self,item):
        "Enqueue the 'item' into the queue"
        #self.__atomicLock.acquire()
        self.list.insert(0,item)
        #self.__atomicLock.release()

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        #self.__atomicLock.acquire()
        ret =self.list.pop()
        #self.__atomicLock.release()
        return ret


    def isEmpty(self):
        "Returns true if the queue is empty"
        #self.__atomicLock.acquire()
        ret = len(self.list) == 0
        #self.__atomicLock.release()
        return ret

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        #self.__atomicLock = threading.Lock()
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        #self.__atomicLock.acquire()
        heapq.heappush(self.heap, entry)
        #self.__atomicLock.release()
        self.count += 1

    def pop(self):
        #self.__atomicLock.acquire()
        (_, _, item) = heapq.heappop(self.heap)
        #self.__atomicLock.release()
        return item

    def peak(self):
        #self.__atomicLock.acquire()
        ret = self.heap[0]
        #self.__atomicLock.release()
        return ret

    def isEmpty(self):
        #self.__atomicLock.acquire()
        ret = len(self.heap) == 0
        #self.__atomicLock.release()
        return ret

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        #self.__atomicLock.acquire()
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
        #self.__atomicLock.release()

class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))
'''        
class Threader:
    pass

class SubThread(threading.Thread):
    def __init__(self, tid):
        threading.Thread.__init__(self)
        self.ID = tid
        self.func = None
        self.haltingLock = threading.Lock()
        self.__threadLock = threading.Lock()
    def run(self):
        while True:
            self.haltingLock.acquire()
            self.__threadLock.acquire()
            if self.func is not None:
                func = self.func
                
            self.haltingLock.release()
'''