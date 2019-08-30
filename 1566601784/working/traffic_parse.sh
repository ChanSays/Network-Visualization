# PURPOSE: parse 

OUTLEN=$(cat out2 | wc -l)

for (( c=1; c<=$OUTLEN; c++ ))
do  
   echo "Welcome $c times"
   
   
python -c "
from os import environ
import re

lineList = [line.rstrip('\n') for line in open('traffic_out/traffic_run_$c')]; print(lineList[0])
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
                    print('len(i)!=1')
            else:
                print('len(i)!=1')
        else:
            print('NO ETHER-2')
except:
    pass
"

done

#environ["JAVA_HOME"] = "$(/usr/libexec/java_home)"
#v3 = re.split(',',val3) #split into packets

# lineList = [line.rstrip('\n') for line in open('traffic_run_1')]
# index: 0,1,2,3,4 
# test,args,pkts, rd_before, rd_after
    
            # {
        #     "color": "#36e236", 
        #     "label": "eth4", 
        #     "attributes": {
        #         "Modularity Class": "2", 
        #         "Number of Links": "10"
        #     }, 
        #     "y": 1843.6963, 
        #     "x": 460.43542, 
        #     "id": "itgen", 
        #     "size": 71.65969
        # }

        # {
        #     "color": "#36e236", 
        #     "label": "culture.gov.uk", 
        #     "attributes": {
        #         "Modularity Class": "2", 
        #         "Number of Pages": "1639"
        #     }, 
        #     "y": 1843.6963, 
        #     "x": 460.43542, 
        #     "id": "culture.gov.uk", 
        #     "size": 71.65969
        # }


        a="{
            'eth4': [<Ether dst=00:00:33:33:30:01 src=00:00:44:44:30:01 type=0x800 
        |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' 
        |>>>>, <Ether dst=00:00:33:33:30:02 src=00:00:44:44:30:02 type=0x800 
        |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' 
        |>>>>, <Ether dst=00:00:33:33:30:03 src=00:00:44:44:30:03 type=0x800 
        |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' 
        |>>>>, <Ether dst=00:00:33:33:30:04 src=00:00:44:44:30:04 type=0x800 
        |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' 
        |>>>>, <Ether dst=00:00:33:33:30:05 src=00:00:44:44:30:05 type=0x800 
        |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' 
        |>>>>, <Ether dst=00:00:33:33:30:06 src=00:00:44:44:30:06 type=0x800 
        |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' |>>>>, <Ether dst=00:00:33:33:30:07 src=00:00:44:44:30:07 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' |>>>>, <Ether dst=00:00:33:33:30:08 src=00:00:44:44:30:08 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' |>>>>, <Ether dst=00:00:33:33:30:09 src=00:00:44:44:30:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' |>>>>, <Ether dst=00:00:33:33:30:0A src=00:00:44:44:30:0A type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0000' |>>>>, <Ether dst=00:00:11:11:10:01 src=00:00:44:44:10:01 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:02 src=00:00:44:44:10:02 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:03 src=00:00:44:44:10:03 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:04 src=00:00:44:44:10:04 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:05 src=00:00:44:44:10:05 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:06 src=00:00:44:44:10:06 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:07 src=00:00:44:44:10:07 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:08 src=00:00:44:44:10:08 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:09 src=00:00:44:44:10:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:11:11:10:0A src=00:00:44:44:10:0A type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0002' |>>>>, <Ether dst=00:00:99:44:10:01 src=00:00:44:00:10:01 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:02 src=00:00:44:00:10:02 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:03 src=00:00:44:00:10:03 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:04 src=00:00:44:00:10:04 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:05 src=00:00:44:00:10:05 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:06 src=00:00:44:00:10:06 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:07 src=00:00:44:00:10:07 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:08 src=00:00:44:00:10:08 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:09 src=00:00:44:00:10:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>, <Ether dst=00:00:99:44:10:0A src=00:00:44:00:10:0A type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0006' |>>>>], 

        'eth3': [<Ether dst=00:00:44:44:30:01 src=00:00:33:33:30:01 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:02 src=00:00:33:33:30:02 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:03 src=00:00:33:33:30:03 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:04 src=00:00:33:33:30:04 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:05 src=00:00:33:33:30:05 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:06 src=00:00:33:33:30:06 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:07 src=00:00:33:33:30:07 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:08 src=00:00:33:33:30:08 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:09 src=00:00:33:33:30:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:44:44:30:0A src=00:00:33:33:30:0A type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0001' |>>>>, <Ether dst=00:00:11:11:20:01 src=00:00:33:33:20:01 type=0x8100 |<Dot1Q vlan=1 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:11:11:20:02 src=00:00:33:33:20:02 type=0x8100 |<Dot1Q vlan=2 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:11:11:20:03 src=00:00:33:33:20:03 type=0x8100 |<Dot1Q vlan=3 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:11:11:20:04 src=00:00:33:33:20:04 type=0x8100 |<Dot1Q vlan=4 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:11:11:20:05 src=00:00:33:33:20:05 type=0x8100 |<Dot1Q vlan=5 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:11:11:20:06 src=00:00:33:33:20:06 type=0x8100 |<Dot1Q vlan=6 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:11:11:20:07 src=00:00:33:33:20:07 type=0x8100 |<Dot1Q vlan=7 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:11:11:20:08 src=00:00:33:33:20:08 type=0x8100 |<Dot1Q vlan=8 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:11:11:20:09 src=00:00:33:33:20:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0004' |>>>>, <Ether dst=00:00:11:11:20:0A src=00:00:33:33:20:0A type=0x8100 |<Dot1Q vlan=10 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0004' |>>>>>, <Ether dst=00:00:99:33:10:01 src=00:00:33:00:10:01 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:02 src=00:00:33:00:10:02 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:03 src=00:00:33:00:10:03 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:04 src=00:00:33:00:10:04 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:05 src=00:00:33:00:10:05 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:06 src=00:00:33:00:10:06 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:07 src=00:00:33:00:10:07 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:08 src=00:00:33:00:10:08 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:09 src=00:00:33:00:10:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>, <Ether dst=00:00:99:33:10:0A src=00:00:33:00:10:0A type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0007' |>>>>],
        
         'eth1': [<Ether dst=00:00:44:44:10:01 src=00:00:11:11:10:01 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:02 src=00:00:11:11:10:02 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:03 src=00:00:11:11:10:03 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:04 src=00:00:11:11:10:04 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:05 src=00:00:11:11:10:05 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:06 src=00:00:11:11:10:06 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:07 src=00:00:11:11:10:07 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:08 src=00:00:11:11:10:08 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:09 src=00:00:11:11:10:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:44:44:10:0A src=00:00:11:11:10:0A type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0003' |>>>>, <Ether dst=00:00:33:33:20:01 src=00:00:11:11:20:01 type=0x8100 |<Dot1Q vlan=1 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:33:33:20:02 src=00:00:11:11:20:02 type=0x8100 |<Dot1Q vlan=2 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:33:33:20:03 src=00:00:11:11:20:03 type=0x8100 |<Dot1Q vlan=3 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:33:33:20:04 src=00:00:11:11:20:04 type=0x8100 |<Dot1Q vlan=4 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:33:33:20:05 src=00:00:11:11:20:05 type=0x8100 |<Dot1Q vlan=5 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:33:33:20:06 src=00:00:11:11:20:06 type=0x8100 |<Dot1Q vlan=6 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:33:33:20:07 src=00:00:11:11:20:07 type=0x8100 |<Dot1Q vlan=7 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:33:33:20:08 src=00:00:11:11:20:08 type=0x8100 |<Dot1Q vlan=8 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:33:33:20:09 src=00:00:11:11:20:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0005' |>>>>, <Ether dst=00:00:33:33:20:0A src=00:00:11:11:20:0A type=0x8100 |<Dot1Q vlan=10 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='0000000000000000000000PGID0005' |>>>>>, <Ether dst=00:00:99:11:10:01 src=00:00:11:00:10:01 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:02 src=00:00:11:00:10:02 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:03 src=00:00:11:00:10:03 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:04 src=00:00:11:00:10:04 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:05 src=00:00:11:00:10:05 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:06 src=00:00:11:00:10:06 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:07 src=00:00:11:00:10:07 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:08 src=00:00:11:00:10:08 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:09 src=00:00:11:00:10:09 type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>, <Ether dst=00:00:99:11:10:0A src=00:00:11:00:10:0A type=0x800 |<IP src=172.17.1.1 dst=172.17.2.1 |<Padding |<Raw load='00000000000000000000000000PGID0008' |>>>>]
         }"