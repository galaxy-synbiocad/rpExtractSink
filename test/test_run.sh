#!/bin/sh

docker run --network host -d -p 8888:8888 --name test_rpExtractSink brsynth/rpextractsink
sleep 10
python tool_rpExtractSink.py -inSBML test_inSBML.sbml -outputSink test_output.csv -compartment_id MNXC3 -server_url http://0.0.0.0:8888/REST
docker kill test_rpExtractSink
docker rm test_rpExtractSink
