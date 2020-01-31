import cv2

video = cv2.VideoCapture(0)

print(video)

check, frame = video.read()

print(check)
print(frame)

video.release()