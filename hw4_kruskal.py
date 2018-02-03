'''
Developer: Abhishek Manoj Sharma
Course: CS 256 Section 2
Homework: 4
Date: October 27, 2017
'''
disjoint_sets = {}

#kruskalMST() method accepts a distance matrix as input and computes the MST using Kruskal's algorithm
def kruskalMST(cm):
    global disjoint_sets
    list_of_nodes = []
    for key in list(cm.keys()):
        list_of_nodes.append(key[0])
        if cm[key] == 0:
            del cm[key]
    cm = sorted(cm.items(), key=lambda x: x[1])
    list_of_nodes  = list(set(list_of_nodes))

    for item in list_of_nodes:
        disjoint_sets[item] = [item]

    kruskal_mst = []

    for item in cm:
        key1 = getKey(item[0][0])
        key2 = getKey(item[0][1])
        if key1 <> key2:
            disjoint_sets[key1].extend(disjoint_sets[key2])
            del disjoint_sets[key2]
            kruskal_mst.append(item)

    return kruskal_mst,list_of_nodes

#getKey() method is used to identify the set the node is a part of to check for nodes forming cycles
def getKey(node_value):
    global disjoint_sets
    for key,value in disjoint_sets.iteritems():
        if node_value in value:
            return key