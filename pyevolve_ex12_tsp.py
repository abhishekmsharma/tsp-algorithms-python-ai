'''
Originally developed by: Pyevolve (Sources posted on sourceforge)
Modified by: Abhishek Manoj Sharma
Course: CS 256 Section 2
Homework: 4
Date: October 27, 2017
'''
from pyevolve import G1DList, GAllele
from pyevolve import GSimpleGA
from pyevolve import Crossovers
from pyevolve import Consts
from hw4_tsp_reader import TSPReader
import os
import time
import os.path
from argparse import ArgumentParser

import sys, random
random.seed(1024)
from math import sqrt

cm     = []
coords = []
CITIES = 100
WIDTH   = 1920
HEIGHT  = 1080
LAST_SCORE = -1

#cartesian_matrix() method is used to produce a distance matrix of the nodes
def cartesian_matrix(coords):
    matrix={}
    for i, (x1, y1) in enumerate(coords):
        for j,(x2,y2)in enumerate(coords):
            dx, dy = x1-x2, y1-y2
            dist=sqrt(dx*dx + dy*dy)
            try:
                matrix[i,j] = dist
            except MemoryError:
                print "Encountered memory error"
                return False
    print "Distance matrix created"
    return matrix

#tour_length() method is sued to calculate the length of a tour provided as list to it
def tour_length(matrix, tour):
    """ Returns the total length of the tour """
    total = 0
    t = tour.getInternalList()
    for i in range(CITIES):
        j = (i+1)%CITIES
        total += matrix[t[i], t[j]]
    return total

#writes the tour path to tsp_output.txt
def write_tour_to_file(coords, tour):
    file = open("tsp_output.txt", "w")
    file.write("TOUR_SECTION"),
    num_cities = len(tour)
    for i in range(num_cities):
        #adding +1 to display node ID instead of index
        file.write("\n" + str(tour[i] + 1))
    file.close()
    print "The output was saved into the tsp_output.txt file."


def G1DListTSPInitializator(genome, **args):
   """ The initializator for the TSP """
   lst = [i for i in xrange(genome.getListSize())]
   random.shuffle(lst)
   genome.setInternalList(lst)

def ga_main_run(filename, write_to_files=False):
    print "------------------------------------------"
    print "Genetic Algorithm -", filename
    start_time = time.time()
    global cm, coords, WIDTH, HEIGHT, CITIES

    #creating an object of class TSPReader to read the TSP file provided
    tsp_reader = TSPReader()
    tsp_attributes = tsp_reader.readTSPFile(filename)

    #if EDGE_WEIGHT_TYPE is not EUC_2D then return and do not calculate ahead
    if not tsp_attributes[0]:
        return
    coords = tsp_attributes[1]
    CITIES = len(coords)
    cm     = cartesian_matrix(coords)
    if cm is False:
        print "------------------------------------------"
        return

    genome = G1DList.G1DList(len(coords))
    genome.evaluator.set(lambda chromosome: tour_length(cm, chromosome))
    genome.crossover.set(Crossovers.G1DListCrossoverEdge)
    genome.initializator.set(G1DListTSPInitializator)
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(1000)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)

    #setting stdout to null to avoid printing
    sys.stdout = open(os.devnull, 'w')

    ga.evolve(freq_stats=500)
    total_time = "{0:.3f}".format((time.time() - start_time))

    #enabling stdout again to print the tour length andother information
    sys.stdout = sys.__stdout__
    best = ga.bestIndividual()
    print "Tour length:", "{0:.3f}".format(best.getRawScore())
    print "Total time:",total_time,"seconds"
    if write_to_files:
        write_tour_to_file(coords,best)
    print "------------------------------------------"

if __name__ == "__main__":

    help_description = "The program accepts the path of .TSP file as input and computes the path using Genetic algorithm"
    parser = ArgumentParser(description=help_description)
    parser.add_argument("-file", help="TSP File Path", required=True)
    args = parser.parse_args()
    f_name = args.file

    if os.path.isfile(f_name):
        ga_main_run(f_name, True)
    else:
        print f_name, "- File not found. \nPlease make sure the path is correct and try again."
        exit()