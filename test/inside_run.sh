#!/bin/bash

python tool_rpExtractSink.py -inSBML inSBML.sbml.xml -outputSink outputSink.csv -compartment_id MNXC3

mv outputSink.csv results/
