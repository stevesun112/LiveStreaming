README v1.0
-------------------------------------------------
1. Directory structure
--------------------------------------------------

+ viro_sim_py (root folder)
-+ topology_workloads           // folder that contains various topologies and run files
--+ topologies           // contains two topologies (fat-tree-k2 and isp-level3) along with *.run.sh files
---+ small topologies       // contains four small topologies (4 node, 7 node, 8 node, 20 node)
--+ workloads_for_report    // contains *run.sh files based on "--+ topologies" folder, 
                  these files can be used for performance measurements, 
                  however not mandatory
                  
-- compile_all.py        // use this file to compile all python code files to generate (bytecode) *.pyc files
                  remember once compiled, add execute permission to all bytecode files by executing
                  "chmod 755 *.pyc" from the folder where you executed compile_all.py
-- constants.py         // contains variable declarations for packet type, etc., 
                  For this project, along with RDV_PUBLISH, RDV_QUERY, etc. 
                  you may want to add a new operation/packet type like DATA = 0x0000

-- plotTopo.py         // use this file to generate the graphical topology of the network 
                  using *.adlist and *.vid files (see section 3 below)
                  
-- traffic-gen.py         // *.run.sh file use the byte-code version of this file (ie. traffic-gen.pyc)
                  to insert data packets into the network as defined by the *.workload file
                  (see section 4) However most of the *workload.run.sh files include this. 
                  Hence unless you are writing your own topology or wanting to try some custom
                  pattern, you may not run this file separately. 
                  
-- veil.py           // contains various helper functions to support veil_switch.
                  Your project will require you to make some changes to this file 
                  (e.g. function createRDV_REPLY)
                  
-- veil_switch.py        // contains code for various algorithms like routing table construction, 
                  process packet, etc. Your project will require majority of the code 
                  additions/modifications to this file. 
                  
-- veil_switch_skeleton.txt   // provides details (pseudo-code) about several functions in veil_switch.py at a very high level

-- vid-assignment.py       // this file uses *.adlist file to assign vid to hosts. (see section 2 below)


NOTE: *.run.sh files:
These are shell executable files that help you run a number of commands together rather than you writing them one by one in the terminal.
The name of all such files will tell you a lot about its purpose. 

For example: 
 4.no.workload.run.sh - says it runs topology "4" with no workload (ie. no data packets in the network, only control packets)
 fat-tree-k2.test1.run - says it runs topology "fat-tree-k2" with 
             workload defined by "fat-tree-k2-test1.workload" file
 
DO NOT CHANGE ANY OF THE FOLDER NAMES PROVIDED TO YOU IN THE BASE VERSION UNLESS YOU KNOW WHAT YOU ARE DOING!
Since many of the *.run.sh files have relative paths defined in them that are based on these folder names, changing any of them may produce errors while execution.


-------------------------------------------------
2. How to Generate Vids for a Network
--------------------------------------------------

Given the adjacency list of a network, use the script "vid-assignment.py" to generate the vids for each node. For example, the following command takes file "4.adlist" as input and generate file "4.vid" which stores the vid mapping, assuming your current directory is "TOPOLOADS":

python ../vid-assignment.py 4.adlist 4.vid

-------------------------------------------------
3. Graphically Plot a Topology
--------------------------------------------------

Once you assign vids, you can use the script "plotTopo.py" to visualize the network. 
For example, use command "python plotTopo.py 4.adlist 4.vid" to generate "4.adlist.png". 
Visualization is not mandatory for the veil_switch to function, it just aides the user to view the topology.

NOTE #1: if plotTopo.py script gives you some errors, make sure you have installed graphviz package.
NOTE #2: use appropriate path while running this script

--------------------------------------------------
4. How to Test Your Code on Topologies with Workloads
--------------------------------------------------

First, please compile all Python source code to bytecode by executing "python compile_all.py", assuming you are using the Python emulator. If you are using Java, make sure to at least compile "traffic-gen.py", the traffic generator.

After compiling it is necessary to add execute permission to all the byte-code generated (*.pyc) files. Hence once you run compile_all.py, please execute on the terminal from the same folder "chmod 755 *.pyc".

There are two sets of scripts for each topology: one without workloads and one with workloads, e.g. "4.no.workload.run.sh" and "4.test1.run.sh" for the 4-node topology. Please open the two files, look for the differences, and run each of them. Change the scripts accordingly if you use Java. 

Note #1: The "veil_switch" emulator provided, although capable of routing DATA packets, does not generate data traffic. Instead, a separate script "traffic-gen.py" is provided to do this job. The script scans the input workload file (with extension "*.workload"), and keeps injecting data packets to its attached switch; and the data packets then get routed in the switch network. Don't try to rewrite this traffic generator in Java, just run this provided script.

Note #2: Each workload file (with extension "*.workload") has a 3-tuple schema: <source, destination, rate>. Open these files and see what is inside. File "fat-tree-k2.test1.workload" and file "isp-level3.test1.workload" contain only several Origin-Destination pairs for you to test/debug your code on the Fat-Tree topology and the Level-3 ISP topology respectively. The final workload files may contain much more O-D pairs.


--------------------------------------------------
5. How to Simulate Failures
--------------------------------------------------

To simulate the failures which would trigger fast re-routing, for simplicity let us only simulate "fatal" failures on a set of pre-specified nodes: i.e. (1) we consider only node failures, instead of link failures; (2) we specify which nodes to fail, at what times, in an additional argument for "veil_switch"; (3) once failed, a node will never come back.

To do this, first you have to add an additional argument for your "veil_switch" program. Suppose your command line is "veil_switch <adlist_file> <vid_file> <ip:port>", then you want to add an integer argument <fail_time> to the end:

veil_switch.pyc <adlist_file> <vid_file> <ip:port> <fail_time>

If fail_time==0, this switch never fails; if fail_time==15, it fails 15 seconds after it starts running.

In your "veil_switch" program, you may want to start a separate thread as a timer if fail_time>0: sleep(fail_time), and then terminate the current process for the switch. You may need to handle some exceptions because of the termination. Don't forget to save those statistics (useful in your report) before the switch fails.

--------------------------------------------------
6. Some useful tips (For Ubuntu users)
--------------------------------------------------

1. Terminate all running instances of veil_switches
  use command on terminal "pkill -f veil_switch"
  
2. To check open ports 
   use command on terminal "netstat -ntlp | grep LISTEN"
   
3. When you run any of the topology_run (.sh) files, and would like to record all the terminal output to a file, use the following command.
   Assuming you are in the folder where *run*.sh file is located, 
    use command "./fat-tree-k2.set1.run.sh > fat-tree-k2.set1.output &
    
    This will create a file "fat-tree-k2.set1.output" which will have all the terminal output given out by various veil_switch(es). After sometime, you can terminate all instances of veil_switches, thereby opening all the ports. You can now use this file to analyze several details.
    

================================================
- Last updated by Arvind (csci5221-s14-TA) on April 2, 2014

