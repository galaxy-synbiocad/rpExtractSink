import sys

import rpTool
import rpCache

def main(input_sbml, output_sink, remove_dead_end, compartment_id):
    #rpcache = rpToolCache.rpToolCache()
    rpcache = rpCache.rpCache()
    rpgensink = rpTool.rpExtractSink()
    rpgensink.mnxm_strc = rpcache.mnxm_strc
    rpgensink.genSink(input_sbml, output_sink, remove_dead_end, compartment_id)
