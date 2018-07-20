import threading

class Messenger(threading.Thread):
    def run(self):
        for _ in range(10):
            print(threading.currentThread().getName())

x = Messenger(name="메세지를 보냄")
y = Messenger(name="메세지를 받음")

x.start()
y.start()
