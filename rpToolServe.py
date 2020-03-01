import sys
#sys.path.insert(0, '/home/')

import rpTool
#import rpToolCache
import rpCache

def main(input_sbml, remove_dead_end, compartment_id):
    #rpcache = rpToolCache.rpToolCache()
    rpcache = rpCache.rpCache()
    rpgensink = rpTool.rpExtractSink()
    rpgensink.mnxm_strc = rpcache.mnxm_strc
    with open(input_sbml, 'rb') as ins:
        return rpgensink.genSink(ins, remove_dead_end, compartment_id)
