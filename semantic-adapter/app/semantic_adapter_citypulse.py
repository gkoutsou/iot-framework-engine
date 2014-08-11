__author__ = 'ehonlia'

import json

from flask import Blueprint, request, Response

from app.mimetype import correct_format, mimetype_map
from lib import semantics

semantic_adapter_citypulse = Blueprint('semantic_adapter_citypulse', __name__, template_folder='../templates')


@semantic_adapter_citypulse.route('/datapoints/<id>')
def datapoints(id):
    output_format = correct_format(request.args.get('format'))

    return Response(semantics.semantic_datapoints_citypulse(id, output_format, params=request.args),
                    mimetype=mimetype_map[output_format])
