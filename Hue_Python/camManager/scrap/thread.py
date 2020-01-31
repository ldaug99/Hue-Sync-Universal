from threading import Thread
from random import randint
import time

class MyThread(Thread):
    def __init__(self):
        ''' Constructor. '''
 
        Thread.__init__(self)
        self.doRun = True
 
 
    def run(self):
        while self.doRun:
            # Sleep for random time between 1 ~ 3 second
            secondsToSleep = randint(1, 5)
            print('%s sleeping for %d seconds...' % (self.getName(), secondsToSleep))
            time.sleep(secondsToSleep)

    def stop(self):
        print("Stopping {}".format(self.getName()))
        self.doRun = False


# Run following code when the program starts
if __name__ == '__main__':
   # Declare objects of MyThread class
   myThreadOb1 = MyThread()
   myThreadOb1.setName('Thread 1')

   # Start running the threads!
   myThreadOb1.start()
 
   input("Press key to stop thread...")
   myThreadOb1.stop()
   # Wait for the threads to finish...
   myThreadOb1.join()
 
   print('Main Terminating...')