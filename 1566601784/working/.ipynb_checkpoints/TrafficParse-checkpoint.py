
import os,sys
from os import environ
import re
import subprocess
import random
import math
import json

# PURPOSE: parses traffic_run_* files from traffic_out into json in traffic_jsons


def json_gen(v3,json_file):

    number_of_colors = 1
    # choose color based on eth


    regex = r"((?:\w|\.|\:|\')*)\=((?:\w|\.|\:|\')*)" # all *=* vals
    regex1 = r"((?:[a-fA-F0-9]{2}:)+[a-fA-F0-9]{2})" # mac addr only, no ip match
    regex2 = r"((?<=\<)\w*)" # get < items
    regex3 = r"((?:\w|\.|\:|\'|\s)*)\=((?:\w|\.|\:|\')*)" #get < items best


    nodes=[]
    edges=[]
    json_obj={}
    i=0
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
                        node_attr[spl[0]]=spl[1]
                #         edge_attr[spl[0]]=spl[1]
                node['color'.replace("'", '"')] = "#"+"%06x" % random.randint(0, 0xFFFFFF)      
                node['attributes']=node_attr
                node['channel']=curr_eth
                node['x']= random.randint(-4000,4000)
                node['y']= random.randint(-4000,4000)
                node['size']= random.randint(100,500)
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



    json_obj['nodes']=nodes
    json_obj['edges']=edges

    #generate json file for each traffic_run
    with open(json_file,'w') as f:
        json.dump(json_obj ,f)


def main():

    os.system("rm -rf traffic_json && mkdir traffic_json")

    cmd = "cat out2 | wc -l"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = output.decode('ASCII').rstrip(os.linesep)
    print(output)

    
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