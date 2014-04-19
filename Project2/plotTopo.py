#!/usr/bin/python
import sys
import commands as cmd

if len(sys.argv) != 3:
    print 'Usage:',sys.argv[0],'<input-topo-adlist>','<vid-file>'
    sys.exit()

fin1 = open(sys.argv[1],'r')
fin2 = open(sys.argv[2],'r')
fout = open(sys.argv[1]+'.dot','w')
fout.write('graph G{\n')
line = fin2.readline()
line = line.strip()
while line!='':
    tokens = line.split(' ')
    #tokens[0] = tokens[0].replace(':','_')
    fout.write('"'+tokens[0]+'" [label="'+tokens[0].replace("localhost",'LH')+'('+tokens[1]+')"];\n')
    line = fin2.readline()
    line = line.strip()
fin2.close()

line = fin1.readline()
line = line.strip()
seen = {}
while line!='':
    #line = line.replace(':','_')
    tokens = line.split(' ')
    #line = line.replace(tokens[0],'')
    line = line.strip()
    seen[tokens[0]] = 1
    for s in seen:
        line = line.replace(s,'')
        line = line.replace('  ',' ')
        line = line.strip()
    source = tokens[0]
    tokens = line.split(' ')
    
    if line == '':
        line = fin1.readline()
        line = line.strip()
        continue
    for t in tokens:
        edge = '"'+source+'"--"'+t+'";\n'
        fout.write(edge)

    line = fin1.readline()
    line = line.strip()
fin1.close()
fout.write('}')
fout.close()

print cmd.getoutput('dot -Tpng '+sys.argv[1]+'.dot'+' -o '+sys.argv[1]+'.png')
