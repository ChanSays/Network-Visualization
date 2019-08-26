# for (( c=1; c<=$OUTLEN; c++ ))
# do  
#    echo "Welcome $c times"
# done


OUTLEN=$(cat out2 | wc -l)

rm -rf traffic_out && mkdir traffic_out

for (( c=1; c<=$OUTLEN; c++ ))
do
    # get testcase name
   var=""
   o2=$(awk "NR==($c)" out2)
   o3=$(awk "NR==($c)" out3)
   o4=$(awk "NR==($c)" out4)
   o5=$(awk "NR==($c)" out5)
 # testcase_name >> traffic_out/traffic_run_$c
   echo $o2 >> traffic_out/traffic_run_$c
   echo $o3 >> traffic_out/traffic_run_$c
   echo $o4 >> traffic_out/traffic_run_$c
   echo $o5 >> traffic_out/traffic_run_$c

done
###############################################################

# get testcase name
TRAFF_NUM=$(echo $o2 | awk -F':' '{print $1}') # traffic_run line number ie 2798
 # compare to o1 testcase line numbers

# cat out1 | awk -F':' '{print $1}'

for (( c=1; c<=$OUTLEN; c++ ))
do
    TEMP=$(awk "NR==($c)" out1 | awk -F':' '{print $1}')
    #compare temp to TRAFF_NUM
    
    if [ "$TEMP" -le "$TRAFF_NUM" ]
     then
     echo " is less"
     cand=$TEMP
        if [ "$TRAFF_NUM" -le $(awk "NR==($c+1)" out1 | awk -F':' '{print $1}') ]
        then
            echo "DONE"
            break
        fi
     else
     echo " is not less"
    fi 
done

if [ "$TEMP" -le "$TRAFF_NUM" ]; then print "$TEMP is less then"; fi
