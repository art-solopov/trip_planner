from flask import Blueprint, request
from flask.json import jsonify
from werkzeug.datastructures import MultiDict

from .. import csrf
from ..shared import user_required
from .forms import GeocodeForm
from . import data


api = Blueprint('api', __name__, url_prefix='/api')


@api.route("/geocode", methods=('POST',))
@csrf.exempt
@user_required
def geocode():
    print(request.headers)
    form = GeocodeForm(MultiDict(request.json))
    trip_id = request.json['trip_id']
    return jsonify(data.geocode(form, trip_id))
