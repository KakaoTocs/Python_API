import threading
from time import sleep, ctime

loops = [8, 2]

class MyThread(threading.Thread):
    def __init__(self, func, args, name=""):
        threading.Thread.__init__(self, name=name)
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

def loop(nloop, nsec):
    print("start loop", nloop, "at: ", ctime())
    sleep(nsec)
    print("loop", nloop, "at: ", ctime())

def test():
    print("starting at: ", ctime())
    threads =[]
    nloops = range(len(loops))

    for i in nloops:
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print("all Done at:", ctime())

if __name__ == "__main__":
    test()
