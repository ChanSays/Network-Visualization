#!/usr/bin/env bash

set -x

log_dir=${16}

cd $log_dir

screen -d -m python /vol/eor-qa/sanity/cbhagwat-cvs/golden/eor/systest/lib/basic_sanity.py \
-build $1 -testsuite $2 -logicaldict $3 -testbed $4 -logfile $5 \
-reportfile $6 -email $7  -jobid $8 -pauseonfail $9 -basemode ${10} -collectlogs False \
-containermode ${11} -dockermode ${12} -issu_build ${13} -ctrl_plugin_image skip -issu_cases \
testReloadSwitch -patch skip -reportsubject ${14} -comments  > ${15}

