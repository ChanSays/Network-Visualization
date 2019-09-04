STEPS

cd /home/djangouser/Downloads/sigma/1566601784/working
bash traffic_collect.sh # create traffic_out/*
python TrafficParse.py # create traffic_json/*

=================
NOW
    
Node2Node links: DUT -> intf -> intf -> DUT
Traffic links : Itgen -> eth-> MAC -> MAC ->  intf -> DUT
Itgen2Node: Itgen -> eth ->  intf -> DUT


- create nodes for DUTs : tor1,tor2,node3,itgen
- get traffic profile for each traffic_run
- only have PKTS->json, need ReturnDictAfter->json to compare before/after send traffic


=================
STRETCH
combine each run into per testcase graph
