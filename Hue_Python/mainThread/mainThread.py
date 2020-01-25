from threading import Thread
import time

class mainThread(Thread):
    KWARG_VERBOSE = "verbose"

    def __init__(self, lightMan, apiMan, camMan, **kwargs):
        Thread.__init__(self)
        # Get variables
        self.__verbose = kwargs.get(mainThread.KWARG_VERBOSE, False)
        # Check if managers are given
        self.__doRun = True # Kill thread when false
        self.__sleepTime = 0.1 # Time to sleep between each picture
        self.__initialized = False
        self.__captureColor = False
        try:
            if lightMan.isReady() and apiMan.isReady() and camMan.isReady():
                self.__lm = lightMan
                self.__am = apiMan
                self.__cm = camMan
                self.__initialized = True
        except:
            self.__doRun = False
        if self.__verbose:
            print("{} initialized with run status {}".format(self.getName(), self.__doRun))

    def run(self):
        if self.__initialized:
            while(self.__doRun):
                while(self.__captureColor):
                    self.__updateColor()
        if self.__verbose:
            print("Exiting {}".format(self.getName()))

    def isReady(self):
        return self.__initialized

    def isRunning(self):
        return self.__doRun

    def isCapturing(self):
        return self.__captureColor

    def stop(self):
        if self.__verbose:
            print("Stopping {}".format(self.getName()))
        self.__captureColor = False
        self.__doRun = False

    def startCapture(self):
        self.__captureColor = True

    def stopCapture(self):
        self.__captureColor = False

    def setFs(self, fs):
        self.__sleepTime = 1 / fs

    def __updateColor(self):
        group = "center"
        r, g, b = self.__cm.getAvgColor()
        lights = self.__lm.getLightsInGroup(group)
        for lightID in lights:
            self.__am.setColor(lightID, r, g, b)
        self.__sleep()

    def __sleep(self):
        if self.__verbose:
            print('%s sleeping for %d seconds...' % (self.getName(), self.__sleepTime))
        time.sleep(self.__sleepTime)