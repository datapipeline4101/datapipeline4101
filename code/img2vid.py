import imp
import cv2
import re
import os
import glob
#import natsort

image_folder = 'E:/tmp/'
video_name = 'video_movement_light.avi'
files = (os.listdir(image_folder))
print(files)
files = sorted(files,key=lambda x: int(os.path.splitext(x)[0]))
print(files)

images = [img for img in files if img.endswith(".jpg")]
images = images[0:190]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 24, (width,height))
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()