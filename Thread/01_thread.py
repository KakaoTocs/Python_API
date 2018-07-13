import threading
from time import ctime

def threadTask(low, high):
    total = 0
    for i in range(low, high):
        total += i
    print("Sub Thread: " + str(total))
    print("Sub Thread END: " + ctime())

if __name__ == '__main__':
    t = threading.Thread(target=threadTask, args=(1, 1999999))
#    t.daemon = True
    t.start()

    print("Main Thread Finish")
    print("Main Thread END: " + ctime())
