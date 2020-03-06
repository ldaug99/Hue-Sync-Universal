from threading import Thread
import time
import cv2
import numpy

class camThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__doRun = True # Kill thread when false
        self.__webcam = cv2.VideoCapture(0)
        self.__sleepTime = 0.1 # Time to sleep between each picture
        self.ct = None
 
    def run(self):
        while self.__doRun:
            self.__snapPicture()
            self.__getAverage()
            self.__sleep()
        self.__webcam.release()
        cv2.destroyAllWindows()

    def stop(self):
        print("Stopping {}".format(self.getName()))
        self.__doRun = False

    def setFs(self, fs):
        self.__sleepTime = 1 / fs

    def __sleep(self):
        #print('%s sleeping for %d seconds...' % (self.getName(), self.__sleepTime))
        time.sleep(self.__sleepTime)

    def __snapPicture(self):
        if self.__webcam != None:
            self.__check, self.__frame = self.__webcam.read()
            #print(self.__check) #prints true as long as the webcam is running
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
            if self.ct != None:
                self.ct.stop()
            avg_color_per_row = numpy.average(self.__frame, axis=0)
            avg_color = numpy.average(avg_color_per_row, axis=0)
            r = avg_color[0]
            g = avg_color[1]
            b = avg_color[2]
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
