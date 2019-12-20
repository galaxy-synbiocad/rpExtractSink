import os
import sys
import io


sys.path.insert(0, '/home/')
import rpTool as rpExtractSink
import rpToolCache


def main(inSBML, outputSink, compartment_id='MNXC3'):
    rpcache = rpToolCache.rpToolCache()
    rpgensink = rpExtractSink.rpExtractSink()
    rpgensink.mnxm_strc = rpcache.mnxm_strc
    with open(inSBML, 'rb') as inSBML_bytes:
        with open(outputSink, 'wb') as ot:
            ot.write(rpgensink.genSink(inSBML_bytes, compartment_id).read().encode())
