#!/bin/bash
set -x

log_dir=${11}

cd $log_dir

screen -d -m python /vol/eor-qa/sanity/cbhagwat-cvs/golden/eor/systest/lib/basic_sanity.py \
-build $1 -testsuite $2 -logicaldict $3 -testbed $4 -logfile $5 \
-reportfile $6 -email $7  -jobid $8 -pauseonfail False -basemode False -collectlogs False \
-containermode False -dockermode False -issu_build skip -ctrl_plugin_image skip -issu_cases \
testReloadSwitch -patch skip -reportsubject NXOSv $9 -comments  > ${10}
