# Sourabh Jain (sourj@cs.umn.edu)
# This program performs a vid assignment for the input topology file.
# First line of the input topology contains: <# of Edges in the topology> <number of nodes in the topology>
# A node can be represented using a string of characters (with no spaces in it)

# It creates an output file which contains the node to vid mapping
import sys, random

# My own random function wrapper:
def myrandom ():
    global randomize
    return random.random()
    if randomize:
        return random.random()
    else:
        return 0.1
      
if len(sys.argv) != 3:
    print "Usage: ", sys.argv[0], '<input topology file, as an adjacency list file>', '<output vid file>'
    sys.exit()
  
print "Warning: it overwrites the output file!"
# first read the topology into a dictionary
fin = open(sys.argv[1], 'r')
fout = open(sys.argv[2],'w')

# delimiter can be changed here
delimiter = ' '
nodes = {} # nodes and their adjacency list
nodeids = {} # nodeid to 0,1,2.. mapping
ids2node = {} # 0,1,2.. to intial nodeid mapping
node2vid = {} # 0,1,2.. to vid mapping
node_n = 0 # number of lines in the file
node2cluster = [] # 0,1,2... to clusterLabel mapping
randomize = True # if we need to break the ties then use the randomization


#line = fin.readline() # ignore the first line
line = fin.readline()
line = line.strip()    
while line != '':
    #print line
    node = line.split(delimiter)
    if node[0] not in nodes:
        nodes[node[0]] = {}
        nodeids[node[0]] = node_n
        ids2node[node_n] = node[0]
        node2cluster.append(node_n)
        node2vid[node_n] = ''
        node_n += 1
    for node1 in node[1:]:
        if node1 not in nodes:
            nodes[node1] = {}
            nodeids[node1] = node_n
            ids2node[node_n] = node1
            node2cluster.append(node_n)
            node2vid[node_n] = ''
            node_n += 1
        nodes[node[0]][node1] = 0
        nodes[node1][node[0]] = 0

    line = fin.readline()
    line = line.strip()
fin.close()
#print 'Input Topology: ',nodes
# construct initial cluster topology    
clusterTopo = {}
for id in nodeids:
    clusterTopo[nodeids[id]] = []
    for n in nodes[id]:
        clusterTopo[nodeids[id]].append(nodeids[n])
maxiter = 5000
iter = 0 
# now cluster all the nodes one by one till we have only 1 large node left.
while True:
    iter += 1
    if iter >maxiter:
        print 'May be caught in a loop! too many iteration, stopping after',maxiter,'iterations'
        break
    if (sum(node2cluster)) == 0:
        print 'done!'
        break
    
    # find the smallest cluster and see if it can be clustered with other nodes
    clustersizes = {}
    for t in node2cluster:
        if node2cluster[t] not in clustersizes:
            clustersizes[node2cluster[t]] = 0
        clustersizes[node2cluster[t]] = clustersizes[node2cluster[t]] + 1
    if len(clustersizes) == 1:
        print 'Only one cluster left, let\'s stop now!'
        break
    smallestClusterLabel = 0
    smallestClusterSize = clustersizes[0]
    for c in clustersizes:
        if clustersizes[c] < smallestClusterSize:
            smallestClusterSize = clustersizes[c]
            smallestClusterLabel = c
        elif clustersizes[c] == smallestClusterSize:
            rand = myrandom()
            if rand > 0.5:
                smallestClusterSize = clustersizes[c]
                smallestClusterLabel = c
    
    # now find the smallest cluster which it can be clubbed with
    secondCluster = clusterTopo[smallestClusterLabel][0]
    secondClusterSize = clustersizes[secondCluster]
    #print 'SmallestClusterLabel:',smallestClusterLabel
    #print 'SmallestClusterSize:',smallestClusterSize
    #print 'ClusterSizes:',clustersizes
    #print 'ClusterTopo:',clusterTopo
    for c in clusterTopo[smallestClusterLabel]:
        #print c
        if clustersizes[c] < secondClusterSize:
            secondCluster = c
            secondClusterSize = clustersizes[c]
        elif clustersizes[c] == secondClusterSize:
            rand = myrandom()
            if rand > 0.5:
                secondClusterSize = clustersizes[c]
                secondCluster = c
    
    # Now put these two clusters together
    newclusterLabel = min(secondCluster, smallestClusterLabel)
    #print 'SmallestCluster:', smallestClusterLabel,'SecondCluster:', secondCluster
    #print 'NewClusterLabel:',newclusterLabel
    len1 = -1
    len2 = -1    
    for x in node2cluster:
        if node2cluster[x] == secondCluster:
            #node2vid[x] = '0' + node2vid[x]
            len1 = len(node2vid[x])
        elif node2cluster[x] == smallestClusterLabel:
            #node2vid[x] = '1' + node2vid[x]
            len2 = len(node2vid[x])
    len3 = max(len1,len2)
    #print 'len1:', len1, 'len2:', len2, 'len3:',len3
    if len2 != len1:
        for x in node2vid:
            if (node2cluster[x] == secondCluster) or (node2cluster[x] == smallestClusterLabel):
                xlen = len(node2vid[x])
                if xlen < len3:
                    #print 'Node2vid[',x,']',node2vid[x]
                    node2vid[x] = (len3-xlen)*'0' + node2vid[x]
                    #print 'Node2vid[',x,']',node2vid[x]
    
    # udpate the cluster labels
    #print 'Node2Vid before:',node2vid
    for x in node2vid:
        if node2cluster[x] == secondCluster:
            node2vid[x] = '0' + node2vid[x]
            #node2cluster[x] = newclusterLabel
        elif node2cluster[x] == smallestClusterLabel:
            node2vid[x] = '1' + node2vid[x]
            #node2cluster[x] = newclusterLabel
    for x in node2vid:
        if node2cluster[x] == secondCluster or node2cluster[x] == smallestClusterLabel:
            node2cluster[x] = newclusterLabel
    #print 'Node2Vid After:',node2vid
            
    # now update the topology
    newtopo = {}
    for c in clusterTopo:
        for i in range(0, len(clusterTopo[c])):
            if clusterTopo[c][i] == smallestClusterLabel or clusterTopo[c][i]== secondCluster:
                clusterTopo[c][i] = newclusterLabel
        if clusterTopo[c].count(newclusterLabel) > 1:
            clusterTopo[c].remove(newclusterLabel)
        if c != smallestClusterLabel and c!= secondCluster:
            newtopo[c] = clusterTopo[c]
    newlist = clusterTopo[smallestClusterLabel] + clusterTopo[secondCluster]
    newkeys ={}
    for x in newlist:
        if x != newclusterLabel:
            newkeys[x] = 0
    newtopo[newclusterLabel] = newkeys.keys()
    
    # some cleaning
    newkeys = {}
    newlist = []
    clusterTopo = newtopo
    newtopo = {}
    #print 'Clustered Nodes:',smallestClusterLabel, secondCluster
    #print 'NewClusterTopo:',clusterTopo
    #print 'VID Assignment: ', node2vid
    #print 'Node to cluster subscription: ', node2cluster
    #print '\n\n'

for x in node2vid:
    fout.write(str(ids2node[x]) + ' ' + node2vid[x]+'\n')
fout.close()
