#!/bin/bash

docker run -v ${PWD}/inside_run.sh:/home/inside_run.sh -v ${PWD}/tool_rpOptBioDes.py:/home/tool_rpOptBioDes.py -v ${PWD}/test_input.tar:/home/test_input.tar -v ${PWD}/results/:/home/results/ --rm brsynth/rpoptbiodes /bin/sh /home/inside_run.sh

cp results/test_output.tar .

#docker run -v ${PWD}/inside_run.sh:/home/inside_run.sh -v ${PWD}/tool_rpFBA.py:/home/tool_rpFBA.py -v ${PWD}/test_input.tar:/home/test_input.tar -v ${PWD}/test_inSBML.sbml:/home/test_inSBML.sbml -v ${PWD}/results/:/home/results/ --rm --user root brsynth/rpfba /bin/sh /home/inside_run.sh

