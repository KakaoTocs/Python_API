import threading
from time import sleep, ctime

threadParams = [2, 2, 2, 2, 2]

class AvILoSThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self, name=name)
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

def threadTask(nloop, nsec):
    print("Thread job start", nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'at:', ctime())

def threadingTest():
    print('First start time: ' + ctime())
    threads = []

    nloops = range(len(threadParams))

    for i in nloops:
        t = AvILoSThread(threadTask, (i, threadParams[i]), threadTask.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    print("Main finish: " + ctime())

if __name__ == '__main__':
    threadingTest()
