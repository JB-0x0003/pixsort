import numpy as np
from PIL import Image

im = np.array(Image.open('early-snow.png').convert('RGBA').rotate(90, expand=1))


minLength = 15

def sortInterval(input,begin,end):

    interval = np.empty((end-begin, 4))
    #print('begining interval from ', begin, ' to ', end)

    for i, pixel in enumerate(input):
        if i == end:
            break
        if i >= begin:
            interval[i-begin] = pixel
        

    interval.sort(0)

    for i, pixel in enumerate(interval):
        input[begin+i] = pixel
    


for i, line in enumerate(im):

    #begin interval at the start of the line
    intervalStart = 0
    print('starting line: ' + str(i))

    for j, pixel in enumerate(line):
        #compare current pixel to the pixel at start of interval
        if abs(line[intervalStart] - pixel)[3] > 10 or abs(line[intervalStart] - pixel)[0] > 90:
            
            #Only sorts if length more than minLength; always resets new interval location
            #This ensures low contrast areas stay readable
            if j - intervalStart > minLength:
                sortInterval(line, intervalStart, j)
            intervalStart = j + 1
    
    #Sort the last interval once the line is over
    if intervalStart < line.shape[0]:
        sortInterval(line, intervalStart, line.shape[0] -1)

    
Image.fromarray(im).rotate(270, expand=1).save('early-snow-tim.png')
