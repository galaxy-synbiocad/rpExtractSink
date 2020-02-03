import sys
sys.path.insert(0, '/home/')

import rpTool
#import rpToolCache
import rpCache

def main(inSBML, compartment_id):
    #rpcache = rpToolCache.rpToolCache()
    rpcache = rpCache.rpCache()
    rpgensink = rpTool.rpExtractSink()
    rpgensink.mnxm_strc = rpcache.mnxm_strc
    with open(inSBML, 'rb') as ins:
        return rpgensink.genSink(ins, compartment_id)
