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
import rpTool as rpExtractSink
import rpToolCache
#import rpCache


##############################################
################### REST #####################
##############################################


app = Flask(__name__)
api = Api(app)

rpcache = rpToolCache.rpToolCache()
#rpcache = rpCache.rpCache()


def stamp(data, status=1):
    appinfo = {'app': 'rpExtractSink', 'version': '1.0',
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
        rpextractsink = rpExtractSink.rpExtractSink()
        rpextractsink.mnxm_strc = rpcache.mnxm_strc
        return send_file(io.BytesIO(rpextractsink.genSink(inSBML, params['compartment_id']).read().encode()), as_attachment=True, attachment_filename='sink.csv', mimetype='text/csv')



api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    #debug = os.getenv('USER') == 'mdulac'
    app.run(host="0.0.0.0", port=8888, debug=True, threaded=True)
