#!/usr/bin/env python3


import argparse
import sys

sys.path.insert(0, '/home/')
import rpToolServe


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate the sink from a model SBML by specifying the compartment')
    parser.add_argument('-input_sbml', type=str)
    parser.add_argument('-output_sink', type=str)
    parser.add_argument('-remove_dead_end', type=str:)
    parser.add_argument('-compartment_id', type=str, default='MNXC3')
    #TODO: check that the compartmentId exists and return an error if not. Idea: print the list of available compartments if error is found
    params = parser.parse_args()
    with open(params.output_sink, 'wb') as ot:
        ot.write(rpToolServe.main(params.input_sbml, params.remove_dead_end, params.compartment_id).read().encode())
