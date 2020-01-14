import os
import uuid
import shutil
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api
#from rpviz.main import run
import sys
import io


sys.path.insert(0, '/home/')
import rpTool as rpGenSink
import rpToolCache

##############################################
################### REST #####################
##############################################

app = Flask(__name__)
api = Api(app)
#dataFolder = os.path.join( os.path.dirname(__file__),  'data' )


#TODO: test that it works well
#declare the rpReader globally to avoid reading the pickle at every instance
rpcache = rpToolCache.rpToolCache()


def stamp(data, status=1):
    appinfo = {'app': 'rpGenSink', 'version': '1.0',
               'author': 'Melchior du Lac',
               'organization': 'BRS',
               'time': datetime.now().isoformat(),
               'status': status}
    out = appinfo.copy()
    out['data'] = data
    return out


class RestApp(Resource):
    """ REST App."""
    def post(self):
        return jsonify(stamp(None))
    def get(self):
        return jsonify(stamp(None))


class RestQuery(Resource):
    """ REST interface that generates the Design.
        Avoid returning numpy or pandas object in
        order to keep the client lighter.
    """
    def post(self):
        inSBML = request.files['inSBML']
        params = json.load(request.files['data'])
        #pass the cache parameters to the rpReader
        rpgensink = rpGenSink.rpGenSink()
        rpgensink.mnxm_strc = rpcache.mnxm_strc

        #pass the files to the rpReader
        #tf = tarfile.open(fileobj=outputTar, mode='w:xz')
        #sink_string = rpgensink.genSink(inSBML, params['compartment_id'])
        #sink_stringio = rpgensink.genSink(inSBML, params['compartment_id'])
        #return send_file(sink_stringio, as_attachment=True, attachment_filename='sink.csv', mimetype='text/csv')
        #outputSink = rpgensink.genSink(inSBML, params['compartment_id'])
        #return send_file(io.BytesIO(outputSink.read().encode()), as_attachment=True, attachment_filename='sink.csv', mimetype='text/csv')
        return send_file(io.BytesIO(rpgensink.genSink(inSBML, params['compartment_id']).read().encode()), as_attachment=True, attachment_filename='sink.csv', mimetype='text/csv')



api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    #debug = os.getenv('USER') == 'mdulac'
    app.run(host="0.0.0.0", port=8888, debug=False, threaded=True)
