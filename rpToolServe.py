import sys
sys.path.insert(0, '/home/')
import rpTool as rpGenSink
import rpToolCache


def main(inSBML, compartment_id):
    rpcache = rpToolCache.rpToolCache()
    rpgensink = rpGenSink.rpGenSink()
    rpgensink.mnxm_strc = rpcache.mnxm_strc
    return rpgensink.genSink(inSBML, compartment_id.read().encode())
