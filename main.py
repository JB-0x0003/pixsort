import numpy as np
from PIL import Image
import sys
import argparse

#Sorts based on red channel only. Surprisingly good
def sortDefault(input):
    #:gigachad:
    return input

#Sorts based on difference from median pixel
def sortMedian(input):

    dummyImage = input.copy(order='K')

    for line in dummyImage:
        line.sort(axis=0)

    medianX = int(dummyImage.shape[1]/2)

    for i, line in enumerate(input):

        medianPixelR = np.intc(dummyImage[i,medianX,0])

        for pixel in line:
            pixel[0] = abs(medianPixelR - pixel[0])
            pixel[1] = pixel[0]
            pixel[2] = pixel[0]
    return input

#Listing of sorting methods
SORTMETHODS = {

    "DEFAULT" : sortDefault,
    "MEDIAN" : sortMedian

}


def sortIntervals(inputImage,inputIntervals,method):

    print("beginning sorting....")
    #parse the image to generate instruction for sorting
    parsedImage = SORTMETHODS[method](inputImage.copy(order='K'))

    for i, intLine in enumerate(inputIntervals):
        #For every line, sort the intervals previously decided upon
        for j, interval in enumerate(intLine):
            sort = np.argsort(parsedImage[i, interval[0]:interval[1]], axis=0)
            inputImage[i, interval[0]:interval[1]] = np.take_along_axis(inputImage[i, interval[0]:interval[1]], sort, 0)



#Finds intervals based on channel diff w/ minimum size
def intervalDiff(input):

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
    "DIFFERENCE" : intervalDiff
}


###Selects and executes interval method
def findIntervals(input, method):

    print("finding intervals...")
    output = INTERVALMETHODS[method](input)
    return output

  
######BEGIN MAIN FUNCTION######
#Begin parsing argumnets
parser = argparse.ArgumentParser(description="Easily Smear Pixels")
parser.add_argument("image", help="File path of the image to be sorted")
parser.add_argument("-o", "--output", help="File path for output to be saved to")

args = parser.parse_args()
inputPath = args.image
outputPath = args.output

im = np.array(Image.open(inputPath).convert('RGBA').rotate(90, expand=1))

minLength = 5


#intervals = findIntervals(im,"DIFFERENCE")
#sortIntervals(im, intervals, "MEDIAN")

#Determine output path if none available
if outputPath == None:
    outputPath = inputPath
    for i in range(len(outputPath)):
        if outputPath[len(outputPath)-i -1] == '.':
            outputPath = outputPath[0:len(outputPath)- i - 1]
            outputPath += '_sorted.png'
            break


#Write to output
Image.fromarray(im).rotate(270, expand=1).save(outputPath)
