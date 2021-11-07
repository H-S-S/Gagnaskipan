import googlemaps
import pprint
import time
import urllib.request
import itertools
import os
import _json
#import GUI as gui


"""
Notes:
You have to delete test file if you insert more locations

"""

"""
Plan:
1. Get distanse from A to B then B to A if same dont need to try BA just AB
2. If gone from AB the BC must be next or BG or whatever5
3. make alogithm that goes to all points and tries all combinations 
"""
#import API key from text document
f = open("API.txt", "r")
lines= f.readlines()
API_key = lines[0]
f.close()
gmaps = googlemaps.Client(key=API_key)

#creates matrix with points x points given from the file
file = open("Data\Destinations.txt","r")
numberOfLocations = len(file.readlines())


#The names of whays you can take from one point to another like(Furuhjali-klyfjasel and Furuhjali-Bakkasel and so on)
def create_matrix_of_pair_names(numberOfLocations, pathOfLocations):
    matrixLengthsName = [[0 for x in range(numberOfLocations)] for y in range(numberOfLocations)]
    remove_new_line_row = 0
    remove_new_line_colum = 0
    file = open(pathOfLocations, "r", encoding="utf-8")
    lines = file.readlines()
    # creates matrix with names of all locations and conection between them
    for row in range(len(matrixLengthsName)):
        for i in range(len(lines[row])):
            if lines[row][i:i + 1] == "\n" or lines[row][i:i + 1] == "\t":
                remove_new_line_row = i

            for colum in range(len(matrixLengthsName)):
                for k in range(len(lines[colum])):
                    if lines[colum][k:k + 1] == "\n" or lines[colum][k:k + 1] == "\t":
                        remove_new_line_colum = k

                if row == colum:
                    matrixLengthsName[row][colum] = "0"
                else:
                    matrixLengthsName[row][colum] = lines[row][0:remove_new_line_row] + "-" + lines[colum][0:remove_new_line_colum]
    return matrixLengthsName





#creates all paths to reach every location once (AB, BC, CD)
def creates_matrix_with_posible_paths(numerOfLocations):
    #creates a simple array with how many locations needed to get to
    matrixPosibleWays = [0 for x in range(numerOfLocations)]
    for i in range(numerOfLocations):
        matrixPosibleWays[i] = i

    # makes a matrix with all posible componations of ways of reaching each point and count how many
    allDiffenetPathsRaw = itertools.permutations(matrixPosibleWays, numberOfLocations)
    countAmountOfPaths = 0
    for item in allDiffenetPathsRaw:
        countAmountOfPaths += 1

    # creates allPosibleWaysFin wich is the same as the componations but easier to work with
    allDiffenetPathsFin = [[0 for x in range(numerOfLocations)] for y in range(countAmountOfPaths)]
    allDiffenetPathsRaw = itertools.permutations(matrixPosibleWays, numberOfLocations)
    countRow = -1
    for item in allDiffenetPathsRaw:
        countColum = 0
        countRow += 1
        for point in item:
            allDiffenetPathsFin[countRow][countColum] = point
            countColum += 1

    return allDiffenetPathsFin


def creates_matrix_with_lengths_of_paths(allDiffenetPaths, matrixLengthDistance):
    totalLengthPaths = [0 for x in range(len(allDiffenetPaths))]
    CountSumOfPaths = -1
    for i in range(len(allDiffenetPaths)):
        sumLength = 0
        CountSumOfPaths += 1
        for ii in range(len(allDiffenetPaths[i]) - 1):
            colum = allDiffenetPaths[i][ii]
            row = allDiffenetPaths[i][ii + 1]
            sumLength += matrixLengthDistance[row][colum]
            if ii == (len(allDiffenetPaths[i]) - 2):
                totalLengthPaths[CountSumOfPaths] = sumLength
    return totalLengthPaths


#finds the shortest distance and what way you take to get it (finds the first one not all)
def shortest_Root(totalLengthPaths, allDiffenetPaths):
    print(allDiffenetPaths)
    minimumDistance = min(totalLengthPaths)
    whatIsShotestIndex = 0

    for i in range(len(totalLengthPaths)):
        if totalLengthPaths[i] == min(totalLengthPaths):
            whatIsShotestIndex = i

    whatWayIsShortest = allDiffenetPaths[whatIsShotestIndex]

    return whatWayIsShortest, minimumDistance


#shows what way is the shortest by names given in text file
def replaces_Poins_With_Name(numerOfLocations):
    shortesWayIsName = ["" for x in range(numerOfLocations - 1)]
    for i in range(len(whatWayIsShortest)-1):
        row = whatWayIsShortest[i]
        colum = whatWayIsShortest[i+1]
        shortesWayIsName[i] = matrixNamePair[row][colum]
    return shortesWayIsName


def create_data_file(base_file, file_name):
    path = base_file + "/" + file_name +".txt"
    if not os.path.isfile(path):
        write_file(path, "")

def write_file(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()

def append_file(path, data):
    f = open(path, "a")
    f.write(data)
    f.close()

def clear_file(path):
    f = open(path, "w")
    f.write("")
    f.close()

def remove_file(path):
    os.remove(path)



def file_with_name_and_length_of_pair(matrixNames, matrixAllLengthsBetweenTwoPoints, nameOfFile, pathTo):
    path = pathTo + "/" + nameOfFile +".txt"
    if not os.path.isfile(path):
        create_data_file(pathTo, nameOfFile)

        for row in range(len(matrixNames)):
            for colum in range(len(matrixNames)):
                    append_file(path, matrixNames[row][colum])
                    append_file(path, ";")
                    append_file(path, str(matrixAllLengthsBetweenTwoPoints[row][colum]))
                    append_file(path,"\n")

#uses file created to get the distance between each pair of location otherwise use google matrix api to get the distance
def create_matrix_length_between_each_location(nameOfFile, numberOfLocations, matrixNamePair):
    path = "Data/"+nameOfFile +".txt"
    matrixLengthDistance = [[0 for x in range(numberOfLocations)] for y in range(numberOfLocations)]

    #Cheks if the test file exist otherwise it useses google matrix api
    if os.path.isfile(path):
        f = open(path, "r")
        lines = f.readlines()
        countLines = 0
        for row in range(numberOfLocations):
            for colum in range(numberOfLocations):
                for i in range(len(lines[countLines])):
                    if lines[countLines][i] == ";":
                        matrixLengthDistance[row][colum] = float(lines[countLines][i+1:])
                countLines += 1
        f.close()
        return matrixLengthDistance

    else:
        for irow in range(numberOfLocations):
            for icolum in range(numberOfLocations):

                for iletter in range(len(matrixNamePair[irow][icolum])):
                    if matrixNamePair[irow][icolum][iletter] == "-":
                        origin = matrixNamePair[irow][icolum][:iletter]
                        destination = matrixNamePair[irow][icolum][iletter + 1:]
                        if irow != icolum:
                            distanceStr = gmaps.distance_matrix(origin, destination)["rows"][0]["elements"][0]["distance"]["text"]
                            for i in range(len(distanceStr)):
                                if distanceStr[i] == " ":
                                    matrixLengthDistance[irow][icolum] = float(distanceStr[:i])
        return matrixLengthDistance





matrixNamePair = create_matrix_of_pair_names(numberOfLocations, "Data/Destinations.txt")

matrixLengthDistance = create_matrix_length_between_each_location("test", numberOfLocations,matrixNamePair)
file_with_name_and_length_of_pair(matrixNamePair, matrixLengthDistance, "test", "Data")
allDiffenetPaths = creates_matrix_with_posible_paths(numberOfLocations)
totalLengthPaths = creates_matrix_with_lengths_of_paths(allDiffenetPaths, matrixLengthDistance)
whatWayIsShortest, minimumDistance = shortest_Root(totalLengthPaths, allDiffenetPaths)

shortesWayIsName = replaces_Poins_With_Name(numberOfLocations)
print("\nShortest root is{} wich is {} km long".format(str(shortesWayIsName), str(minimumDistance)))





