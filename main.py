import numpy as np
from PIL import Image

im = np.array(Image.open('early-snow.png').convert('RGBA').rotate(90, expand=1))


minLength = 15

def sortIntervals(input,intervals):

    output = np.empty(im.shape)

    for i, inLine in enumerate(intervals):
        outLine = []
        


#Implementations of interval selection methods
def intervalMinSize(input):

    allIntervals = []
    

    for i, line in enumerate(input):
        currentInterval = [0,0]
        allIntervals.append([])        
        
        for currentInterval[1], pixel in enumerate(line):
               #compare current pixel to the pixel at the start of the interval
               if abs(line[currentInterval[0]] - pixel)[3] > 10 or abs(line[currentInterval[0]] - pixel)[0] > 90:
                    
                    #print([currentInterval[0],currentInterval[1]])
                    #only adds to list if the length is more than minLength; always resets new interval location
                    #Ensures high contrast areas stay readable
                    if currentInterval[1] - currentInterval[0] > minLength:
                        
                        #print("added")
                        allIntervals[i].append(currentInterval[:])
                    currentInterval[0] = currentInterval[1] + 1
         
        if currentInterval[0] < line.shape[0]:
            
            allIntervals[i].append(currentInterval)
        
        #print(allIntervals)
        #break
    

    return allIntervals


#List of interval selection methods
INTERVALMETHODS = {
    "MINSIZE" : intervalMinSize
}


###Finds list of intervals to be sorted
def findIntervals(input, method):

    intervalMinSize(input)

def   


######BEGIN MAIN FUNCTION######
intervals = findIntervals(im,"MINSIZE")


#for i, line in enumerate(im):
#
#    #begin interval at the start of the line
#    intervalStart = 0
#    print('starting line: ' + str(i))#
#
#    for j, pixel in enumerate(line):
#        #compare current pixel to the pixel at start of interval
#        if abs(line[intervalStart] - pixel)[3] > 10 or abs(line[intervalStart] - pixel)[0] > 90:
#            
#            #Only sorts if length more than minLength; always resets new interval location
#            #This ensures low contrast areas stay readable
#            if j - intervalStart > minLength:
#                sortInterval(line, intervalStart, j)
#            intervalStart = j + 1
#    
#    #Sort the last interval once the line is over
#    if intervalStart < line.shape[0]:
#        sortInterval(line, intervalStart, line.shape[0] -1)

#Write to output
Image.fromarray(im).rotate(270, expand=1).save('early-snow-tim.png')
