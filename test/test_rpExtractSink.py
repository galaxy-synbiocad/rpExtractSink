import unittest
import tempfile
import os
import sys
import hashlib

sys.path.insert(0, '..')

import rpTool
#WARNING: Need to copy a version of rpSBML locally
import rpSBML
#WARNING: Also need to copy cache and cache/cid_strc.pickle.gz
import rpCache

class TestRPextractsink(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        rpcache = rpCache.rpCache()
        cidstrc = rpcache.getCIDstrc()
        self.rpex = rpTool.rpExtractSink()

    def test_genSink(self):
        with tempfile.TemporaryDirectory() as tmp_output_folder:
            self.rpex.genSink(os.path.join('data', 'model.xml'),
                              os.path.join(tmp_output_folder, 'sink.csv'),
                              True)
            with open(os.path.join(tmp_output_folder, 'sink.csv'), 'rb') as sinkf:
                self.assertEqual(hashlib.md5(sinkf.read()).hexdigest(), '3a00b9b8003dba014ea7c07c1534a9d6')
            self.rpex.genSink(os.path.join('data', 'model.xml'),
                              os.path.join(tmp_output_folder, 'sink.csv'),
                              False)
            with open(os.path.join(tmp_output_folder, 'sink.csv'), 'rb') as sinkf:
                self.assertEqual(hashlib.md5(sinkf.read()).hexdigest(), '3a00b9b8003dba014ea7c07c1534a9d6')
