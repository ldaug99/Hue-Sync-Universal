from threading import Thread
import matplotlib.pyplot as plt

class colorThread(Thread):
    def __init__(self, r, g, b):
        Thread.__init__(self)
        self.r = r; self.g = g; self.b = b
        self.__doRun = True # Kill thread when false
    
    def run(self):
        plt.imshow([[(self.r, self.g, self.b)]])
        plt.show()
        while self.__doRun:
            pass

    def stop(self):
        self.__doRun = False