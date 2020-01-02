import sys
sys.path.insert(0, '/home/')
import rpTool as rpGenSink
import rpToolCache


def main():
    rpcache = rpToolCache.rpToolCache()
    rpgensink = rpGenSink.rpGenSink()
    rpgensink.mnxm_strc = rpcache.mnxm_strc
    return rpgensink.genSink(inSBML, params['compartment_id']).read().encode())
