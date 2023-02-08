import imp
import cv2
import re
import os
#import natsort

image_folder = 'E:/tmp/'
video_name = 'video_earth_rot.avi'
files = (os.listdir(image_folder))
print(files)
files = sorted(files,key=lambda x: int(os.path.splitext(x)[0]))
print(files)

images = [img for img in files if img.endswith(".jpg")]
images = images[0:240]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 24, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()