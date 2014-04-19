import socket, struct,sys,random
#from collections  import namedtuple

# Local imports 
from constants import * # for the constants.


# convert a string containing mac address into a byte array
def getMacArray(mac):
    mac_array=[0]*6
    macbytes = mac.split(":")
    if len(macbytes) != 6:
        print 'Error: MalFormed mac, expected 6 bytes, found : ',len(macbytes),'bytes in the input array: ',mac
    #t 'macbytes: ', macbytes
    for i in range (0,6):
        if i < len(macbytes):
            mac_array[i] = int (macbytes[i],16)
    return mac_array
     
# convert a byte array into the string format            
def getMacHexString(bytes):
    macstring = ''
    #print "Converting Bytes: ", bytes
    for i in range(0,6):
        #print 'Bytes[i] = ', bytes[i]
        #print 'hex = ', hex(bytes[i])
        s = hex(bytes[i]).replace('0x','')
        if len(s) < 2:
            s = '0' + s
        macstring = macstring + s
        if i < 5:
            macstring = macstring+':'
    return macstring

# Extract the operation from the packet
def getOperation(packet):
    operation = (struct.unpack('!H',packet[OPER_OFFSET: OPER_OFFSET+OPER_LEN]))[0]
    return operation

# creates an arp packet, OPER is the operation, mac_src is the source mac address as string, ip_src is the source ip as string
def createARPPacket(OPER,mac_src,ip_src,mac_dst,ip_dst):
    ip_src_num = socket.inet_aton(ip_src)
    ip_dst_num = socket.inet_aton(ip_dst)
    mac_src_array = getMacArray(mac_src)
    mac_dst_array = getMacArray(mac_dst)
    arppacket = struct.pack("!HHBBHBBBBBB4sBBBBBB4s",HTYPE,PTYPE,HLEN,PLEN,OPER,mac_src_array[0],mac_src_array[1],mac_src_array[2],mac_src_array[3],mac_src_array[4],mac_src_array[5],ip_src_num, mac_dst_array[0], mac_dst_array[1], mac_dst_array[2], mac_dst_array[3], mac_dst_array[4], mac_dst_array[5], ip_dst_num)
    return arppacket

# creates the switchRegistrationReplyPacket
def createSwitchRegistrationReplyPacket(switchvid):
    srcvid_array = getMacArray(VEIL_MASTER)
    srcdst_array = getMacArray(switchvid)    
    registrationreply = struct.pack("!HHBBHBBBBBBBBBBBB",HTYPE,PTYPE,HLEN,PLEN,SWITCH_REGISTER_REPLY,srcvid_array[0],srcvid_array[1],srcvid_array[2],srcvid_array[3],srcvid_array[4],srcvid_array[5], srcdst_array[0], srcdst_array[1], srcdst_array[2], srcdst_array[3], srcdst_array[4], srcdst_array[5])
    return registrationreply
# convert operation number into a string
def getOperationName(operation):
    if operation in OPERATION_NAMES:
        return OPERATION_NAMES[operation]
    else:
        return 'UNKNOWN OPERATION'
    
# create echo_request packet:
def createEchoRequestPacket(srcvid,dstvid):
    #Packet Structure
    #HTYPE PTYPE HLEN PLEN OPER SRC_VID(48) DST_VID(48)
    srcvid_array = getMacArray(srcvid)
    srcdst_array = getMacArray(dstvid)    
    echorequest = struct.pack("!HHBBHBBBBBBBBBBBB",HTYPE,PTYPE,HLEN,PLEN,ECHO_REQUEST,srcvid_array[0],srcvid_array[1],srcvid_array[2],srcvid_array[3],srcvid_array[4],srcvid_array[5], srcdst_array[0], srcdst_array[1], srcdst_array[2], srcdst_array[3], srcdst_array[4], srcdst_array[5])
    return echorequest

# create echo_request packet:
def createEchoReplyPacket(srcvid,dstvid):
    srcvid_array = getMacArray(srcvid)
    srcdst_array = getMacArray(dstvid)    
    echoreply = struct.pack("!HHBBHBBBBBBBBBBBB",HTYPE,PTYPE,HLEN,PLEN,ECHO_REPLY,srcvid_array[0],srcvid_array[1],srcvid_array[2],srcvid_array[3],srcvid_array[4],srcvid_array[5], srcdst_array[0], srcdst_array[1], srcdst_array[2], srcdst_array[3], srcdst_array[4], srcdst_array[5])
    return echoreply

# create registration reply packet:
def createSwitchRegistrationReplyPacket1(srcvid,dstvid):
    srcvid_array = getMacArray(srcvid)
    srcdst_array = getMacArray(dstvid)    
    reply = struct.pack("!HHBBHBBBBBBBBBBBB",HTYPE,PTYPE,HLEN,PLEN,SWITCH_REGISTER_REPLY,srcvid_array[0],srcvid_array[1],srcvid_array[2],srcvid_array[3],srcvid_array[4],srcvid_array[5], srcdst_array[0], srcdst_array[1], srcdst_array[2], srcdst_array[3], srcdst_array[4], srcdst_array[5])
    return reply
# create a store_request packet:
def createStorePacket(ip_to_store,vid_to_store,src_vid,dst_vid):
    # Packet Structure
    # HTYPE PTYPE HLEN PLEN OPER SRC_VID(48) DST_VID(48) IP_TO_STORE(32) VID_TO_STORE(48)
    #print 'Source VID: ', src_vid, 'Destination VID: ', dst_vid, ' IP to store: ', ip_to_store, 'vid to store: ', vid_to_store
    ipnum = socket.inet_aton(ip_to_store)
    vid_array = getMacArray(vid_to_store)
    src_vid_array = getMacArray(src_vid)
    dst_vid_array = getMacArray(dst_vid)
    # First prepare header
    store_packet = struct.pack("!HHBBH",HTYPE,PTYPE,HLEN,PLEN,STORE_REQUEST)
    #print 'StorePACKET = ',store_packet.encode('hex')
    # Put the source vid now
    store_packet = store_packet+struct.pack("!BBBBBB",src_vid_array[0],src_vid_array[1],src_vid_array[2],src_vid_array[3],src_vid_array[4],src_vid_array[5])
    #print 'StorePACKET = ',store_packet.encode('hex')
    # Put the destination vid now
    store_packet = store_packet+struct.pack("!BBBBBB",dst_vid_array[0],dst_vid_array[1],dst_vid_array[2],dst_vid_array[3],dst_vid_array[4],dst_vid_array[5])
    #print 'StorePACKET = ',store_packet.encode('hex')
    # Put the IP on the packet now
    store_packet = store_packet + struct.pack("!4s",ipnum)
    #print 'StorePACKET = ',store_packet.encode('hex')
    # Put the vid on the packet now
    store_packet = store_packet + struct.pack("!BBBBBB",vid_array[0],vid_array[1],vid_array[2],vid_array[3],vid_array[4],vid_array[5])    
    #print 'StorePACKET = ',store_packet.encode('hex')
    return store_packet

# extract IP/VID mapping to store:
def extractIPtoStore(store_request_packet):
    #print 'start offset: ',ECHO_SRC_OFFSET+2*HLEN
    #print 'end offset: ', ECHO_SRC_OFFSET+2*HLEN +PLEN
    #print 'String buffer: ', store_request_packet[ECHO_SRC_OFFSET+2*HLEN:ECHO_SRC_OFFSET+2*HLEN+PLEN]
    ipnum = struct.unpack("!4s",store_request_packet[ECHO_SRC_OFFSET+2*HLEN:ECHO_SRC_OFFSET+2*HLEN+PLEN])
    return socket.inet_ntoa(ipnum[0])

def extractVIDtoStore(store_request_packet):
    vid = struct.unpack("!BBBBBB",store_request_packet[ECHO_SRC_OFFSET+2*HLEN+PLEN:ECHO_SRC_OFFSET+3*HLEN+PLEN])
    return getMacHexString(vid)

# extract source  vid from echopacket
def extractEchoSrc(echopacket):
    srcvid = struct.unpack("!BBBBBB", echopacket[ECHO_SRC_OFFSET:ECHO_SRC_OFFSET+HLEN])
    return getMacHexString(srcvid)

# extract source vid from echopacket
def extractEchoDst(echopacket):
    dstvid = struct.unpack("!BBBBBB", echopacket[ECHO_SRC_OFFSET+HLEN:ECHO_SRC_OFFSET+2*HLEN])
    return getMacHexString(dstvid)

# extract source vid from echopacket
def extractARPSrcMac(arppacket):
    srcmac = struct.unpack("!BBBBBB", arppacket[ECHO_SRC_OFFSET:ECHO_SRC_OFFSET+HLEN])
    return getMacHexString(srcmac)

# extract source vid from echopacket
def extractARPDstMac(arppacket):
    mac = struct.unpack("!BBBBBB", arppacket[ECHO_SRC_OFFSET+HLEN+PLEN:ECHO_SRC_OFFSET+2*HLEN+PLEN])
    return getMacHexString(mac)

# extract IP addresses
def extractARPDstIP(arppacket):
    ip = struct.unpack("!4s", arppacket[ECHO_SRC_OFFSET+2*HLEN+PLEN:ECHO_SRC_OFFSET+2*HLEN+2*PLEN])
    ipaddress = socket.inet_ntoa(ip[0])
    return ipaddress   
def extractARPSrcIP(arppacket):
    ip = struct.unpack("!4s", arppacket[ECHO_SRC_OFFSET+HLEN:ECHO_SRC_OFFSET+HLEN+PLEN])
    ipaddress = socket.inet_ntoa(ip[0])
    return ipaddress  

# extract an IP address at a give offset
def extractIP(packet,offset):
    ip = struct.unpack("!4s", packet[offset:offset+PLEN])
    ipaddress = socket.inet_ntoa(ip[0])
    return ipaddress     

# extract a MAC address at a give offset
def extractMAC(packet,offset):
    mac = struct.unpack("!BBBBBB", packet[offset:offset+HLEN])
    return getMacHexString(mac) 

# receives a packet from a tcp socket, waits till it receives NULL
def receivePacket(sock):
    #print 'Receiving packet at socket: ',sock
    data = sock.recv(128)
    #print 'data received: ', data.encode("hex")
    '''packet = ''
    while data != '':
        packet = packet+data
        data = sock.recv(64)
        print 'data received: ', data'''
    return data

# Method for switch registration
def register_switch(veil_master_ip,veil_master_port,serverport):
    # Packet structure 
    # HTYPE PTYPE HLEN PLEN OPER SRCVID(48bit) DSTVID(48bit) TCPPORT(16bit)
    print 'Register switch at port: ',serverport, ' with VEIL_MASTER IP: ',veil_master_ip, ' VEIL_MASTER PORT: ',veil_master_port
    registration_packet =  struct.pack("!HHBBH",HTYPE,PTYPE,HLEN,PLEN,SWITCH_REGISTER_REQUEST)
    srcvid_array = getMacArray("ff:ff:ff:ff:ff:ff")
    registration_packet = registration_packet + struct.pack("!BBBBBB",srcvid_array[0],srcvid_array[1],srcvid_array[2],srcvid_array[3],srcvid_array[4],srcvid_array[5])
    dstvid_array = getMacArray(VEIL_MASTER)
    registration_packet = registration_packet + struct.pack("!BBBBBB",dstvid_array[0],dstvid_array[1],dstvid_array[2],dstvid_array[3],dstvid_array[4],dstvid_array[5])
    registration_packet = registration_packet + struct.pack("!H",serverport)
    print 'Registration packet to be sent: ', registration_packet.encode("hex")
    sock_master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_master.connect((veil_master_ip, veil_master_port))  
    sock_master.send(registration_packet)
    registration_reply = receivePacket(sock_master)
    print 'Registration packet reply to be received: ', registration_reply.encode("hex")
    sock_master.close()
    return extractMAC(registration_reply, ECHO_SRC_OFFSET+HLEN)

# Gets a new ID for the switch. Basically generates a 32-bit random integer and checks if its in use or not
def getANewSwitchID(current_ids):
    MAXID = 2**32-1
    if len(current_ids) == MAXID:
        print 'ERROR: NO more IDS left!'
        return 0
    #random.seed(1)
    id = random.randint(1,MAXID)
    while id in current_ids:
        id = random.randint(1,MAXID)
    return id

# converts an ID (32-bit number) into a VID format    
def switchID2Vid(id): 
    vid = '00:00'
    id_str = hex(id).replace('0x','')
    id_str = id_str.lower()
    id_str = id_str.replace('l','')
    
    while len(id_str) < 8:
        id_str = '0' + id_str
    vid = id_str[0:2] + ':' + id_str[2:4] + ':' + id_str[4:6] + ':' + id_str[6:8] + ':' + vid
    return vid  

# This function determines the ID for the access switch.
def  getAccessSwitchID(ip,ids):
    MAXINT = 2**32 -1
    RADIUS = 2**31
    if len(ids) == 0:
        return 0
    hashval = hash(ip)%(MAXINT+1)
    mindiff = MAXINT
    accessSwitchID = 0
    for id in ids:
        diff = abs(hashval - id)%(RADIUS)
        if diff < mindiff:
            accessSwitchID = id
            mindiff = diff
    return accessSwitchID

# Generates a unique host-vid
def getAVid(ip,mac,mySwitch_vid,myHost_ids):
    MAX_HOSTID = 2**16-1
    hostid = ''
    for i in range (1, MAX_HOSTID+1):
        if i not in myHost_ids:
            break
    if i == MAX_HOSTID:
        print 'Warning: All the VIDs are currently in use!'
        hostid = "ff:ff"
    else:
        myHost_ids.append(i)
        id = hex(i).replace("0x",'')
        while len(id) < 4:
            id = '0'+id
        hostid = id[0:2]+':'+id[2:4]
    bytes = mySwitch_vid.split(":")
    vid = bytes[0]+":"+bytes[1]+":"+bytes[2]+":"+bytes[3]+":"+hostid
    return vid 

# get the prefix of kth bucket for a node myvid
def getPrefix(vid,dist):
    L = len(vid)
    prefix = vid[:L - dist]
    # flip the dist-1 th bit from the right
    if vid[L-dist] == '0':
        prefix = prefix + '1'
    else:
        prefix = prefix + '0'
    prefix = prefix + (dist-1)*'*'
    return prefix

# check if the bucket is already present in the set or not:
def isDuplicateBucket(bucketlist,bucket):
    isduplicate = False
    for i in range(0, len(bucketlist)):
        if bucketlist[i][0] == bucket[0] and bucketlist[i][1] == bucket[1] and bucketlist[i][2] == bucket[2]:
            isduplicate = True
            return isduplicate
    return isduplicate

# returns the rendezvousID for a node 
def getRendezvousID(dist,myvid):
    L = len(myvid)
    rdvid = myvid[:L-dist+1]
    rdvid = rdvid + hashval(rdvid,dist-1)
    return rdvid

# returns the k character long string containing hash of the input value
def hashval(key, length):
    return length*'0'

# creates a packet of type RDV_PUBLISH
def createRDV_PUBLISH(bucket,myvid,dst):
    # First prepare header
    packet = struct.pack("!HHBBH",HTYPE,PTYPE,HLEN,PLEN,RDV_PUBLISH)
    # Sender VID (32 bits)
    svid = struct.pack("!I",int(myvid,2))    
    # Desitnation VID (32 bits)
    dvid = struct.pack("!I",int(dst,2))
    # Destination Subtree-k
    z = struct.pack("!I",bucket[0])
    return (packet+svid+dvid+z)

# create a RDV_REPLY Pakcet
# GW IS AN INT HERE! AND REST ARE BINARY STRINGS
def createRDV_REPLY(gw,bucket_dist,myvid, dst):
    # First prepare header
    packet = struct.pack("!HHBBH",HTYPE,PTYPE,HLEN,PLEN,RDV_REPLY)
    # Sender VID (32 bits)
    svid = struct.pack("!I",int(myvid,2))    
    # Desitnation VID (32 bits)
    dvid = struct.pack("!I",int(dst,2))
    
    #bucket distance
    buck_dist = struct.pack("!I",bucket_dist)
    
    # Destination Subtree-k
    z = struct.pack("!I",gw)
    return (packet+svid+dvid+buck_dist+z)    

# create a RDV_QUERY Pakcet
# bucket_dist IS AN INT HERE! AND REST ARE BINARY STRINGS
def createRDV_QUERY(bucket_dist,myvid, dst):
    # First prepare header
    packet = struct.pack("!HHBBH",HTYPE,PTYPE,HLEN,PLEN,RDV_QUERY)
    # Sender VID (32 bits)
    svid = struct.pack("!I",int(myvid,2))    
    # Desitnation VID (32 bits)
    dvid = struct.pack("!I",int(dst,2))
    # Destination Subtree-k
    z = struct.pack("!I",bucket_dist)
    return (packet+svid+dvid+z)      

# it flips the kth bit (from the right) in the dst and returns it.   
def flipBit(dst,dist):
    L = len(dst)
    prefix = dst[:L-dist]
    if dst[L-dist] == '0':
        prefix = prefix + '1'
    else:
        prefix = prefix + '0'
    prefix = prefix + dst[L-dist+1:]
    return prefix  

# udpate the destination on the packet
def updateDestination(packet,dst):
    header = packet[:8]
    sender = packet[8:12]
    payload = packet[16:]
    newdest = struct.pack("!I",int(dst,2))
    return (header+sender+newdest+payload)   
        
        
# returns the destination in the string format
def getDest(packet,L):
    t = struct.unpack("!I", packet[12:16])
    dest = bin2str(t[0],L)
    return dest

# prints the packet content
def printPacket(packet,L):
    [opcode] = struct.unpack("!H", packet[6:8])
    [svid] = struct.unpack("!I", packet[8:12])
    [dvid] = struct.unpack("!I", packet[12:16])
    [payload] = struct.unpack("!I", packet[16:20])
    
    if opcode not in OPERATION_NAMES:
        print 'Unknown packet opcode: ',hex(opcode)
        print 'Content in hexadecimal: ', packet.encode("hex")
        return
    print 'Type: ',OPERATION_NAMES[opcode], 'Source: ', bin2str(svid,L), 'Destination: ', bin2str(dvid,L), 'Payload: ',bin2str(payload,L)
    
# converts the binary representation of an integer to binary string.
def bin2str(id, L):
    binstr = bin(id)
    binstr = binstr.replace('0b','')
    binstr = (L-len(binstr))*'0' + binstr
    return binstr
    

# logical distance 
def delta(vid1,vid2):
    L = len(vid1)
    dist = L
    for i in range(0,L):
        if vid1[i] == vid2[i]:
            dist = dist -1
        else:
            return dist
    return dist           