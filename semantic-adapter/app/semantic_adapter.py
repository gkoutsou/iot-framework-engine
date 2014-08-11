__author__ = 'ehonlia'

import json

from flask import Response, request, jsonify, Blueprint

from app.mimetype import JSON, mimetype_map, correct_format
from lib import semantics


semantic_adapter = Blueprint('semantic_adapter', __name__, template_folder='../templates')


@semantic_adapter.route('/streams')
def streams():
    output_format = correct_format(request.args.get('format'))
    combined = request.args.get('combined')

    if combined is None:
        return Response(json.dumps(semantics.semantic_streams(output_format, request.args)), mimetype=JSON)
    else:
        return Response(semantics.semantic_streams_combined(output_format, request.args),
                        mimetype=mimetype_map[output_format])


@semantic_adapter.route('/virtual_streams')
def virtual_streams():
    output_format = correct_format(request.args.get('format'))
    combined = request.args.get('combined')

    if combined is None:
        return Response(json.dumps(semantics.semantic_virtual_streams(output_format, request.args)), mimetype=JSON)
    else:
        return Response(semantics.semantic_virtual_streams_combined(output_format, params=request.args),
                        mimetype=mimetype_map[output_format])


@semantic_adapter.route('/datapoints')
def datapoints():
    output_format = correct_format(request.args.get('format'))
    combined = request.args.get('combined')

    if combined is None:
        return Response(json.dumps(semantics.semantic_datapoints(output_format, params=request.args)), mimetype=JSON)
    else:
        return Response(semantics.semantic_datapoints_combined(output_format, params=request.args),
                        mimetype=mimetype_map[output_format])


@semantic_adapter.route('/vsdatapoints')
def vsdatapoints():
    output_format = correct_format(request.args.get('format'))
    combined = request.args.get('combined')

    if combined is None:
        return Response(json.dumps(semantics.semantic_datapoints(output_format, 'vsdatapoint', request.args)),
                        mimetype=JSON)
    else:
        return Response(semantics.semantic_datapoints_combined(output_format, 'vsdatapoint', request.args),
                        mimetype=mimetype_map[output_format])


@semantic_adapter.route('/mapping')
def mapping():
    return jsonify(semantics.mapping())
