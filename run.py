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


def main(input_sbml, output, compartment_id='MNXC3', remove_dead_end=True):
    """Generate the sink from an SBML model

    :param input_sbml: The path to the SBML file
    :param output: The path to the output sink file
    :param compartment_id: The id of the SBML compartment to extract the sink from
    :param remove_dead_end: Remove the dead end species

    :param input_sbml: str
    :param output: str
    :param compartment_id: str
    :param remove_dead_end: bool

    :rtype: None
    :return: None
    """
    docker_client = docker.from_env()
    image_str = 'brsynth/rpextractsink-standalone:v2'
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
        if os.path.exists(input_sbml):
            shutil.copy(input_sbml, tmpOutputFolder+'/input.sbml')
            command = ['python',
                       '/home/tool_rpExtractSink.py',
                       '-input',
                       '/home/tmp_output/input.sbml',
                       '-output',
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
            elif 'WARNING' in err_str:
                print(err_str)
            if not os.path.exists(tmpOutputFolder+'/output.dat'):
                print('ERROR: Cannot find the output file: '+str(tmpOutputFolder+'/output.dat'))
            else:
                shutil.copy(tmpOutputFolder+'/output.dat', output)
            container.remove()
        else:
            logging.error('Cannot find the input file: '+str(inputfile))
            exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate the sink from a model SBML by specifying the compartment')
    parser.add_argument('-input', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-compartment_id', type=str, default='MNXC3')
    parser.add_argument('-remove_dead_end', type=str, default='True')
    params = parser.parse_args()
    if params.remove_dead_end==True or params.remove_dead_end=='True' or params.remove_dead_end=='true' or params.remove_dead_end=='t':
        remove_dead_end = True 
    elif params.remove_dead_end==False or params.remove_dead_end=='False' or params.remove_dead_end=='false' or params.remove_dead_end=='f':
        remove_dead_end = False
    else:
        logging.error('Cannot interpret input -remove_dead_end: '+str(params.remove_dead_end))
        exit(1)
    main(params.input, params.output, params.compartment_id, remove_dead_end)
