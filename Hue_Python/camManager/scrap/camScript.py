import cv2
import time
import numpy

class cam():
    SNAPINTERVAL = 0.01 # Update every 100 milliseconds

    def __init__(self):
        self.__lastUpdate = time.time()
        self.__webcam = cv2.VideoCapture(0)
        # Wait for start
        time.sleep(1)

    def run(self):
        while 1==1:
            self.__timeNow = time.time()
            while (self.__timeNow - self.__lastUpdate) < cam.SNAPINTERVAL:
                pass
                #command = input("Input a command: ")
                #self.__processCommand(command)
            self.__snapPicture()
            self.__lastUpdate = self.__timeNow

            #self.__timeNow = time.time()
            #if (self.__timeNow - self.__lastUpdate) > snapInterval:
            #    self.__snapPicture():
            #else:
            #    command = input("Input a command: ")
            #    self.__processCommand(command)
            #    # Wait for input
            #    self.__waitForCommand()

    def stop(self):
        self.__webcam.release()
        cv2.destroyAllWindows()

    def __waitForCommand(self):
        while 1==1:
            command = input("Input a command: ")
            self.__processCommand(command)

    def __processCommand(self, command):
        switcher = {
            "snap": self.__snapPicture,
            "dom": self.__getDominante,
            "avg": self.__getAverage,
            "stop": self.stop
        }
        function = switcher.get(command, self.__comInvalid)
        function()

    def __snapPicture(self):
        if self.__webcam != None:
            self.__check, self.__frame = self.__webcam.read()
            print(self.__check) #prints true as long as the webcam is running
            #print(frame) #prints matrix values of each framecd 
            if self.__check:
                k = cv2.waitKey(1)
                cv2.imshow("Picture", self.__frame)
            else:
                print("Unable to get picture")
        else:
            print("No communication to webcam")

    def __getAverage(self):
        if self.__check:
            avg_color_per_row = numpy.average(self.__frame, axis=0)
            avg_color = numpy.average(avg_color_per_row, axis=0)
            print(avg_color)

    def __getDominante(self):
        if self.__check:
            pixels = numpy.float32(self.__frame.reshape(-1, 3))
            n_colors = 5
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
            flags = cv2.KMEANS_RANDOM_CENTERS
            _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
            _, counts = numpy.unique(labels, return_counts=True)
            dominant = palette[numpy.argmax(counts)]
            print(dominant)

    def __comInvalid(self):
        print("No")