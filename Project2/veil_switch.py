#!/usr/bin/python

from veil import extractARPDstMac
import socket, struct, sys, time, random

# Local imports 
from veil import * # for the constants.
from threading import Thread

#######################################
#    Server Port THREAD FUNCTION
#######################################
def serverThread(server_socket):
    while(True):
        print '-----------------------------------------------------'
        client_socket, address = server_socket.accept()
        print "\n",myprintid,"Received an incoming connection from ", address
        packet = receivePacket(client_socket)
        print 'Received packet: ',packet.encode("hex")
        if len(packet) < HEADER_LEN + 8:
            print 'Malformed packet! Packet Length:',len(packet), 'Expected:',HEADER_LEN+8
            client_socket.close()
            continue
        printPacket(packet,L)
        processPacket(packet)
        client_socket.close()
###############################################
#    Server THREAD FUNCTION ENDS HERE
###############################################

# Adds an entry to rdvStore, and also ensures that there are no duplicates
def addIfNODuplicateRDVENTRY(dist,newentry):
    global rdvStore
    for x in rdvStore[dist]:
        if x[0] == newentry[0] and x[1] == newentry[1]:
            return
    rdvStore[dist].append(newentry)
    
# Finds a logically closest gateway for a given svid    
def findAGW(rdvStore,k,svid):    
    gw = {}
    
    # if no entry return blank string
    if k not in rdvStore:
        return ''
    
    # for every entry in rdvStore, add Gateway to gateway set {gw}
    for t in rdvStore[k]:
        r = delta(t[0],svid)
        
        if r not in gw:
            gw[r] = t[0]
        gw[r] = t[0]
        
    if len(gw) == 0:
        return ''    
    
    # get all the keys from the gateway set {gw}
    s = gw.keys()
    
    # sort based on logical distance
    s.sort()
    
    # return the gateway with least logical distance
    return gw[s[0]]

#######################################
#    PROCESSPACKET FUNCTION
#######################################
def processPacket(packet):
    dst = getDest(packet,L)
    
    # forward the packet if I am not the destination
    if dst != myvid:
        routepacket(packet)
        return
    
    # I am the destination of the packet, so process it.
    packettype = getOperation(packet) # ie. RDV_REPLY / RDV_QUERY / RDV_PUBLISH / DATA?
    print myprintid, 'Processing packet'
    printPacket(packet,L)
    
    # extract source vid from packet
    svid = bin2str((struct.unpack("!I", packet[8:12]))[0],L)
    
    # extract payload from packet
    payload = bin2str((struct.unpack("!I", packet[16:20]))[0],L)
        
    # RDV_PUBLISH packet   
    if packettype == RDV_PUBLISH:
		#payload in RDV_PUBLISH is a vid that is the gateway at dist
        dist = delta(myvid,payload) # calculate logical distance
        
        # check if published information already in rdvStore
        if dist not in rdvStore:
            rdvStore[dist] = []
        
        # prepare rdvStore entry    
        newentry = [svid,payload] # 
        
        # add new entry if not present in rdvStore
        addIfNODuplicateRDVENTRY(dist,newentry)
        return
        
    elif packettype == RDV_QUERY:
        k = int(payload,2)
        
        # search in rdvStore for the logically closest gateway to reach kth distance away neighbor
        gw = findAGW(rdvStore,k,svid)
        
        # no gateway found
        if gw == '':
            print myprintid, 'No gateway found for the rdv_query packet to reach bucket: ',k,' for node: ', svid
            return
        
        # gateway found, form reply packet and sent to svid
        # create a RDV_REPLY packet and send it
        replypacket = createRDV_REPLY(int(gw,2),k,myvid, svid)
        routepacket(replypacket)
        return
        
    elif packettype == RDV_REPLY:
        # Fill my routing table using this new information
        [gw] = struct.unpack("!I", packet[20:24])
        gw_str = bin2str(gw,L)
        k = int(payload,2)
        
        if k in routingTable:
            print myprintid, 'Already have an entry to reach neighbors at distance: ',k
            return
        
        # get nextHop using routingTable to reach Gateway [gw_str]    
        nexthop = getNextHop(gw_str)
        
        if nexthop == '':
            print 'ERROR: no nexthop found for the gateway:',gw_str
            print 'New routing information couldnt be added! '
            return
        
        # convert nextHop from binary to decimal    
        nh = int(pid2vid[nexthop],2)
        
        # prepare routingTable entry
        bucket_info = [nh, gw, getPrefix(myvid,k)]
        routingTable[k] = []
        
        # insert entry into routingTable
        routingTable[k].append(bucket_info)
    else:
        print myprintid, 'Unexpected Packet!!'
        
###############################################
#    SPROCESSPACKET FUNCTION ENDS HERE
###############################################
###############################################
#    getNextHop function starts here
###############################################

def getNextHop(destvid_str):
    nexthop = ''
    
    # if dest is neighbor return 
    if destvid_str in vid2pid:
        return vid2pid[destvid_str]
    
    # calculate logical distance
    dist = delta(myvid,destvid_str)
    
    # return node from routingTable with dist
    if dist in routingTable:
        nexthop = bin2str(routingTable[dist][0][0],L)
        nexthop = vid2pid[nexthop]
        
    return nexthop
    
###############################################
#    getNextHop FUNCTION ENDS HERE
###############################################

###############################################
#    sendPacket function starts here
###############################################

def sendPacket(packet,nexthop):
    # connect to the nexthop
    try:
        toSwitch = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = nexthop.split(':')
        toSwitch.connect((address[0],int(address[1])))
        toSwitch.send(packet) # send the packet
        toSwitch.close() # close the connection
    except:
        print myprintid,"Unexpected Exception: ",'received while sending packet to Switch at IP: ', address[0], 'port: ',address[1]
        printPacket(packet,L)    
    
    
###############################################
#    sendPacket FUNCTION ENDS HERE
###############################################

###############################################
#    routepacket function starts here
###############################################

def routepacket(packet):
    global myvid, routingTable, vid2pid, myprintid, L
    
    # get destination from packet
    dst = getDest(packet,L)
    
    # If destination is me
    if dst == myvid:
        #print 'I am the destination!'
        processPacket(packet)
        return
    
    #If destination is one of my physical neighbor
    if dst in vid2pid:
        sendPacket(packet,vid2pid[dst])
        return
    
    #Find the next hop
    nexthop = ''
    packettype = getOperation(packet) # ie. RDV_REPLY / RDV_QUERY / RDV_PUBLISH / DATA?
    
    while nexthop == '':
        if dst in vid2pid:
            nexthop = vid2pid[dst]
            break
        
        # Calculate logical distance with destination    
        dist = delta(myvid,dst)
        
        if dist == 0:
            break
            
        if dist in routingTable:
            nexthop = bin2str(routingTable[dist][0][0],L)
            nexthop = vid2pid[nexthop]
            break
            
        if (packettype != RDV_PUBLISH) and (packettype != RDV_QUERY):
            break 
        
        print myprintid,'No next hop for destination: ',dst,'dist: ', dist
        # flip the dist bit to
        dst = flipBit(dst,dist)
         
    #print 'MyVID: ', myvid, 'DEST: ', dst
    if dst != getDest(packet,L):
        # update the destination on the packet
        updateDestination(packet,dst)
        
    if dst == myvid:
        #print "I am the destination for this RDV Q/P message:"
        printPacket(packet,L)
        processPacket(packet)
        
    if nexthop == '':
        print myprintid,'no route to destination' ,'MyVID: ', myvid, 'DEST: ', dst
        printPacket(packet,L)
        return
    
    sendPacket(packet,nexthop)

###############################################
#    routepacket FUNCTION ENDS HERE
###############################################
###############################################
#    Publish function starts here
###############################################

def publish(bucket,k):
    global myvid
    dst = getRendezvousID(k,myvid)
    packet = createRDV_PUBLISH(bucket,myvid,dst)
    print myprintid, 'Publishing my neighbor', bin2str(bucket[0],L), 'to rdv:',dst
    printPacket(packet,L)
    routepacket(packet)

###############################################
#    Publish FUNCTION ENDS HERE
###############################################

###############################################
#    Query function starts here
###############################################

def query(k):
    global myvid
    dst = getRendezvousID(k,myvid)
    packet = createRDV_QUERY(k,myvid,dst)
    print myprintid, 'Quering to reach Bucket:',k, 'to rdv:',dst
    printPacket(packet,L)
    routepacket(packet)

###############################################
#    Query FUNCTION ENDS HERE
###############################################


###############################################
#    RunARount function starts here
###############################################

def runARound(round):
    global routingTable
    global vid2pid, pid2vid, mypid, myvid,L
    # start from round 2 since connectivity in round 1 is already learnt using the physical neighbors
    for i in range(2,round+1):
        # see if routing entry for this round is already available in the routing table.
        if i in routingTable:
            if len(routingTable[i]) > 0:
                #publish the information if it is already there
                for t in routingTable[i]:
                    if t[1] == int(myvid,2):
                        publish(t,i)
            else:
                query(i)
        else:
            query(i)

###############################################
#    RunARound FUNCTION ENDS HERE
###############################################

if len(sys.argv) != 4:
    print '-----------------------------------------------'
    print 'Wrong number of input parameters'
    print 'Usage: ', sys.argv[0], ' <TopologyFile>', '<vid_file>', '<my_ip:my_port>'
    print 'A node will have two identifiers'
    print 'i) pid: in this project pid is mapped to IP:Port of the host so if a veil_switch is running at flute.cs.umn.edu at port 5211 than pid of this switch is = flute.cs.umn.edu:5211'
    print 'ii) vid: It is the virtual id of the switch.'
    print 'TopologyFile: It contains the adjacency list using the pids. So each line contains more than one pid(s), it is interepreted as physical neighbors of the first pid.'
    print 'vid_file: It contains the pid to vid mapping, each line here contains a two tuples (space separated) first tuple is the pid and second tuple is the corresponding vid'
    print '-----------------------------------------------\n\n\n'
    sys.exit(0)

sleeptime = random.random()*5
print 'Sleeping :',sleeptime,' seconds!'
time.sleep(sleeptime)

# Put arguments into variables
topofile = sys.argv[1]
vidfile = sys.argv[2]
myport = int((sys.argv[3].split(":"))[1])
mypid = sys.argv[3]


# Learn my neighbors by reading the input adjacency list file
myneighbors = []
myvid = ''
pid2vid = {}
vid2pid = {}
routingTable = {} 
rdvStore = {} 
myprintid = ''
L = 0
# Routing table is a dictionary, it contains the values at each distances from 1 to L
# So key in the routing table is the bucket distance, value is the 3 tuple: tuple 1 = nexthop (vid), tuple 2 = gateway (vid), tuple 3 = prefix (string)

# RDV STORE is a dictionary: it stores the list of edges with distances

# open the topology file in READ mode
fin = open(topofile,'r')

# read the file line by line
line = fin.readline() #reads and pushes the first line into "line"
line = line.strip() #strips whitespaces from the beginning and end of the line (not the whitespaces in between)

while line != '':
    if line.find(mypid) ==0: #satisfies if the first node in the line is mypid
        # this is the line which contains the neighbor list for my 
        myneighbors = (line.split(' '))[1:] #populates every neighbor into the myneigbors array
        break #exit while loop
    line = fin.readline() # move to next line
    line = line.strip()
fin.close() # close topology file

#Error checking
if ' ' in myneighbors:
    print 'Warning: My neighbor list contains empty pids!'
if  len(myneighbors) < 1:
    print 'Warning: My neighbor list is empty, will quit now!'
    sys.exit(0)

#Print list of myneighbors    
print 'My neighbors: ',myneighbors    

# Learn my and myneighbor's vids
fin = open(vidfile, 'r') #open file in read mode
line = fin.readline() #reads and pushes the first line into "line"
line = line.strip() #strips whitespaces from the beginning and end of the line (not the whitespaces in between)

while line != '':
    tokens = line.split(' ')
    if tokens[0] in myneighbors: # if pid present in myneighbor[] array
        pid2vid[tokens[0]] = tokens[1] # eg. pid2vid["localhost:5001"] = "11"
        vid2pid[tokens[1]] = tokens[0] # eg. pid2vid["11"] = "localhost:5001"
    elif tokens[0] == mypid: # if pid == mypid
        myvid = tokens[1] # store my vid
    
    line = fin.readline() # move to next line
    line = line.strip()
fin.close() # close vid file

# Learn L, it is the length of any vid
L = len(myvid)

myprintid = "VEIL_SWITCH: ["+mypid+'|'+myvid+']'

# Now start my serversocket to listen to the incoming packets         
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", myport))
server_socket.listen(5)
print myprintid, ' is now listening at port: ',myport

# create a server thread to take care of incoming messages:
server = Thread(target=serverThread,args=([server_socket]))
server.start()

round = 1

# Round 1: Put my physical neighbors' information in my routing table
for vid in vid2pid: # iterate for every vid in vid2pid list
    dist = delta(vid,myvid) #calculate logical distance XOR
    
    if dist not in routingTable:
        routingTable[dist] = [] # create dist level entry in routingTable
    
    bucket_len = len(routingTable[dist]) # no. of entries with dist in routingTable
    
    # int(X,2) converts binary X to decimal
    # getPrefix(myvid,dist), flips the dist^th bit and makes RHS of dist as * 
    #   eg. getPrefix('0101', 3) will return '00**'
    #	format[dist] = <Nexthop vid>, <gateway vid>, <prefix>
    bucket_info = [int(vid,2), int(myvid,2), getPrefix(myvid,dist)]    
    
    if not isDuplicateBucket(routingTable[dist], bucket_info):
        routingTable[dist].append(bucket_info) # add bucket_into to routingTable[dist]
        
while True:
    print myprintid, 'Starting Round #',round
    runARound(round)
    round = round + 1
    if round > L:
        round = L
    print '\n\t----> Routing Table at :',myvid,'|',mypid,' <----'
    for i in range(1,L+1):
        if i in routingTable:
            for j in routingTable[i]:
                print 'Bucket #', i, 'Nexthop:',bin2str(j[0],L), 'Gateway:',bin2str(j[1],L), 'Prefix:',j[2]
        else:
            print 'Bucket #',i,'  --- E M P T Y --- '
    print 'RDV STORE: ', rdvStore
    print '\n --  --  --  --  -- --  --  --  --  -- --  --  --  --  -- \n'
    sys.stdout.flush()
    time.sleep(ROUND_TIME) 
