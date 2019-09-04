
import os,sys
from os import environ
import re
import subprocess
import random
import math
import json
import yaml
# PURPOSE: parses traffic_run_* files from traffic_out into json in traffic_jsons

g_node_dict={}

def nodeDictCreate():
    f=open("logfile_name.txt", "r")
    tb_yml=f.read()
    tb_yml=tb_yml.rstrip('\n')
#     tb_yml
    with open(tb_yml, 'r') as stream:
        try:
            parsed_yml = yaml.safe_load(stream)
#             print(yaml.safe_load(stream))
            global g_node_dict
            g_node_dict = parsed_yml['node_dict']
        except yaml.YAMLError as exc:
            print(exc)
    
        
def json_gen(v3,json_file):

    number_of_colors = 1
    # choose color based on eth
#     nodeDictCreate()
    global g_node_dict
#     print(g_node_dict)
    regex = r"((?:\w|\.|\:|\')*)\=((?:\w|\.|\:|\')*)" # all *=* vals
    regex1 = r"((?:[a-fA-F0-9]{2}:)+[a-fA-F0-9]{2})" # mac addr only, no ip match
    regex2 = r"((?<=\<)\w*)" # get < items
    regex3 = r"((?:\w|\.|\:|\'|\s)*)\=((?:\w|\.|\:|\')*)" #get < items best


    nodes=[]
    edges=[]
    json_obj={}
    i=0
    nodes = nodeGen(nodes) # after appending tor1 etc.
    nodes = intfGen(nodes)
    
    for v3item in v3: 
        for key in v3item: # eth1,eth2..
            color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
            col = color[0] #rand color
            curr_eth= key
            for test_str in v3item[key]: # pkt in [pkt,pkt..]

                matches = re.finditer(regex3, test_str)
    #             print("\n\nNEW PKT\n\n") #make new json obj now
                


                node={}
                edge={}
                node_attr={}
                edge_attr={}
                for matchNum, match in enumerate(matches, start=1):


                    s1 = match.group().strip()
                    spl = s1.split("=")
                #     print(spl)
                    dic = {}

                    if len(spl)==2:
                        dic[spl[0].replace('"', "'") ]=spl[1].replace('"', "'") 


                    if spl[0]=='src':
                        #append to label,id source
                        node["label"]=spl[1]
                        node["id"]=spl[1]
                        edge["source"]=spl[1]

                    elif spl[0]=='Ether dst':
                        edge['target']=spl[1]
                    elif spl[0]=='Raw load':
                        pass
                    else:
                        # append to attr
#                         node_attr[spl[0]]=spl[1]
                        pass
                #         edge_attr[spl[0]]=spl[1]
                node['color'.replace("'", '"')] = "#"+"%06x" % random.randint(0, 0xFFFFFF)      
                node['attributes']=node_attr
                node['channel']=curr_eth
                node['x']= random.randint(-4000,4000)
                node['y']= random.randint(-4000,4000)
#                 node['size']= random.randint(100,300)
                node["size"] = random.randint(2, 10)
                edge['id']= 'e'+str(i)
                i+=1
                edge['weight'] = random.randint(20,200)
                edge['label']=''
                #     edge['attr']=edge_attr
                nodes.append(node)
                edges.append(edge)

                for groupNum in range(0, len(match.groups())):

                    groupNum = groupNum + 1

                    if matchNum==1 and groupNum==1:
                        label= match.group(groupNum).strip() # mac addr
                        id_obj= match.group(groupNum).strip()

    
#     dut_nodes = nodeGen()

    json_obj['nodes']=nodes
    json_obj['edges']=edges

    #generate json file for each traffic_run
    with open(json_file,'w') as f:
        json.dump(json_obj ,f)

def profileGen():
    p1='profile_l2_sanity'
    p2='profile_vxlan_access'
    curr_tb = 'sanity97-testbed.yml'
    old_profile= 'old_profile.yml'
    new_profile = 'new_profile.yml'

    # create new traffic profile
    cmd_prof_find = "sed -n '/"+p1+"/,/profile/p' " + curr_tb + ' > '+old_profile + " && sed -e '$ d' "+old_profile+" > "+new_profile

    # 
    cmd_exist_prof = "ag -g '"+p1+".yml' > res.txt"

    # 
    cmd_file_size = "wc -l < res.txt"
    cmd_file_size
    
#     cmd = "cat out2 | wc -l"  
    pop_res = subprocess.Popen(cmd_prof_find,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = pop_res.communicate()[0]
    output = output.decode('ASCII').rstrip(os.linesep)
    print(output)

def jsonifySanityDict():
    # ['node01', 'node02', 'node03', 'tgn']
    global g_node_dict
    for i in list(g_node_dict.keys()):
    #     curr_node_dict = i+'_dict'

        intf_list=list(g_node_dict[i]['interfaces'].values())
    #     print(intf_list)
        new_intf_dict = {}

        for j in intf_list:
            j = j.split(" ")
    #         print(i)
            intf_name=j[1]
    #         print(intf_name)
            attr_list1=j[2:]
            attr_list2=[]
            for k in attr_list1:
                k=k.replace("-","")
                attr_list2.append(k)
    #             print(k)

    #         print(attr_list1)
    #         print(attr_list2)
            it = iter(attr_list2)
            attr = dict(zip(it, it))
    #         print(b)
            new_intf= dict({intf_name:attr})
            new_intf_dict[intf_name]=attr
    #         print(new_intf)
    #   print(new_intf_dict)
        g_node_dict[i]['interfaces']=new_intf_dict
    print(g_node_dict[i])
    #     print("\n\n\n")
    
def intfGen(node_lst):
    # create Eth1/5 json
    # create eth4 json
    try:
        global g_node_dict
        for curr_node in g_node_dict.keys():
            for i in g_node_dict[curr_node]["interfaces"]:
                curr_intf = i  # ie Eth2/1
                #     print(curr_intf)
                peer = (
                    g_node_dict[curr_node]["interfaces"][i]["peer_device"]
                    + "-"
                    + g_node_dict[curr_node]["interfaces"][i]["peer_interface"]
                )  # ie node02-Eth2/1
                #     print(peer) # node02-Eth2/1

                node = {}
                edge = {}
                node_attr = {}
                edge_attr = {}


                node["label"] = str(peer)
                node["id"] = str(peer)
                node["color".replace("'", '"')] = "#" + "%06x" % random.randint(0, 0xFFFFFF)
                node["attributes"] = node_attr
                node["channel"] = None
                node["x"] = random.randint(-18000, -10000)
                node["y"] = random.randint(-18000, -10000)
                node["size"] = random.randint(2, 10)
        #         print(node)

                node_lst.append(node)
    except Exception as exc:
        print(exc)
        

    return node_lst    
    
def nodeGen(node_lst):
    # create node01 json
    # create tgn json
    global g_node_dict
    for i in g_node_dict.keys():
        node = {}
        edge = {}
        node_attr = {}
        edge_attr = {}

#         node_attr = g_node_dict[i]

        node["label"] = str(i)
        node["id"] = str(i)
        node["color".replace("'", '"')] = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        node["attributes"] = node_attr
        node["channel"] = ''
        node["x"] = random.randint(-8000, -5000)
        node["y"] = random.randint(5000, 8000)
        node["size"] = random.randint(100, 100)
        
        node_lst.append(node)
        
    return node_lst

def main():

    os.system("rm -rf traffic_json && mkdir traffic_json")
    
    nodeDictCreate()
    global g_node_dict
    
    jsonifySanityDict()
    
    cmd = "cat out2 | wc -l"  
    ps = "cat out2 | wc -l"  
    pop_res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = pop_res.communicate()[0]
    output = output.decode('ASCII').rstrip(os.linesep)
#     print(output)

    
    environ['OUTLEN']=output

    OUTLEN = int(environ['OUTLEN'])

    for i in range(1,OUTLEN+1):
        #print('traffic_run_'+str(ex_list[i]))
        traff_file = 'traffic_out/traffic_run_'
        traff_file += str(i)
        json_file = 'traffic_json/json_run_' + str(i)

        lineList = [line.rstrip('\n') for line in open(traff_file)]
#         print(lineList[0])
        test=lineList[0] #casename
        args=lineList[1] #params
        pkts=lineList[2] #PKTS
        rd_before=lineList[3] # returndict before stop
        rd_after=lineList[4] # returndict after stop
        
        val1 = [i for i in test.split('\"') if i][0]
        val2 = args.split('Namespace')[1]
        val3 = pkts.split('PKTS ')[1]
        val4 = rd_before.split('stop ')[1]
        val5 = rd_after.split('stop ')[1]


        # packet processing
        v3 = re.split("('eth[0-9]')",val3) # split by eth
        del v3[0]
        new_v3=[]
        pckt_lst=[]

        try:
            for x in range(0, len(v3)):
                i = v3[x]
                if 'Ether' in i:
                    # is packet
                    i = i.split(': [')

                    i = [i1 for i1 in i if i1]
                    #print(i, end = '\n\n')
                    if len(i)==1:
                        # rem extra punc
                        i = i[0].split('], ')
                        i = i[0].split(']}')
                        i = [i1 for i1 in i if i1]
                        #print(i, end = '\n\n')
                        if len(i)==1:
                            x1=i[0].split(',') #pckts done

                            v3[x]= dict({v3[x-1].replace("'",""): x1})
                            del v3[x-1]
                            #new_v3+=i
                            #print(new_v3)
                            #print(i, end = '\n\n')
                        else:
#                             print('len(i)!=1')
                            pass
                    else:
#                         print('len(i)!=1')
                        pass
                else:
#                     print('NO ETHER-2')
                    pass
        except:
            pass
        
        
        # generate json
        json_gen(v3,json_file)

if __name__ == "__main__" :
    main()