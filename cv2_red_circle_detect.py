import numpy as np
import cv2, sys, os
import argparse

# example path
# path = r"C:\Project_Files\Python_Scripts\img_verif_export\red_circles\circles.jpg"


def check_if_image_path_exists(imgPath):
    if os.path.exists(imgPath):
        return True
    else:
        print("Path not found, try again")
        sys.exit()

def main(path):
    # checking if path exits
    check_if_image_path_exists(path)
    # read the image
    img = cv2.imread(path)
    # make a clone
    clone = img.copy()
    # perform median blur
    median = cv2.medianBlur(clone,3)
    # convert bgr to hsv
    hsv_image = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    # identify lower red color hue range
    lower_red_hue_range = cv2.inRange(hsv_image, (0,100,100), (10,255,255))
    # identify upper red color hue range
    upper_red_hue_range = cv2.inRange(hsv_image, (160,100,100), (179,255,255))
    # red hue image
    red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)
    # perform gaussian blue
    red_hue_image = cv2.GaussianBlur(red_hue_image,(9,9),2)
    # detect circles
    circles = cv2.HoughCircles(red_hue_image, cv2.HOUGH_GRADIENT, 3, len(red_hue_image)/8, 100, 20)
    # if circles present draw border
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(clone, (x, y), r, (0, 255, 0), 4)
            # cv2.rectangle(clone, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # displaying output
        cv2.namedWindow("Threshold Lower Image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Threshold Lower Image",lower_red_hue_range)
        cv2.namedWindow("Threshold Upper Image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Threshold Upper Image",upper_red_hue_range)
        cv2.namedWindow("Combined Lower Image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Combined Lower Image",red_hue_image)
        cv2.namedWindow("Detected red circles on the input image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Detected red circles on the input image",clone)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-imgPath", "--foperand", required=True, help="first operand")
    args = vars(ap.parse_args())
    main(args["foperand"])

