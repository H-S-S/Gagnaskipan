import googlemaps
import itertools
import os



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


#creates matrix with points x points given from the file
def get_number_of_locations(loc_array):
    return len(loc_array)



#The names of whays you can take from one point to another like(Furuhjali-klyfjasel and Furuhjali-Bakkasel and so on)
def create_matrix_of_pair_names(numer_of_locations, location_array):
    matrix_loc_to_loc = [["0" for x in range(numer_of_locations)] for y in range(numer_of_locations)]


    # creates matrix with names of all locations and conection between them
    for row in range(numer_of_locations):
        for column in range(numer_of_locations):

            if row == column:
                matrix_loc_to_loc[row][column] = "0"
            else:
                matrix_loc_to_loc[row][column] = location_array[row] + "-" + location_array[column]



    return matrix_loc_to_loc



def create_matrix_length_between_each_location_using_array(numer_of_locations, matrix_loc_to_loc):
    matrix_length_distance_between_loc = [[0 for x in range(numer_of_locations)] for y in range(numer_of_locations)]
    f = open("API.txt", "r")
    lines = f.readlines()
    API_key = lines[0]
    f.close()
    gmaps = googlemaps.Client(key=API_key)
    #useses google matrix api
    for irow in range(numer_of_locations):
        for icolum in range(numer_of_locations):

            for iletter in range(len(matrix_loc_to_loc[irow][icolum])):
                if matrix_loc_to_loc[irow][icolum][iletter] == "-":
                    origin = matrix_loc_to_loc[irow][icolum][:iletter]
                    destination = matrix_loc_to_loc[irow][icolum][iletter + 1:]
                    if irow != icolum:
                        distanceStr = gmaps.distance_matrix(origin, destination)["rows"][0]["elements"][0]["distance"]["text"]
                        for i in range(len(distanceStr)):
                            if distanceStr[i] == " ":
                                matrix_length_distance_between_loc[irow][icolum] = float(distanceStr[:i])

    return matrix_length_distance_between_loc



#creates all paths to reach every location once (AB, BC, CD)
def creates_matrix_with_posible_paths(numer_of_locations):

    #creates a simple array with how many locations needed to get to
    matrix_posible_ways = [0 for x in range(numer_of_locations)]
    for i in range(numer_of_locations):
        matrix_posible_ways[i] = i

    # makes a matrix with all posible componations of ways of reaching each point and count how many
    allDiffenetPathsRaw = itertools.permutations(matrix_posible_ways, numer_of_locations)
    countAmountOfPaths = 0
    for item in allDiffenetPathsRaw:
        countAmountOfPaths += 1

    # creates allPosibleWaysFin wich is the same as the componations but easier to work with
    all_diffenet_paths_fin = [[0 for x in range(numer_of_locations)] for y in range(countAmountOfPaths)]
    allDiffenetPathsRaw = itertools.permutations(matrix_posible_ways, numer_of_locations)
    countRow = -1
    for item in allDiffenetPathsRaw:
        countColum = 0
        countRow += 1
        for point in item:
            all_diffenet_paths_fin[countRow][countColum] = point
            countColum += 1

    return all_diffenet_paths_fin

def creates_matrix_with_lengths_of_paths(all_diffenet_paths, matrix_length_distance_between_loc):
    total_length_of_all_paths = [0 for x in range(len(all_diffenet_paths))]
    CountSumOfPaths = -1
    for i in range(len(all_diffenet_paths)):
        sumLength = 0
        CountSumOfPaths += 1
        for ii in range(len(all_diffenet_paths[i]) - 1):
            colum = all_diffenet_paths[i][ii]
            row = all_diffenet_paths[i][ii + 1]
            sumLength += matrix_length_distance_between_loc[row][colum]
            if ii == (len(all_diffenet_paths[i]) - 2):
                total_length_of_all_paths[CountSumOfPaths] = sumLength
    return total_length_of_all_paths


#finds the shortest distance and what way you take to get it (finds the first one not all)
def shortest_Root(total_length_of_all_paths, all_diffenet_paths):

    minimumDistance = min(total_length_of_all_paths)
    whatIsShotestIndex = 0

    for i in range(len(total_length_of_all_paths)):
        if total_length_of_all_paths[i] == min(total_length_of_all_paths):
            whatIsShotestIndex = i

    whatWayIsShortest = all_diffenet_paths[whatIsShotestIndex]

    return whatWayIsShortest, minimumDistance


#shows what way is the shortest by names given in text file
def replaces_Poins_With_Name(numer_of_locations, what_way_is_shortest, matrix_loc_to_loc):
    shortes_way_is_name = ["" for x in range(numer_of_locations - 1)]
    for i in range(len(what_way_is_shortest)-1):
        row = what_way_is_shortest[i]
        colum = what_way_is_shortest[i+1]
        shortes_way_is_name[i] = matrix_loc_to_loc[row][colum]

    return shortes_way_is_name
