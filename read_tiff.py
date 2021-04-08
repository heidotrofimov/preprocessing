import cv2

image = cv2.imread('s1_iq/combined.tif', cv2.IMREAD_UNCHANGED)
#print(image.shape)

channels = cv2.split(image)

print(channels[0])

