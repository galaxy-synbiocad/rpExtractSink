import os
import sys
import io


sys.path.insert(0, '/home/')
import rpTool as rpExtractSink
import rpToolCache


def main(inSBML, outputSink, compartment_id='MNXC3'):
    rpcache = rpToolCache.rpToolCache()
    rpextractsink = rpExtractSink.rpExtractSink()
    rpextractsink.mnxm_strc = rpcache.mnxm_strc
    with open(inSBML, 'rb') as inSBML_bytes:
        with open(outputSink, 'wb') as ot:
            ot.write(rpextractsink.genSink(inSBML_bytes, compartment_id).read().encode())
