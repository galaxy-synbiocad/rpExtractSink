#!/bin/bash

docker run -v ${PWD}/inside_run.sh:/home/inside_run.sh -v ${PWD}/tool_rpExtractSink.py:/home/tool_rpExtractSink.py -v ${PWD}/inSBML.sbml.xml:/home/inSBML.sbml.xml -v ${PWD}/results/:/home/results/ --rm brsynth/rpextractsink /bin/sh /home/inside_run.sh

cp results/outputSink.csv .
