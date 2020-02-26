#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Extract the sink from an SBML into RP2 friendly format

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


##
#
#
def main(input_sbml, output_sink, compartment_id):
    docker_client = docker.from_env()
    image_str = 'brsynth/rpextractsink-standalone:dev'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        shutil.copy(input_sbml, tmpOutputFolder+'/input_sbml.sbml')
        command = ['/home/tool_rpExtractSink.py',
                   '-input_sbml',
                   '/home/tmp_output/input_sbml.sbml',
                   '-output_sink',
                   '/home/tmp_output/output.dat',
                   '-compartment_id',
                   compartment_id]
        docker_client.containers.run(image_str, 
                command, 
                auto_remove=True, 
                detach=False, 
                volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        shutil.copy(tmpOutputFolder+'/output.dat', os.getcwd()+'/'+output_sink)


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate the sink from a model SBML by specifying the compartment')
    parser.add_argument('-input_sbml', type=str)
    parser.add_argument('-output_sink', type=str)
    parser.add_argument('-compartment_id', type=str, default='MNXC3')
    params = parser.parse_args()
    main(params.input_sbml, params.output_sink, params.compartment_id)
