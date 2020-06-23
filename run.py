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
def main(input_sbml, output_sink, compartment_id='MNXC3', remove_dead_end=True):
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
        shutil.copy(input_sbml, tmpOutputFolder+'/input.sbml')
        command = ['python',
                   '/home/tool_rpExtractSink.py',
                   '-input_sbml',
                   '/home/tmp_output/input.sbml',
                   '-output_sink',
                   '/home/tmp_output/output.dat',
                   '-compartment_id',
                   str(compartment_id),
                   '-remove_dead_end',
                   str(remove_dead_end)]
        container = docker_client.containers.run(image_str,
                                                 command,
                                                 detach=True,
                                                 stderr=True,
                                                 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        err_str = err.decode('utf-8')
        if 'ERROR' in err_str:
            print(err_str)
        else:
            shutil.copy(tmpOutputFolder+'/output.dat', output_sink)
        container.remove()


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate the sink from a model SBML by specifying the compartment')
    parser.add_argument('-input_sbml', type=str)
    parser.add_argument('-output_sink', type=str)
    parser.add_argument('-compartment_id', type=str, default='MNXC3')
    parser.add_argument('-remove_dead_end', type=str, default='True')
    params = parser.parse_args()
    if params.remove_dead_end==True or params.remove_dead_end=='True' or params.remove_dead_end=='true' or params.remove_dead_end=='t':
        remove_dead_end = True 
    elif params.remove_dead_end==False or params.remove_dead_end=='False' or params.remove_dead_end=='false' or params.remove_dead_end=='f':
        remove_dead_end = False
    else:
        logging.error('Cannot interpret input -remove_dead_end: '+str(params.remove_dead_end))
    main(params.input_sbml, params.output_sink, params.compartment_id, remove_dead_end)
