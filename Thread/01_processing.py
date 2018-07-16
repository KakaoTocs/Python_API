from multiprocessing import Process, Queue
from concurrent.ProcessProducer import *
import Process

signal_exit = 0

def processConsumer(procQueue):
    try:
        print("[processConsumer] Processing Start")
        while True:
            data = procQueue.get()
            print("[processConsumer] Data Received: {}".format(data))

            if signal_exit == 1:
                print("application::processConsumer is finishing!")
                break

    except Exception as e:
        print("application::processConsumer Exception: {}".format(e))
    finally:
        print("application::processConsumer is finished!")

    procQueue.close()

if __name__ == '__main__':
    try:
        procQueue = Queue()
        procPrducer = ProcessProducer(procQueue)

        procConsumer = Process(target=processConsumer, args=(procQueue, ), name="ProcessConsumer")

        procPrducer.start()
        procConsumer.start()
        print("[ProcessProducer] [1] PID: {} | [2] ProcessName: {}".format(procPrducer.pid, procPrducer.name))
        print("[ProcessConsumer] [1] PID: {} | [2] ProcessName: {}".format(procConsumer.pid, procConsumer.name))
        print("[MainProgram] [1] PID: {} | [2] ProgramPath: {}".format(os.getpid(), os.path.realpath(__file__)))

        procPrducer.join()
        procConsumer.join()

    except Exception as e:
        print("Exception: " + str(e))

    finally:
        print("[Application Exit] Application::finally")

        print("ProcessCheck -> [procPrducer]: {} | [procConsumer]: {}".format(procPrducer.is_alive(), procConsumer.is_alive()))
        procQueue.close()
        signal_exit = 1

        procPrducer.terminate()
        procConsumer.terminate()


from multiprocessing import Process, Lock

class ProcessProducer(Process):
    def __init__(self, procQueue):
        Process.__init__(self, name="ProcessProducer")
        self.procQueue = procQueue
        print("[ProcessProducer] __init__ command")

    def __del__(self):
        print("[ProcessProducer] __del__ command")
        self.procQueue.close()

    def run(self):
        print("[ProcessProducer] Run")
        for i in range(10):
            self.procQueue.put(i)
            print("[ProcessProducer] {} produced".format(i))
