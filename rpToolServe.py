import sys
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

import rpTool
import rpCache

def main(input_sbml, output_sink, remove_dead_end, compartment_id):
    rpcache = rpCache.rpCache()
    rpgensink = rpTool.rpExtractSink()
    rpgensink.cid_strc = rpcache.getCIDstrc()
    rpgensink.genSink(input_sbml, output_sink, remove_dead_end, compartment_id)
