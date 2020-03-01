import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api
import sys
import io


sys.path.insert(0, '/home/')
import rpTool as rpExtractSink
import rpToolCache


##############################################
################### REST #####################
##############################################


app = Flask(__name__)
api = Api(app)

rpcache = rpToolCache.rpToolCache()


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
        input_sbml = request.files['input_sbml']
        params = json.load(request.files['data'])
        rpextractsink = rpExtractSink.rpExtractSink()
        rpextractsink.mnxm_strc = rpcache.mnxm_strc
        return send_file(io.BytesIO(rpextractsink.genSink(input_sbml, bool(params['remove_dead_end']), str(params['compartment_id'])).read().encode()), as_attachment=True, attachment_filename='sink.csv', mimetype='text/csv')



api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False, threaded=True)
