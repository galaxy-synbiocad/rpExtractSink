#!/usr/bin/env python3

import logging
import argparse
import json
import requests

##
#
#
def rpGenSinkUpload(inSBML,
        server_url,
        outputSink,
        compartment_id):
    # Post request
    data = {'compartment_id': compartment_id}
    files = {'inSBML': open(inSBML, 'rb'),
             'data': ('data.json', json.dumps(data))}
    r = requests.post(server_url+'/Query', files=files)
    r.raise_for_status()
    with open(outputSink, 'wb') as ot:
        ot.write(r.content)



if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate the sink from a model SBML by specifying the compartment')
    parser.add_argument('-inSBML', type=str)
    parser.add_argument('-server_url', type=str)
    parser.add_argument('-outputSink', type=str)
    parser.add_argument('-compartment_id', type=str, default='MNXC3')
    #TODO: check that the compartmentId exists and return an error if not. Idea: print the list of available compartments if error is found
    params = parser.parse_args()
    rpGenSinkUpload(params.inSBML, params.server_url, params.outputSink, params.compartment_id)
    exit(0)
