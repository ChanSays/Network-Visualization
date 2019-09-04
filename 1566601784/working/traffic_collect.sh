# ### FIRST FILE IN SEQUENCE, NEXT IS TrafficParse.py


# PURPOSE: take traffic out per itgen run from specified log ie interface_uls-sanity97.log -> traffic_out/*

# for (( c=1; c<=$OUTLEN; c++ ))
# do  
#    echo "Welcome $c times"
# done

LOGFILE=$(ls -1 | grep -E "^.*\.log$")
TB_YML=$(ag -lig 'sanity.*testbed.yml')


# get log name
ag '(?<=TESTCASE )test.*(?=\")' $LOGFILE > out1 # has line numbers
ag 'Passed Arguments are' $LOGFILE > out2 # traffic params
ag 'PKTS' $LOGFILE > out3 
ag 'returndict before stop' $LOGFILE > out4
ag 'returndict after stop' $LOGFILE > out5
ag -lig 'sanity.*testbed.yml' . > logfile_name.txt

OUTLEN=$(cat out2 | wc -l)

rm -rf traffic_out && mkdir traffic_out
d=1
for (( c=1; c<=$OUTLEN; c++ ))
do
    # get testcase name
   var=""
   o2=$(awk "NR==($c)" out2)
   o3=$(awk "NR==($c)" out3)
   o4=$(awk "NR==($c)" out4)
   o5=$(awk "NR==($c)" out5)
    while [ $d -le $OUTLEN ]
    #for (( d=1; d<=$OUTLEN; d++ ))
        do
            TRAFF_NUM=$(echo $o2 | awk -F':' '{print $1}') # traffic_run line number ie 2798
            CASENUM=$(awk "NR==($d)" out1 | awk -F':' '{print $1}')
            
            
            #compare temp to TRAFF_NUM
            
            if [ "$CASENUM" -le "$TRAFF_NUM" ] 
            then
            echo "CASENUM: $CASENUM <= TRAFF_NUM: $TRAFF_NUM"
            cand=$CASENUM
            CASENXTNUM=$(awk "NR==($d+1)" out1 | awk -F':' '{print $1}')
                if [ "$TRAFF_NUM" -le "$CASENXTNUM" ]
                then
                    echo "TRAFF_NUM: $TRAFF_NUM <= CASENXTNUM: $next" 
                    echo "DONE"
                    CASE=$(awk "NR==($d)" out1 | awk -F':' '{print $2}')
                    CASENAME=$(echo $CASE | grep -oe "test.*\"")
                    break
                fi
            ((d++))
            else
            echo " is not less"
            
            fi 
    done
 # testcase_name >> traffic_out/traffic_run_$c
   echo $CASENAME >> traffic_out/traffic_run_$c
   echo $o2 >> traffic_out/traffic_run_$c
   echo $o3 >> traffic_out/traffic_run_$c
   echo $o4 >> traffic_out/traffic_run_$c
   echo $o5 >> traffic_out/traffic_run_$c

done
###############################################################

# get testcase name
 # compare to o1 testcase line numbers

# cat out1 | awk -F':' '{print $1}'
# if [ "$TEMP" -le "$TRAFF_NUM" ]; then print "$TEMP is less then"; fi
###############################################################


# OUTLEN=$(cat out2 | wc -l)

# for (( c=1; c<=$OUTLEN; c++ ))
# do
#     TRAFF_NUM=$(echo $o2 | awk -F':' '{print $1}') # traffic_run line number ie 2798
#     TEMP=$(awk "NR==($c)" out1 | awk -F':' '{print $1}')
#     CASE=$(awk "NR==($c)" out1 | awk -F':' '{print $2}')

#     #compare temp to TRAFF_NUM
    
#     if [ "$TEMP" -le "$TRAFF_NUM" ] 
#      then
#      echo " is less"
#      cand=$TEMP
#         if [ "$TRAFF_NUM" -le $(awk "NR==($c+1)" out1 | awk -F':' '{print $1}') ]
#         then
#             echo $cand 
#             echo "DONE"
#             CASENAME=$(echo $CASE | grep -oe "test.*\"")
#             break
#         fi
#      else
#      echo " is not less"
#     fi 

# done

###############################################################
