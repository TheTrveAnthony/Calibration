import cv2
import numpy as np
import os
import sys


if len(sys.argv) != 5:
	print("please enter the grid size, the squares size of your board and the number of pics you wanna take for calibration, or you'll see this message for all eternity.\n")
	sys.exit()


gx = int(sys.argv[1])
gy = int(sys.argv[2])
gs = gx * gy
grille = (gx, gy)	# grid size
square = int(sys.argv[3])			# square size

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, square, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((gs,3), np.float32)
objp[:,:2] = np.mgrid[0:gx,0:gy].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap = cv2.VideoCapture(0)
hasFrame, frame = cap.read()

k = 0 		# number of patterns caught
xx = int(sys.argv[4])


print("press the space bar to capture a frame and use it for calibration\n")
while k < xx:
   
    hasFrame, frame = cap.read()

    
    if not hasFrame:
        cv2.waitKey()
        print("Camera failed to start")
        break

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, grille, None)

    if ret == True:
        

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        frame = cv2.drawChessboardCorners(frame, grille, corners2,ret)
		
        if cv2.waitKey(2) == 32:		# Press the space bar to catch a frame and use it for calibration

        	objpoints.append(objp)
        	imgpoints.append(corners2)
        	k += 1
        	print(k)

    cv2.imshow('calib dat shit', frame)
	

cv2.destroyAllWindows()

print("Commencing calibration...\n")

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


camname = input("Done, what's the name of your cam ?\n")
fich = camname + "_calibration.txt"

## Write da results
with open(fich, 'w') as f:
	
	start = "Calabration results of the" + camname + " cam.\n\n"
	f.write(start)

	mx = "Camera matrix : \n\n" + str(mtx) + "\n\n\n\n"
	f.write(mx)

	disto = "Distortion Coeffs : \n\n" + str(dist) + "\n\n\n\n"
	f.write(disto)
