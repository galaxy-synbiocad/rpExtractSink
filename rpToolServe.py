import sys
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    #level=logging.DEBUG,
    level=logging.WARNING,
    #level=logging.ERROR,
    datefmt='%Y-%m-%d %H:%M:%S')

import rpTool
import rpCache

def main(input_sbml, output_sink, remove_dead_end, compartment_id):
    """Generate the sink from an SBML model

    :param input_sbml: The path to the SBML file
    :param output_sink: The path to the output sink file
    :param remove_dead_end: Remove the dead end species
    :param compartment_id: The id of the SBML compartment to extract the sink from

    :param input_sbml: str
    :param output_sink: str
    :param remove_dead_end: bool
    :param compartment_id: str

    :rtype: None
    :return: None
    """
    rpcache = rpCache.rpCache()
    rpgensink = rpTool.rpExtractSink()
    rpgensink.cid_strc = rpcache.getCIDstrc()
    rpgensink.genSink(input_sbml, output_sink, remove_dead_end, compartment_id)
