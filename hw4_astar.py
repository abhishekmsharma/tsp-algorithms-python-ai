'''
Developer: Abhishek Manoj Sharma
Course: CS 256 Section 2
Homework: 4
Date: October 27, 2017
'''
from hw4_tsp_reader import TSPReader
from hw4_kruskal import kruskalMST
from math import sqrt
import time
import os.path
from argparse import ArgumentParser

START_NODE_INDEX = 0
kruskal_mst = []
kruskal_mst_total = 0.0
edge_cost = {}
cm = {}
number_of_nodes = 0

#cartesian_matrix() method is used to produce a distance matrix of the nodes
def cartesian_matrix(coords):
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = sqrt(dx * dx + dy * dy)
            matrix[i, j] = dist
    print "Distance matrix created"
    return matrix

#astar_main_run() drives the program by calling the cartesian_matrix() method to generate distance matrix and then computeAStar() method to generate path using A* algorithm
def astar_main_run(filename):
    start_time = time.time()
    global cm, tsp_file_name, kruskal_mst, kruskal_mst_total, edge_cost, number_of_nodes
    tsp_file_name = filename

    #creating an object of class TSPReader to read the TSP file provided
    tsp_reader = TSPReader()
    tsp_attributes = tsp_reader.readTSPFile(tsp_file_name)

    #if EDGE_WEIGHT_TYPE is not EUC_2D then return and do not calculate ahead
    if not tsp_attributes[0]:
        return
    coords = tsp_attributes[1]
    print "------------------------------------------"
    print "A* Algorithm -", tsp_file_name
    cm = cartesian_matrix(coords)
    print "Computing using A* algorithm.\nThis may take a lot of time, please be patient."
    kruskal_results = kruskalMST(cm)
    kruskal_mst = kruskal_results[0]
    list_of_nodes = kruskal_results[1]

    for item in kruskal_mst:
        kruskal_mst_total+=item[1]

    edge_cost[0] = 0.0
    for key, value in cm.iteritems():
        if key[0] == 0:
            edge_cost[key[1]] = value
    number_of_nodes = len(list_of_nodes)
    computeAStar(list_of_nodes)
    print "Total time:", "{0:.3f}".format((time.time() - start_time)), "seconds"
    print "------------------------------------------"

#successor_function() method is used to generate a list of all unvisited nodes
def successor_function(visited_nodes,all_nodes):
    return list(set(visited_nodes) ^ set(all_nodes))

#calc_edge_cost() method is used to calcualte the g(n)
def calc_edge_cost(current_node,visited_nodes):
    global cm
    v_nodes = visited_nodes[:]
    v_nodes.append(current_node)
    v_length = len(v_nodes)
    total = 0.0
    for i in range(0,v_length-1):
        n1 = v_nodes[i]
        n2 = v_nodes[i+1]
        for key,value in cm.iteritems():
            if (key[0]==n1 and key[1]==n2) or (key[0]==n2 and key[1]==n1):
                total+=value
                break
    return total

#computeAStar() method calculates the path using A* algorithm
def computeAStar(list_of_nodes):
    global START_NODE_INDEX, edge_cost, kruskal_mst_total
    current_node = START_NODE_INDEX
    visited_nodes = []
    visited_nodes.append(current_node)
    all_nodes_count = len(list_of_nodes)
    dictNodes = {}
    unvisited_nodes = successor_function(visited_nodes, list_of_nodes)
    while len(visited_nodes)<all_nodes_count:
        for u_n in unvisited_nodes:
            current_node = u_n
            g_n = calc_edge_cost(current_node,visited_nodes)
            h_n = distNearestUnvisited(current_node,unvisited_nodes) + getKruskalTotal(visited_nodes,current_node) + distNearestUnvisitedToStart(current_node,unvisited_nodes)
            f_n = g_n + h_n
            v_nodes = visited_nodes[:]
            v_nodes.append(current_node)
            dictNodes[tuple(v_nodes)] = f_n
        min_node = min(dictNodes, key=dictNodes.get)
        visited_nodes = list(min_node)
        del dictNodes[min_node]
        unvisited_nodes = successor_function(visited_nodes, list_of_nodes)

    #calculate and print tour length
    tourLength(visited_nodes)

#tourLength() method is used to calcualte and print the tour length of the tour provided as list
def tourLength(tour):
    global cm, number_of_nodes
    total = 0
    t = list(tour)
    for i in range(number_of_nodes):
        j = (i + 1) % number_of_nodes
        total += cm[t[i], t[j]]
    print "Tour length:","{0:.3f}".format(total)

#used to calculate the first path of the heuristic h(n)
def distNearestUnvisited(node,unvisited_nodes):
    global cm
    dict_current_node = {}
    for key,value in cm.iteritems():
        if key[0] == node and key[1] in unvisited_nodes:
            dict_current_node[key[1]] = value
    if len(unvisited_nodes) == 1:
        return 0
    return dict_current_node[min(dict_current_node, key=dict_current_node.get)]

#used to calculate the third path of the heuristic h(n)
def distNearestUnvisitedToStart(current_node, unvisited_nodes):
    global edge_cost
    dict_univisited_start_dist={}
    for key,value in edge_cost.iteritems():
        if key in unvisited_nodes and key<>current_node:
            dict_univisited_start_dist[key] = value
    if len(unvisited_nodes)==1:
        dict_univisited_start_dist[0] = edge_cost[current_node]
    return dict_univisited_start_dist[min(dict_univisited_start_dist, key=dict_univisited_start_dist.get)]

#used to generate MST of all unvisited nodes using Kruskal's algorithm
def getKruskalTotal(visited_nodes,current_node):
    global cm
    visited_temp = visited_nodes[:]
    visited_temp.append(current_node)
    cm_temp = dict(cm)

    for key,value in cm_temp.items():
        if not set(visited_temp).isdisjoint(key):
            del cm_temp[key]
    if len(cm_temp)==0:
        return 0
    else:
        total = 0.0
        kMST = kruskalMST(cm_temp)[0]
        for item in kMST:
            total += item[1]
        return total

if __name__ == "__main__":

    help_description = "The program accepts the path of .TSP file as input and computes the path using A* algorithm"
    parser = ArgumentParser(description=help_description)
    parser.add_argument("-file", help="TSP File Path", required=True)
    args = parser.parse_args()
    f_name = args.file

    if os.path.isfile(f_name):
        astar_main_run(f_name)
    else:
        print f_name, "- File not found. \nPlease make sure the path is correct and try again."
        exit()