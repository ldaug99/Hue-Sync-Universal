import cv2
import numpy

class camManager():
    ### Static class variables ###
    KWARG_VERBOSE = "verbose"

    # Initialization
    def __init__(self, index = 0, **kwargs):
        # Get variables
        self.__verbose = kwargs.get(camManager.KWARG_VERBOSE, False)
        # Define instance varaibles
        self.__webcam = cv2.VideoCapture(index) # Get camera
        self.__showFrame = False

    def isReady(self):
        check, frame = self.__webcam.read()
        return self.__webcam.isOpened() and check

    def retryOpen(self, index = 0):
        if self.__webcam.isOpened():
            self.__webcam.release()
        return self.__webcam.open(index)

    def release(self):
        self.__webcam.release()
        cv2.destroyAllWindows()
        cv2.waitKey(0)
        cv2.waitKey(0) 
        cv2.waitKey(0) 
        cv2.waitKey(0) 
        cv2.waitKey(0)  
    
    def showFrame(self, state):
        self.__showFrame = state
        if not self.__showFrame:
             cv2.destroyAllWindows()
             cv2.waitKey(0) 
             cv2.waitKey(0) 
             cv2.waitKey(0) 
             cv2.waitKey(0) 
             cv2.waitKey(0) 

    def getFrame(self):
        if self.__webcam.isOpened():
            check, frame = self.__webcam.read()
            if check:
                if self.__showFrame:
                    cv2.imshow("Picture", frame)
                    cv2.waitKey(1)
                return check, frame
            else:
                print("Exception on camManager() -> getFrame(): Unable to get picture from webcam.")
                return False, None
        else:
            print("Exception on camManager() -> getFrame(): Unable to communication with webcam.")
            return False, None

    def getAvgColor(self):
        check, frame = self.getFrame()
        if check:
            avg_color_per_row = numpy.average(frame, axis=0)
            avg_color = numpy.average(avg_color_per_row, axis=0)
            b = avg_color[0]
            g = avg_color[1]
            r = avg_color[2]
            if self.__verbose:
                print("Average color is [{} {} {}] (R, G, B)".format(r, g, b))
            return r, g, b
        else:
            print("Exception on camManager() -> getAvgColor(): Unable to get color from None frame.")
            return None, None, None

    def getDomColor(self):
        check, frame = self.getFrame()
        if check:
            pixels = numpy.float32(self.__frame.reshape(-1, 3))
            n_colors = 5
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
            flags = cv2.KMEANS_RANDOM_CENTERS
            _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
            _, counts = numpy.unique(labels, return_counts=True)
            dominant = palette[numpy.argmax(counts)]
            r = dominant[0]
            g = dominant[1]
            b = dominant[2]
            if self.__verbose:
                print("Dominant color is [{} {} {}] (R, G, B)".format(r, g, b))
            return r, g, b
        else:
            print("Exception on camManager() -> getDomColor(): Unable to get color from None frame.")
            return None, None, None