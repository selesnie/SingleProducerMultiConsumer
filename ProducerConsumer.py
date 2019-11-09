from threading import Thread
from threading import Lock
import threading
from queue import Queue

class Producer:
    def __init__(self, q, data):
        self._queue = q
        self._data = data

    def send(self):
        while True:
            for value in self._data:
                self._queue.put(value)
            self._queue.put(None)
            break

class Consumer:
    def __init__(self, q, lock):
        self._queue = q
        self._lock = lock

    def receive(self):
        while True:
            value = self._queue.get()
            with self._lock:
                print('Thread id {} got value {}'.format(threading.get_ident(), value), end='\n')
            if value == None:
                break

if __name__ == '__main__':
    q = Queue(2)
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    producer = Producer(q, values)
    l = Lock()
    c1 = Consumer(q, l)
    c2 = Consumer(q, l)
    producerThread = Thread(target=producer.send)
    c1Thread = Thread(target=c1.receive)
    c2Thread = Thread(target=c2.receive)
    producerThread.start()
    c1Thread.start()
    c2Thread.start()
    producerThread.join()
    c1Thread.join()
    c2Thread.join()
