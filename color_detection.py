import cv2
import numpy as np
import pandas as pd
import urllib.request
import sys
import PySimpleGUI as sg

# accepts input, converts to array, and reads image
url = input("What image would you like to detect colors on? \n")
url_response = urllib.request.urlopen(url)
img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
img = cv2.imdecode(img_array, -1)

# declaring global variables (are used later on)
r = g = b = xpos = ypos = 0
mode = False

# reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# function to get x,y coordinates of mouse position
def draw_function(event, x, y, flags, param):
    try:
        if event == cv2.EVENT_MOUSEMOVE:
            global b, g, r, xpos, ypos, mode
            mode = True
            xpos = x
            ypos = y
            b,g,r = img[y,x]
            b = int(b)
            g = int(g)
            r = int(r)
    except ValueError:
        # If value of color is not found it will give error message
        for _ in range(1):
            sg.Popup("This doesn't work")
            sys.exit('This picture does not work. Try another')

# conserves aspect ratio of the image
scale_percent = 60 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

# resizes the image to fit the screen
cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', draw_function)

# displays the image and UI
while(1):
    cv2.imshow("image", img)

    if mode == True:

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if (r + g + b >= 600):
            cv2.putText(img, text,(50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    # break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()
