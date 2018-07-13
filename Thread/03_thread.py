import threading

g_count = 0

class MutexThread(threading.Thread):
    def run(self):
        global g_count
        for i in range(20):
            lock.acquire()
            g_count += 1
            lock.release()

if __name__ == '__main__':
    lock = threading.Lock()
    threadArr = []

    for i in range(10):
        thread = MutexThread()
        thread.start()
        threadArr.append(thread)

    for thread in threadArr:
        thread.join()

    print("All threads finished: ", g_count)
