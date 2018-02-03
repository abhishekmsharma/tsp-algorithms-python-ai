'''
Developer: Abhishek Manoj Sharma
Course: CS 256 Section 2
Homework: 4
Date: October 27, 2017
'''

from hw4_tsp_reader import TSPReader
from math import sqrt
from argparse import ArgumentParser
import time
import os.path

cm = {}
TOUR_START_NODE_INDEX = 0
tsp_file_name = ""

#cartesian_matrix() method is used to produce a distance matrix of the nodes
def cartesian_matrix(coords):
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = sqrt(dx * dx + dy * dy)
            try:
                if (j,i) not in matrix:
                    matrix[i, j] = dist
            except MemoryError:
                print "Memory error encountered. Insufficient resources in machine."
                return False
    print "Distance matrix created"
    return matrix

#greedy_main_run() method drives the program by calling the cartesian_matrix() method to produce distance matrix and then the computePathGreedy() method to calculate path using Greedy algorithm
def greedy_main_run(filename, printTour = False):
    global cm, TOUR_START_NODE_INDEX, tsp_file_name
    tsp_file_name = filename

    #creating an object of class TSPReader to read the TSP file provided
    tsp_reader = TSPReader()
    tsp_attributes = tsp_reader.readTSPFile(tsp_file_name)

    #if EDGE_WEIGHT_TYPE is not EUC_2D then return and do not calculate ahead
    if not tsp_attributes[0]:
        return
    coords = tsp_attributes[1]
    print "------------------------------------------"
    print "Greedy Algorithm -", tsp_file_name
    cm = cartesian_matrix(coords)
    if cm is False:
        print "------------------------------------------"
        return
    start_time = time.time()
    computePathGreedy(len(coords), TOUR_START_NODE_INDEX, printTour)
    print "Total time:", "{0:.3f}".format((time.time() - start_time)), "seconds"
    print "------------------------------------------"

#computePathGreedy() method produces the tour using greedy algorithm
def computePathGreedy(number_of_nodes, start_node, printTour):
    global cm, TOUR_START_NODE_INDEX, tsp_file_name
    visited_nodes = []
    total_tour_length = 0.0
    while len(visited_nodes) <> number_of_nodes-1:
        visited_nodes.append(start_node)
        node_distances = {}
        for key, value in cm.iteritems():
            if key[0] == start_node and key[0] <> key[1] and key[1] not in visited_nodes:
                node_distances[key[1]] = value
            elif key[1] == start_node and key[0] <> key[1] and key[0] not in visited_nodes:
                node_distances[key[0]] = value
        start_node = min(node_distances, key=node_distances.get)
        total_tour_length += node_distances.pop(start_node)

    visited_nodes.append(start_node)

    try:
        total_tour_length += cm[start_node, TOUR_START_NODE_INDEX]
    except KeyError:
        total_tour_length += cm[TOUR_START_NODE_INDEX,start_node]

    #adding +1 to display node ID instead of index
    visited_nodes = [i + 1 for i in visited_nodes]
    if printTour:
        print "\nPath:", visited_nodes
    print "Tour length:", "{0:.3f}".format(total_tour_length)

if __name__ == "__main__":

    help_description = "The program accepts the path of .TSP file as input and computes the path using Greedy algorithm"
    parser = ArgumentParser(description=help_description)
    parser.add_argument("-file", help="TSP File Path", required=True)
    args = parser.parse_args()
    f_name = args.file

    if os.path.isfile(f_name):
        greedy_main_run(f_name, True)
    else:
        print f_name,"- File not found. \nPlease make sure the path is correct and try again."
        exit()