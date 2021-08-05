import numpy as np
from PIL import Image

im = np.array(Image.open('early-snow.png').convert('RGBA').rotate(90, expand=1))


minLength = 15

#Sorts based on red channel only. Shockingly good
def sortDefault(pixel):
    return pixel
    

#Listing of sorting methods
SORTMETHODS = {

    "DEFAULT" : sortDefault

}


def sortIntervals(inputImage,inputIntervals,method):

    print("beginning sorting....")
    #Create Parsed version of image for determination of sorting 
    parsedImage = inputImage.copy(order='K')

    for line in parsedImage:
        for pixel in line:
            #Parse each pixel based on chosen method
            pixel = SORTMETHODS[method](pixel)

    for i, intLine in enumerate(inputIntervals):
        #For every line, sort the intervals previously decided upon
        for j, interval in enumerate(intLine):
            sort = np.argsort(parsedImage[i, interval[0]:interval[1]], axis=0)
            inputImage[i, interval[0]:interval[1]] = np.take_along_axis(inputImage[i, interval[0]:interval[1]], sort, 0)



#Finds intervals based on channel diff w/ minimum size
def intervalMinSize(input):

    allIntervals = []
    

    for i, line in enumerate(input):
        currentInterval = [0,0]
        allIntervals.append([])        
        
        print("finding intervals on line" + str(i))
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


###Selects and executes interval method
def findIntervals(input, method):

    print("finding intervals...")
    output = INTERVALMETHODS[method](input)
    return output

  
######BEGIN MAIN FUNCTION######
intervals = findIntervals(im,"MINSIZE")
sortIntervals(im, intervals, "DEFAULT")

#Write to output
Image.fromarray(im).rotate(270, expand=1).save('early-snow-tim.png')
