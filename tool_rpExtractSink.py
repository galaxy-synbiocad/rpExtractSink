#!/usr/bin/env python3

import logging
import argparse
import json
import requests

##
#
#
def rpExtractSinkUpload(input_sbml,
                        server_url,
                        output_sink,
                        remove_dead_end,
                        compartment_id):
    # Post request
    data = {'compartment_id': compartment_id,
            'remove_dead_end': remove_dead_end}
    files = {'input_sbml': open(input_sbml, 'rb'),
             'data': ('data.json', json.dumps(data))}
    r = requests.post(server_url+'/Query', files=files)
    r.raise_for_status()
    with open(output_sink, 'wb') as ot:
        ot.write(r.content)



if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate the sink from a model SBML by specifying the compartment')
    parser.add_argument('-input', type=str)
    parser.add_argument('-server_url', type=str, default='http://0.0.0.0:8888/REST')
    parser.add_argument('-output', type=str)
    parser.add_argument('-remove_dead_end', type=bool, default=True)
    parser.add_argument('-compartment_id', type=str, default='MNXC3')
    params = parser.parse_args()
    #TODO: check that the compartmentId exists and return an error if not. Idea: logging.error the list of available compartments if error is found
    if params.remove_dead_end=='True' or params.remove_dead_end=='T' or params.remove_dead_end==True or params.remove_dead_end=='true':
        remove_dead_end = True
    elif params.remove_dead_end=='False' or params.remove_dead_end=='F' or params.remove_dead_end==False or params.remove_dead_end=='false':
        remove_dead_end = False
    else:
        logging.error('Cannot detect entry remove_dead_end: '+str(params.remove_dead_end))
        exit(1)
    rpExtractSinkUpload(params.input, params.server_url, params.output, remove_dead_end, params.compartment_id)
    exit(0)
