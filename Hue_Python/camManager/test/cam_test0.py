import cv2
import time
import numpy

def getAverage(channel):
    color_sum = 0
    for i in channel:
        sum2 = 0
        for k in channel[i]:
            sum2 = sum2 + channel[i][k]
        color_sum = color_sum + (sum2 / len(channel[k]))
    color = color_sum / len(channel[i])
    return color

webcam = cv2.VideoCapture(0)

key = cv2.waitKey(1)

time.sleep(1)

test = None

# while True:
#     check, frame = webcam.read()
#     print(check) #prints true as long as the webcam is running
#     print(frame) #prints matrix values of each framecd 
#     key = cv2.waitKey(1)
#     if check:
#         cv2.imshow("Capturing", frame)
#     if key == ord('q'):
#         webcam.release()
#         cv2.destroyAllWindows()
#         break

while True:
    check, frame = webcam.read()
    print(check) #prints true as long as the webcam is running
    #print(frame) #prints matrix values of each framecd 
    key = cv2.waitKey(1)
    if check:
        cv2.imshow("Capturing", frame)
        test = frame

        avg_color_per_row = numpy.average(test, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
        print(avg_color)

        pixels = numpy.float32(test.reshape(-1, 3))

        n_colors = 5
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = numpy.unique(labels, return_counts=True)

        dominant = palette[numpy.argmax(counts)]
        print(dominant)
    if key == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break


# check, frame = webcam.read()
# print(check) #prints true as long as the webcam is running
# #print(frame) #prints matrix values of each framecd 
# cv2.imshow("Capturing", frame)
# webcam.release()
# cv2.destroyAllWindows()

# test = frame

# avg_color_per_row = numpy.average(test, axis=0)
# avg_color = numpy.average(avg_color_per_row, axis=0)
# print(avg_color)

# pixels = numpy.float32(test.reshape(-1, 3))

# n_colors = 5
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
# flags = cv2.KMEANS_RANDOM_CENTERS

# _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
# _, counts = numpy.unique(labels, return_counts=True)

# dominant = palette[numpy.argmax(counts)]
# print(dominant)

#print("Red average is {}".format(avg_red))
#print("Green average is {}".format(avg_green))
#print("Blue average is {}".format(avg_blue))


